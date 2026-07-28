import os

# Função simples para carregar variáveis de um arquivo .env se ele existir
def load_env(env_path=".env"):
    if os.path.exists(env_path):
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, val = line.split("=", 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    os.environ[key] = val

# Carrega as variáveis de ambiente locais
load_env()

# Configurações globais expostas
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-seguro-desenvolvimento-123456789")
DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "yes")
PORT = int(os.getenv("PORT", "5000"))
