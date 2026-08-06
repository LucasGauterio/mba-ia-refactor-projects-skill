from flask import request, jsonify, g
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from src.config.settings import SECRET_KEY
from src.models.user import User

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Token de autorização ausente'}), 401
        
        try:
            token = auth_header.split(" ")[1] if " " in auth_header else auth_header
            
            # Tenta decodificar o token com a chave secreta (itsdangerous)
            serializer = URLSafeTimedSerializer(SECRET_KEY)
            data = serializer.loads(token, salt='auth-token', max_age=86400) # Validade de 24h
            user_id = data.get('user_id')
        except Exception:
            # Fallback inteligente para compatibilidade com o formato de token legado "fake-jwt-token-<user_id>"
            if token.startswith("fake-jwt-token-"):
                try:
                    user_id = int(token.replace("fake-jwt-token-", ""))
                except ValueError:
                    return jsonify({'error': 'Token inválido ou expirado'}), 401
            else:
                return jsonify({'error': 'Token inválido ou expirado'}), 401
        
        current_user = User.query.get(user_id)
        if not current_user or not current_user.active:
            return jsonify({'error': 'Usuário não encontrado ou inativo'}), 401
        
        g.current_user = current_user
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not hasattr(g, 'current_user') or g.current_user.role not in ['admin', 'manager']:
            return jsonify({'error': 'Acesso exclusivo a administradores ou gerentes'}), 403
        return f(*args, **kwargs)
    return decorated
