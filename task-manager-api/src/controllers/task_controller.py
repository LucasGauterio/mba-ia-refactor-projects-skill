from flask import jsonify, request
from src.config.database import db
from src.models.task import Task
from src.models.user import User
from src.models.category import Category
from src.config.settings import VALID_STATUSES
from src.utils.helpers import parse_date
from datetime import datetime
from sqlalchemy.orm import joinedload

def get_tasks():
    # Eager load user e category com joinedload para evitar o gargalo N+1
    tasks = Task.query.options(joinedload(Task.user), joinedload(Task.category)).all()
    result = []
    for t in tasks:
        task_data = {
            'id': t.id,
            'title': t.title,
            'description': t.description,
            'status': t.status,
            'priority': t.priority,
            'user_id': t.user_id,
            'category_id': t.category_id,
            'created_at': str(t.created_at),
            'updated_at': str(t.updated_at),
            'due_date': str(t.due_date) if t.due_date else None,
            'tags': t.tags.split(',') if t.tags else [],
            'overdue': t.is_overdue(),
            'user_name': t.user.name if t.user else None,
            'category_name': t.category.name if t.category else None
        }
        result.append(task_data)
    return jsonify(result), 200

def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404
        
    data = task.to_dict()
    data['overdue'] = task.is_overdue()
    return jsonify(data), 200

def create_task():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    title = data.get('title')
    if not title:
        return jsonify({'error': 'Título é obrigatório'}), 400

    if len(title) < 3:
        return jsonify({'error': 'Título muito curto'}), 400
    if len(title) > 200:
        return jsonify({'error': 'Título muito longo'}), 400

    status = data.get('status', 'pending')
    priority = data.get('priority', 3)
    user_id = data.get('user_id')
    category_id = data.get('category_id')
    due_date = data.get('due_date')
    tags = data.get('tags')

    if status not in VALID_STATUSES:
        return jsonify({'error': 'Status inválido'}), 400

    if priority < 1 or priority > 5:
        return jsonify({'error': 'Prioridade deve ser entre 1 e 5'}), 400

    if user_id:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404

    if category_id:
        cat = Category.query.get(category_id)
        if not cat:
            return jsonify({'error': 'Categoria não encontrada'}), 404

    task = Task()
    task.title = title
    task.description = data.get('description', '')
    task.status = status
    task.priority = priority
    task.user_id = user_id
    task.category_id = category_id

    if due_date:
        parsed = parse_date(due_date)
        if not parsed:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        task.due_date = parsed

    if tags:
        if isinstance(tags, list):
            task.tags = ','.join(tags)
        else:
            task.tags = tags

    db.session.add(task)
    db.session.commit()
    print(f"Task criada: {task.id} - {task.title}")
    return jsonify(task.to_dict()), 201

def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    if 'title' in data:
        title = data['title']
        if len(title) < 3:
            return jsonify({'error': 'Título muito curto'}), 400
        if len(title) > 200:
            return jsonify({'error': 'Título muito longo'}), 400
        task.title = title

    if 'description' in data:
        task.description = data['description']

    if 'status' in data:
        if data['status'] not in VALID_STATUSES:
            return jsonify({'error': 'Status inválido'}), 400
        task.status = data['status']

    if 'priority' in data:
        priority = data['priority']
        if priority < 1 or priority > 5:
            return jsonify({'error': 'Prioridade deve ser entre 1 e 5'}), 400
        task.priority = priority

    if 'user_id' in data:
        user_id = data['user_id']
        if user_id:
            user = User.query.get(user_id)
            if not user:
                return jsonify({'error': 'Usuário não encontrado'}), 404
        task.user_id = user_id

    if 'category_id' in data:
        category_id = data['category_id']
        if category_id:
            cat = Category.query.get(category_id)
            if not cat:
                return jsonify({'error': 'Categoria não encontrada'}), 404
        task.category_id = category_id

    if 'due_date' in data:
        due_date = data['due_date']
        if due_date:
            parsed = parse_date(due_date)
            if not parsed:
                return jsonify({'error': 'Formato de data inválido'}), 400
            task.due_date = parsed
        else:
            task.due_date = None

    if 'tags' in data:
        tags = data['tags']
        if isinstance(tags, list):
            task.tags = ','.join(tags)
        else:
            task.tags = tags

    db.session.commit()
    print(f"Task atualizada: {task.id}")
    return jsonify(task.to_dict()), 200

def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task não encontrada'}), 404

    db.session.delete(task)
    db.session.commit()
    print(f"Task deletada: {task_id}")
    return jsonify({'message': 'Task deletada com sucesso'}), 200

def search_tasks():
    query = request.args.get('q', '')
    status = request.args.get('status', '')
    priority = request.args.get('priority', '')
    user_id = request.args.get('user_id', '')

    tasks = Task.query

    if query:
        tasks = tasks.filter(
            db.or_(
                Task.title.like(f'%{query}%'),
                Task.description.like(f'%{query}%')
            )
        )

    if status:
        tasks = tasks.filter(Task.status == status)

    if priority:
        tasks = tasks.filter(Task.priority == int(priority))

    if user_id:
        tasks = tasks.filter(Task.user_id == int(user_id))

    results = tasks.all()
    output = [t.to_dict() for t in results]
    return jsonify(output), 200

def task_stats():
    # Executa counts no banco de dados para evitar ler todas as linhas na memória
    total = Task.query.count()
    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    done = Task.query.filter_by(status='done').count()
    cancelled = Task.query.filter_by(status='cancelled').count()

    # Conta tasks atrasadas no banco diretamente
    overdue_count = Task.query.filter(
        Task.due_date.isnot(None),
        Task.due_date < datetime.utcnow(),
        Task.status.notin_(['done', 'cancelled'])
    ).count()

    stats = {
        'total': total,
        'pending': pending,
        'in_progress': in_progress,
        'done': done,
        'cancelled': cancelled,
        'overdue': overdue_count,
        'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
    }
    return jsonify(stats), 200
