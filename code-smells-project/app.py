from src.app import create_app
from src.config.settings import PORT, FLASK_DEBUG

app = create_app()

if __name__ == "__main__":
    print("=" * 50)
    print("SERVIDOR INICIADO (MVC REFACTOR)")
    print(f"Rodando em http://localhost:{PORT}")
    print("=" * 50)
    
    app.run(host="0.0.0.0", port=PORT, debug=FLASK_DEBUG)
