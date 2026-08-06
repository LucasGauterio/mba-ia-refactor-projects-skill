import os
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env se ele existir
load_dotenv()

PORT = int(os.getenv("PORT", 5000))
DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-123")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///tasks.db")

# SMTP Settings
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER", "taskmanager@gmail.com")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "senha123")
