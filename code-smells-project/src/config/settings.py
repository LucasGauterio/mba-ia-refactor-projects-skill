import os

def load_dotenv():
    # Encontra o arquivo .env no diretório raiz do projeto
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    env_path = os.path.join(base_dir, ".env")
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    if "=" in line:
                        key, val = line.split("=", 1)
                        os.environ[key.strip()] = val.strip()

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações do Flask
SECRET_KEY = os.getenv("SECRET_KEY", "chave-fallback-segura-desenvolvimento-mvc-1234")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "False").lower() in ("true", "1", "t")
PORT = int(os.getenv("PORT", 5000))

# Configurações do Banco de Dados
DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")

# Segurança
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin-token-secreto-123")

# Constantes de Domínio - Status de Pedido
STATUS_PENDENTE = "pendente"
STATUS_APROVADO = "aprovado"
STATUS_ENVIADO = "enviado"
STATUS_ENTREGUE = "entregue"
STATUS_CANCELADO = "cancelado"

STATUS_VALIDOS = [
    STATUS_PENDENTE,
    STATUS_APROVADO,
    STATUS_ENVIADO,
    STATUS_ENTREGUE,
    STATUS_CANCELADO
]

# Constantes de Domínio - Tipos de Usuário
TIPO_CLIENTE = "cliente"
TIPO_ADMIN = "admin"
TIPOS_USUARIO = [TIPO_CLIENTE, TIPO_ADMIN]

# Constantes de Domínio - Categorias de Produto
CATEGORIAS_VALIDAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]
