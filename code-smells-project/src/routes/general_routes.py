from flask import Blueprint, jsonify
import src.controllers.general_controller as general_controller
from src.middlewares.auth import admin_required
from src.config.database import get_db

general_bp = Blueprint('general', __name__)

general_bp.add_url_rule("/health", "health_check", general_controller.health_check, methods=["GET"])

@general_bp.route("/")
def index():
    return jsonify({
        "mensagem": "Bem-vindo à API da Loja",
        "versao": "1.0.0",
        "endpoints": {
            "produtos": "/produtos",
            "usuarios": "/usuarios",
            "pedidos": "/pedidos",
            "login": "/login",
            "relatorios": "/relatorios/vendas",
            "health": "/health"
        }
    })

@general_bp.route("/admin/reset-db", methods=["POST"])
@admin_required
def reset_database():
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute("BEGIN TRANSACTION;")
        cursor.execute("DELETE FROM itens_pedido")
        cursor.execute("DELETE FROM pedidos")
        cursor.execute("DELETE FROM produtos")
        cursor.execute("DELETE FROM usuarios")
        db.commit()
        print("!!! BANCO DE DADOS RESETADO !!!")
        return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
    except Exception as e:
        db.rollback()
        raise e
