from flask import Blueprint
from src.controllers import category_controller

category_bp = Blueprint('categories', __name__)

category_bp.route('/categories', methods=['GET'])(category_controller.get_categories)
category_bp.route('/categories', methods=['POST'])(category_controller.create_category)
category_bp.route('/categories/<int:cat_id>', methods=['PUT'])(category_controller.update_category)
category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])(category_controller.delete_category)
