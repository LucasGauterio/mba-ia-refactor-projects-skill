from src.config.database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import hashlib

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password,
            'role': self.role,
            'active': self.active,
            'created_at': str(self.created_at)
        }

    def set_password(self, pwd):
        # Utiliza pbkdf2 seguro por padrão
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        # Suporta verificação de hashes MD5 antigos para retrocompatibilidade
        # se o hash salvo tiver tamanho 32 (MD5 hexdigest possui 32 caracteres)
        if len(self.password) == 32:
            return self.password == hashlib.md5(pwd.encode()).hexdigest()
        return check_password_hash(self.password, pwd)

    def is_admin(self):
        return self.role == 'admin'
