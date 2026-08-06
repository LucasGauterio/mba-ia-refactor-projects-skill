from flask import Blueprint
from src.controllers import pedido_controller

pedido_bp = Blueprint("pedido", __name__)

pedido_bp.route("/pedidos", methods=["POST"])(pedido_controller.criar_pedido)
pedido_bp.route("/pedidos", methods=["GET"])(pedido_controller.listar_todos_pedidos)
pedido_bp.route("/pedidos/usuario/<int:usuario_id>", methods=["GET"])(pedido_controller.listar_pedidos_usuario)
pedido_bp.route("/pedidos/<int:pedido_id>/status", methods=["PUT"])(pedido_controller.atualizar_status_pedido)
