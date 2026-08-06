from flask import Blueprint, jsonify
from src.controllers import general_controller
from src.middlewares.auth import admin_required
from src.config.database import get_db

general_bp = Blueprint("general", __name__)

# Registrar rotas públicas
general_bp.route("/", methods=["GET"])(general_controller.index)
general_bp.route("/health", methods=["GET"])(general_controller.health_check)

# Registrar rota administrativa protegida por token
@general_bp.route("/admin/reset-db", methods=["POST"])
@admin_required
def reset_database():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM itens_pedido")
    cursor.execute("DELETE FROM pedidos")
    cursor.execute("DELETE FROM produtos")
    cursor.execute("DELETE FROM usuarios")
    db.commit()
    print("!!! BANCO DE DADOS RESETADO !!!")
    return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
