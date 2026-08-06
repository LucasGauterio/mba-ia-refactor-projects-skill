import os

# Carregar variáveis do arquivo .env manualmente para evitar dependências extras
if os.path.exists(".env"):
    with open(".env", "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, val = line.split("=", 1)
                os.environ[key.strip()] = val.strip()

from src.app import create_app
from src.config.settings import PORT, FLASK_DEBUG

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO (MVC)")
    print(f"Rodando em http://localhost:{PORT}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=FLASK_DEBUG)
