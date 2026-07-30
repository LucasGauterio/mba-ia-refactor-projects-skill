from flask import jsonify
from src.config.database import get_db

def health_check():
    """Realiza uma verificação de integridade operacional do sistema e do banco de dados de forma segura, sem vazamento de segredos."""
    db = get_db()
    cursor = db.cursor()
    
    # Testa a comunicação com a base de dados
    cursor.execute("SELECT 1")
    
    # Recupera contagens estatísticas de tabelas básicas
    cursor.execute("SELECT COUNT(*) FROM produtos")
    produtos = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos = cursor.fetchone()[0]

    return jsonify({
        "status": "ok",
        "database": "connected",
        "counts": {
            "produtos": produtos,
            "usuarios": usuarios,
            "pedidos": pedidos
        },
        "versao": "1.0.0"
    }), 200
