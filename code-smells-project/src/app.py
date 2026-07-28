from flask import Flask
from flask_cors import CORS
from src.config.settings import SECRET_KEY, FLASK_DEBUG
from src.config.database import init_db
from src.views.routes import register_routes
from src.middlewares.error_handler import register_error_handlers

def create_app():
    """
    Inicializa a aplicação Flask aplicando configurações de ambiente, CORS,
    rotas e middlewares de erro centralizados.
    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = FLASK_DEBUG
    
    # Ativa CORS na aplicação
    CORS(app)
    
    # Registra o tratador global de exceções
    register_error_handlers(app)
    
    # Registra todas as rotas da aplicação
    register_routes(app)
    
    # Garante a inicialização do banco de dados na inicialização da aplicação
    init_db()
    
    return app
