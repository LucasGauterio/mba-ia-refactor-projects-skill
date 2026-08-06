from flask import Flask
from flask_cors import CORS
from src.config.database import db
from src.config import settings
from src.routes.task_routes import task_bp
from src.routes.user_routes import user_bp
from src.routes.report_routes import report_bp
from src.routes.category_routes import category_bp
from src.middlewares.error_handler import register_error_handlers
import datetime

# Inicialização da aplicação Flask
app = Flask(__name__)

# Configurações a partir do settings centralizado
app.config['SQLALCHEMY_DATABASE_URI'] = settings.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = settings.SECRET_KEY

# Ativação do CORS
CORS(app)

# Inicialização do banco de dados
db.init_app(app)

# Registro dos tratadores globais de erro (Middleware)
register_error_handlers(app)

# Registro de Blueprints de rotas organizadas por domínios
app.register_blueprint(task_bp)
app.register_blueprint(user_bp)
app.register_blueprint(report_bp)
app.register_blueprint(category_bp)

@app.route('/health')
def health():
    return {'status': 'ok', 'timestamp': str(datetime.datetime.now())}

@app.route('/')
def index():
    return {'message': 'Task Manager API', 'version': '1.0'}
