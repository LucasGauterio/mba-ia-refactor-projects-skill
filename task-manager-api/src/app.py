from flask import Flask
from flask_cors import CORS
from src.config.database import db
from src.config.settings import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from src.routes.task_routes import task_bp
from src.routes.user_routes import user_bp
from src.routes.category_routes import category_bp
from src.routes.report_routes import report_bp
from src.middlewares.error_handler import register_error_handlers
import datetime

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

    CORS(app)
    db.init_app(app)

    # Registro de blueprints das rotas
    app.register_blueprint(task_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(report_bp)

    # Registro do tratador centralizado de erros
    register_error_handlers(app)

    @app.route('/health')
    def health():
        return {'status': 'ok', 'timestamp': str(datetime.datetime.now())}

    @app.route('/')
    def index():
        return {'message': 'Task Manager API', 'version': '1.0'}

    return app

# Expõe objeto app para servidores WSGI/Gunicorn e compatibilidade geral
app = create_app()
