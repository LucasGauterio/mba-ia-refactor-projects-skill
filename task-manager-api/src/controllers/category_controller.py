from flask import request, jsonify
from src.config.database import db
from src.models.category import Category
from src.models.task import Task
from sqlalchemy import func

def get_categories():
    categories = Category.query.all()
    
    # Otimização da query N+1: Conta a quantidade de tarefas em uma única consulta agrupada
    counts = db.session.query(Task.category_id, func.count(Task.id))\
        .filter(Task.category_id.isnot(None))\
        .group_by(Task.category_id).all()
        
    counts_dict = {cat_id: count for cat_id, count in counts}
    
    result = []
    for c in categories:
        cat_data = c.to_dict()
        cat_data['task_count'] = counts_dict.get(c.id, 0)
        result.append(cat_data)
        
    return jsonify(result), 200

def create_category():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    name = data.get('name')
    if not name:
        return jsonify({'error': 'Nome é obrigatório'}), 400

    category = Category()
    category.name = name
    category.description = data.get('description', '')
    category.color = data.get('color', '#000000')

    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201

def update_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Categoria não encontrada'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Dados inválidos'}), 400

    if 'name' in data:
        cat.name = data['name']
    if 'description' in data:
        cat.description = data['description']
    if 'color' in data:
        cat.color = data['color']

    db.session.commit()
    return jsonify(cat.to_dict()), 200

def delete_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Categoria não encontrada'}), 404

    # Garante Integridade Referencial: Desvincula as tarefas associadas antes de excluir a categoria
    Task.query.filter_by(category_id=cat_id).update({Task.category_id: None})
    
    db.session.delete(cat)
    db.session.commit()
    return jsonify({'message': 'Categoria deletada'}), 200
