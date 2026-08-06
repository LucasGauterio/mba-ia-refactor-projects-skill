import os
from src.app import app
from src.config import settings

if __name__ == '__main__':
    # Inicializa o servidor web Flask lendo as configurações parametrizadas
    app.run(host='0.0.0.0', port=settings.PORT, debug=settings.DEBUG)
