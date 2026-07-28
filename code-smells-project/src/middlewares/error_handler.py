import traceback
from flask import jsonify
from werkzeug.exceptions import HTTPException

def register_error_handlers(app):
    """
    Registra tratadores de erro globais na aplicação Flask.
    Captura exceções inesperadas para evitar vazamento de informações do servidor.
    """
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Trata exceções HTTP conhecidas (ex: 404 Not Found, 405 Method Not Allowed)
        if isinstance(e, HTTPException):
            return jsonify({"erro": e.description, "sucesso": False}), e.code

        # Trata exceções genéricas
        # Loga stack trace no console de forma detalhada para depuração
        print("=" * 80)
        print("EXCEÇÃO INTERNA CAPTURADA PELO MIDDLEWARE DE ERROS:")
        traceback.print_exc()
        print("=" * 80)

        # Retorna erro opaco e seguro para o cliente
        return jsonify({
            "erro": "Ocorreu um erro interno no servidor",
            "sucesso": False
        }), 500
