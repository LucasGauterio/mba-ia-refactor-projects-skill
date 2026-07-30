from flask import jsonify, request
from src.config.database import db
from src.models.category import Category
from src.utils.helpers import is_valid_color
from sqlalchemy.orm import selectinload

def get_categories():
    # Eager load tasks para evitar N+1 query no count de tasks por categoria
    categories = Category.query.options(selectinload(Category.tasks)).all()
    result = []
    for c in categories:
        cat_data = c.to_dict()
        cat_data['task_count'] = len(c.tasks)
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
    
    color = data.get('color', '#000000')
    if not is_valid_color(color):
        category.color = '#000000'
    else:
        category.color = color

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
        color = data['color']
        if is_valid_color(color):
            cat.color = color

    db.session.commit()
    return jsonify(cat.to_dict()), 200

def delete_category(cat_id):
    cat = Category.query.get(cat_id)
    if not cat:
        return jsonify({'error': 'Categoria não encontrada'}), 404

    db.session.delete(cat)
    db.session.commit()
    return jsonify({'message': 'Categoria deletada'}), 200
