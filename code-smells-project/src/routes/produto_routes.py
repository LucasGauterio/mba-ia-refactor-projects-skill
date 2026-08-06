from flask import Blueprint
from src.controllers import produto_controller

produto_bp = Blueprint("produto", __name__)

produto_bp.route("/produtos", methods=["GET"])(produto_controller.listar_produtos)
produto_bp.route("/produtos/busca", methods=["GET"])(produto_controller.buscar_produtos)
produto_bp.route("/produtos/<int:id>", methods=["GET"])(produto_controller.buscar_produto)
produto_bp.route("/produtos", methods=["POST"])(produto_controller.criar_produto)
produto_bp.route("/produtos/<int:id>", methods=["PUT"])(produto_controller.atualizar_produto)
produto_bp.route("/produtos/<int:id>", methods=["DELETE"])(produto_controller.deletar_produto)
