from flask import jsonify
from werkzeug.exceptions import HTTPException
import traceback

def register_error_handlers(app):
    @app.errorhandler(Exception)
    def handle_exception(e):
        # Loga o erro internamente com stack trace completo para depuração
        print(f"Erro capturado pelo handler global: {str(e)}")
        traceback.print_exc()
        
        # Retorna o status HTTP correto se for um erro padrão do Flask/Werkzeug
        if isinstance(e, HTTPException):
            return jsonify({"error": e.description}), e.code
            
        # Caso contrário, retorna um erro interno genérico para não vazar detalhes internos
        return jsonify({"error": "Ocorreu um erro interno no servidor"}), 500
