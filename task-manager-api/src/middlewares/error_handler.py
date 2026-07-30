from flask import jsonify

def handle_exception(e):
    # Log da exceção real de forma segura no console do servidor
    print(f"Erro inesperado capturado: {str(e)}")
    return jsonify({"error": "Ocorreu um erro interno no servidor"}), 500

def register_error_handlers(app):
    app.register_error_handler(Exception, handle_exception)
