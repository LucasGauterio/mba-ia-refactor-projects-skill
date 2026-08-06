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

    # Relacionamento com tarefas usando cascade para deletar tarefas órfãs
    tasks = db.relationship('Task', back_populates='user', cascade="all, delete-orphan")

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
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        if check_password_hash(self.password, pwd):
            return True
        
        # Fallback de compatibilidade para hash MD5 legado
        md5_hash = hashlib.md5(pwd.encode()).hexdigest()
        if self.password == md5_hash:
            # Migra o hash legado para o novo hash seguro
            self.set_password(pwd)
            try:
                db.session.commit()
            except Exception:
                pass
            return True
        return False

    def is_admin(self):
        return self.role == 'admin'
