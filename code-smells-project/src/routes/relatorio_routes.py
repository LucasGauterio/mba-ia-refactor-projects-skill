from flask import Blueprint
from src.controllers import relatorio_controller
from src.middlewares.auth import admin_required

relatorio_bp = Blueprint("relatorio", __name__)

# Registrar rota de vendas protegida por token administrativo
relatorio_bp.route("/relatorios/vendas", methods=["GET"])(admin_required(relatorio_controller.relatorio_vendas))
