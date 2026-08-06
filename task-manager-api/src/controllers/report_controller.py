from flask import jsonify
from src.config.database import db
from src.models.task import Task
from src.models.user import User
from src.models.category import Category
from datetime import datetime, timedelta
from sqlalchemy import func

def summary_report():
    total_tasks = Task.query.count()
    total_users = User.query.count()
    total_categories = Category.query.count()

    # Conta tasks por status
    pending = Task.query.filter_by(status='pending').count()
    in_progress = Task.query.filter_by(status='in_progress').count()
    done = Task.query.filter_by(status='done').count()
    cancelled = Task.query.filter_by(status='cancelled').count()

    # Conta tasks por prioridade
    p1 = Task.query.filter_by(priority=1).count()
    p2 = Task.query.filter_by(priority=2).count()
    p3 = Task.query.filter_by(priority=3).count()
    p4 = Task.query.filter_by(priority=4).count()
    p5 = Task.query.filter_by(priority=5).count()

    # Busca apenas tasks atrasadas com uma query específica (evita carregar tudo em memória)
    overdue_tasks = Task.query.filter(
        Task.due_date.isnot(None),
        Task.due_date < datetime.utcnow(),
        Task.status.notin_(['done', 'cancelled'])
    ).all()

    overdue_count = len(overdue_tasks)
    overdue_list = []
    for t in overdue_tasks:
        overdue_list.append({
            'id': t.id,
            'title': t.title,
            'due_date': str(t.due_date),
            'days_overdue': (datetime.utcnow() - t.due_date).days
        })

    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_tasks = Task.query.filter(Task.created_at >= seven_days_ago).count()

    recent_done = Task.query.filter(
        Task.status == 'done',
        Task.updated_at >= seven_days_ago
    ).count()

    # Otimização da Query N+1 de estatísticas dos usuários
    # 1. Agrupa contagem total por usuário
    total_by_user = db.session.query(
        Task.user_id,
        func.count(Task.id)
    ).filter(Task.user_id.isnot(None)).group_by(Task.user_id).all()
    total_dict = {user_id: count for user_id, count in total_by_user}

    # 2. Agrupa contagem de concluídas por usuário
    completed_by_user = db.session.query(
        Task.user_id,
        func.count(Task.id)
    ).filter(Task.user_id.isnot(None), Task.status == 'done').group_by(Task.user_id).all()
    completed_dict = {user_id: count for user_id, count in completed_by_user}

    # 3. Monta estatísticas de usuários sem gerar queries adicionais no laço
    users = User.query.all()
    user_stats = []
    for u in users:
        total = total_dict.get(u.id, 0)
        completed = completed_dict.get(u.id, 0)
        user_stats.append({
            'user_id': u.id,
            'user_name': u.name,
            'total_tasks': total,
            'completed_tasks': completed,
            'completion_rate': round((completed / total) * 100, 2) if total > 0 else 0
        })

    report = {
        'generated_at': str(datetime.utcnow()),
        'overview': {
            'total_tasks': total_tasks,
            'total_users': total_users,
            'total_categories': total_categories,
        },
        'tasks_by_status': {
            'pending': pending,
            'in_progress': in_progress,
            'done': done,
            'cancelled': cancelled,
        },
        'tasks_by_priority': {
            'critical': p1,
            'high': p2,
            'medium': p3,
            'low': p4,
            'minimal': p5,
        },
        'overdue': {
            'count': overdue_count,
            'tasks': overdue_list,
        },
        'recent_activity': {
            'tasks_created_last_7_days': recent_tasks,
            'tasks_completed_last_7_days': recent_done,
        },
        'user_productivity': user_stats,
    }

    return jsonify(report), 200

def user_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Usuário não encontrado'}), 404

    tasks = Task.query.filter_by(user_id=user_id).all()

    total = len(tasks)
    done = 0
    pending = 0
    in_progress = 0
    cancelled = 0
    overdue = 0
    high_priority = 0

    for t in tasks:
        if t.status == 'done':
            done = done + 1
        elif t.status == 'pending':
            pending = pending + 1
        elif t.status == 'in_progress':
            in_progress = in_progress + 1
        elif t.status == 'cancelled':
            cancelled = cancelled + 1

        if t.priority <= 2:
            high_priority = high_priority + 1

        if t.due_date and t.due_date < datetime.utcnow():
            if t.status not in ['done', 'cancelled']:
                overdue = overdue + 1

    report = {
        'user': {
            'id': user.id,
            'name': user.name,
            'email': user.email,
        },
        'statistics': {
            'total_tasks': total,
            'done': done,
            'pending': pending,
            'in_progress': in_progress,
            'cancelled': cancelled,
            'overdue': overdue,
            'high_priority': high_priority,
            'completion_rate': round((done / total) * 100, 2) if total > 0 else 0
        }
    }

    return jsonify(report), 200
