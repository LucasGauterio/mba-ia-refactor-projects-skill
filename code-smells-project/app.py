# root app.py wrapper
from src.app import app
from src.config.settings import PORT, FLASK_DEBUG

if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO (ROOT WRAPPER)")
    print(f"Rodando em http://localhost:{PORT}")
    print("=" * 50)
    app.run(host="0.0.0.0", port=PORT, debug=FLASK_DEBUG)
