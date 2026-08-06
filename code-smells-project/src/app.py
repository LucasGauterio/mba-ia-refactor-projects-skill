from flask import Flask
from flask_cors import CORS
from src.config.settings import SECRET_KEY, FLASK_DEBUG
from src.config.database import init_db
from src.middlewares.error_handler import register_error_handlers

from src.routes.general_routes import general_bp
from src.routes.produto_routes import produto_bp
from src.routes.usuario_routes import usuario_bp
from src.routes.pedido_routes import pedido_bp
from src.routes.relatorio_routes import relatorio_bp

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = FLASK_DEBUG

    CORS(app)

    # Inicializar banco de dados (tabelas e seeds)
    init_db(app)

    # Registrar tratador global de exceções
    register_error_handlers(app)

    # Registrar Blueprints das rotas
    app.register_blueprint(general_bp)
    app.register_blueprint(produto_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(relatorio_bp)

    return app
