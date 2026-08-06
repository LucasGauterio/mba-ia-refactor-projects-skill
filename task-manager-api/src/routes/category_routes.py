from flask import Blueprint
from src.controllers import category_controller
from src.middlewares.auth import token_required

category_bp = Blueprint('categories', __name__)

category_bp.route('/categories', methods=['GET'])(token_required(category_controller.get_categories))
category_bp.route('/categories', methods=['POST'])(token_required(category_controller.create_category))
category_bp.route('/categories/<int:cat_id>', methods=['PUT'])(token_required(category_controller.update_category))
category_bp.route('/categories/<int:cat_id>', methods=['DELETE'])(token_required(category_controller.delete_category))
