from flask import Blueprint
from src.controllers import report_controller

report_bp = Blueprint('reports', __name__)

report_bp.route('/reports/summary', methods=['GET'])(report_controller.summary_report)
report_bp.route('/reports/user/<int:user_id>', methods=['GET'])(report_controller.user_report)
