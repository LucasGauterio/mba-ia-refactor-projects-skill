import logging
from flask import jsonify

logger = logging.getLogger(__name__)

def register_error_handlers(app):
    """Registra tratadores de exceção centralizados no aplicativo Flask."""
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Registra o log detalhado no servidor contendo a pilha de execução (stack trace)
        logger.error(f"Erro interno não tratado: {str(e)}", exc_info=True)
        
        # Retorna uma mensagem amigável e segura para o cliente externo
        return jsonify({
            "erro": "Ocorreu um erro interno no servidor",
            "sucesso": False
        }), 500
