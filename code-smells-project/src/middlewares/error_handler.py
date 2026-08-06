from flask import jsonify
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger("app_error_handler")

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Loga o erro internamente com stack trace para observabilidade
        logger.error("Erro interno detectado: %s", str(e), exc_info=True)
        # Retorna uma mensagem genérica sem vazar segredos ou detalhes internos do banco
        return jsonify({
            "erro": "Ocorreu um erro interno no servidor",
            "sucesso": False
        }), 500
