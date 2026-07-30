import os
import sys

# Garante que a raiz do projeto esteja no python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.app import app
from src.config.database import db
from src.config.settings import PORT, DEBUG

if __name__ == '__main__':
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)
