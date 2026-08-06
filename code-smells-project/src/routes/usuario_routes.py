from flask import Blueprint
from src.controllers import usuario_controller

usuario_bp = Blueprint("usuario", __name__)

usuario_bp.route("/usuarios", methods=["GET"])(usuario_controller.listar_usuarios)
usuario_bp.route("/usuarios/<int:id>", methods=["GET"])(usuario_controller.buscar_usuario)
usuario_bp.route("/usuarios", methods=["POST"])(usuario_controller.criar_usuario)
usuario_bp.route("/login", methods=["POST"])(usuario_controller.login)
