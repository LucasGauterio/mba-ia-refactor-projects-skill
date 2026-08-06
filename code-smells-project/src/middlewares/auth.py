from flask import request, jsonify
from functools import wraps
from src.config.settings import ADMIN_TOKEN

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({
                "erro": "Token de autorização ausente",
                "sucesso": False
            }), 401

        # Tratar formatos "Bearer <token>" ou apenas "<token>"
        parts = auth_header.split(" ")
        if len(parts) == 2 and parts[0].lower() == "bearer":
            token = parts[1]
        else:
            token = parts[0]

        if token != ADMIN_TOKEN:
            return jsonify({
                "erro": "Acesso não autorizado. Token inválido",
                "sucesso": False
            }), 403

        return f(*args, **kwargs)
    return decorated
