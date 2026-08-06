from flask import Blueprint
from src.controllers import task_controller
from src.middlewares.auth import token_required

task_bp = Blueprint('tasks', __name__)

task_bp.route('/tasks', methods=['GET'])(token_required(task_controller.get_tasks))
task_bp.route('/tasks/<int:task_id>', methods=['GET'])(token_required(task_controller.get_task))
task_bp.route('/tasks', methods=['POST'])(token_required(task_controller.create_task))
task_bp.route('/tasks/<int:task_id>', methods=['PUT'])(token_required(task_controller.update_task))
task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])(token_required(task_controller.delete_task))
task_bp.route('/tasks/search', methods=['GET'])(token_required(task_controller.search_tasks))
task_bp.route('/tasks/stats', methods=['GET'])(token_required(task_controller.task_stats))
