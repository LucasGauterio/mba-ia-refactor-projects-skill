from flask import Blueprint
from src.controllers import user_controller
from src.middlewares.auth import token_required, admin_required

user_bp = Blueprint('users', __name__)

user_bp.route('/users', methods=['GET'])(token_required(user_controller.get_users))
user_bp.route('/users/<int:user_id>', methods=['GET'])(token_required(user_controller.get_user))
user_bp.route('/users', methods=['POST'])(user_controller.create_user)  # Público para cadastro
user_bp.route('/users/<int:user_id>', methods=['PUT'])(token_required(user_controller.update_user))
user_bp.route('/users/<int:user_id>', methods=['DELETE'])(token_required(admin_required(user_controller.delete_user))) # Apenas admins podem deletar
user_bp.route('/users/<int:user_id>/tasks', methods=['GET'])(token_required(user_controller.get_user_tasks))
user_bp.route('/login', methods=['POST'])(user_controller.login)
