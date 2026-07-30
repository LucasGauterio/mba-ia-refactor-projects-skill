from flask import request, jsonify
from functools import wraps
from src.config.settings import ADMIN_TOKEN

def admin_required(f):
    """Decorator de autenticação para validar cabeçalhos Bearer contendo o ADMIN_TOKEN."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return jsonify({"erro": "Token de autorização ausente", "sucesso": False}), 401
        
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            return jsonify({
                "erro": "Formato de token inválido. Use 'Bearer <token>'",
                "sucesso": False
            }), 401
        
        token = parts[1]
        if token != ADMIN_TOKEN:
            return jsonify({"erro": "Acesso não autorizado. Token inválido", "sucesso": False}), 403
            
        return f(*args, **kwargs)
    return decorated_function
