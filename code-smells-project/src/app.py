from flask import Flask
from flask_cors import CORS
from src.config.settings import SECRET_KEY, FLASK_DEBUG, PORT
from src.config.database import init_db, close_db
from src.middlewares.error_handler import register_error_handlers

# Import Blueprints das Rotas
from src.routes.produto_routes import produto_bp
from src.routes.usuario_routes import usuario_bp
from src.routes.pedido_routes import pedido_bp
from src.routes.relatorio_routes import relatorio_bp
from src.routes.general_routes import general_bp

def create_app():
    # Inicializa o banco de dados e aplica as migrações necessárias no startup
    init_db()

    app = Flask(__name__)
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["DEBUG"] = FLASK_DEBUG
    CORS(app)

    # Associa a desconexão automática do banco ao ciclo de vida da requisição
    app.teardown_appcontext(close_db)

    # Registra o middleware global de tratamento de exceções
    register_error_handlers(app)

    # Registra as rotas mapeadas por Blueprints
    app.register_blueprint(produto_bp)
    app.register_blueprint(usuario_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(relatorio_bp)
    app.register_blueprint(general_bp)

    return app

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO")
    print(f"Rodando em http://localhost:{PORT}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=FLASK_DEBUG)
