from src.config.database import get_db
from werkzeug.security import generate_password_hash, check_password_hash

def get_todos_usuarios():
    """Busca todos os usuários cadastrados."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        result.append({
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "senha": row["senha"],
            "tipo": row["tipo"],
            "criado_em": row["criado_em"]
        })
    return result

def get_usuario_por_id(id):
    """Busca um usuário específico por ID."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE id = ?", (id,))
    row = cursor.fetchone()
    if row:
        return {
            "id": row["id"],
            "nome": row["nome"],
            "email": row["email"],
            "senha": row["senha"],
            "tipo": row["tipo"],
            "criado_em": row["criado_em"]
        }
    return None

def login_usuario(email, senha):
    """Valida o login de um usuário autenticando seu e-mail e conferindo o hash da senha."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (email,))
    row = cursor.fetchone()
    if row:
        hashed_password = row["senha"]
        if check_password_hash(hashed_password, senha):
            return {
                "id": row["id"],
                "nome": row["nome"],
                "email": row["email"],
                "tipo": row["tipo"]
            }
    return None

def criar_usuario(nome, email, senha, tipo="cliente"):
    """Cria um novo usuário salvando um hash pbkdf2 seguro de sua senha."""
    db = get_db()
    cursor = db.cursor()
    hashed_password = generate_password_hash(senha)
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
        (nome, email, hashed_password, tipo)
    )
    db.commit()
    return cursor.lastrowid
