import sqlite3
from flask import g
from werkzeug.security import generate_password_hash
from src.config.settings import DATABASE_PATH

def get_db():
    """Retorna uma conexão com o SQLite exclusiva para o contexto da requisição atual."""
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """Fecha a conexão do SQLite do contexto da requisição atual, se houver."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    """Inicializa a estrutura do banco de dados e executa sementes (seeds) seguras."""
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Criação das tabelas caso não existam
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            descricao TEXT,
            preco REAL,
            estoque INTEGER,
            categoria TEXT,
            ativo INTEGER DEFAULT 1,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            email TEXT,
            senha TEXT,
            tipo TEXT DEFAULT 'cliente',
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER,
            status TEXT DEFAULT 'pendente',
            total REAL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER,
            produto_id INTEGER,
            quantidade INTEGER,
            preco_unitario REAL
        )
    """)
    conn.commit()

    # Seed de Produtos
    cursor.execute("SELECT COUNT(*) FROM produtos")
    if cursor.fetchone()[0] == 0:
        produtos = [
            ("Notebook Gamer", "Notebook potente para jogos", 5999.99, 10, "informatica"),
            ("Mouse Wireless", "Mouse sem fio ergonômico", 89.90, 50, "informatica"),
            ("Teclado Mecânico", "Teclado mecânico RGB", 299.90, 30, "informatica"),
            ("Monitor 27''", "Monitor 27 polegadas 144hz", 1899.90, 15, "informatica"),
            ("Headset Gamer", "Headset com microfone", 199.90, 25, "informatica"),
            ("Cadeira Gamer", "Cadeira ergonômica", 1299.90, 8, "moveis"),
            ("Webcam HD", "Webcam 1080p", 249.90, 20, "informatica"),
            ("Hub USB", "Hub USB 3.0 7 portas", 79.90, 40, "informatica"),
            ("SSD 1TB", "SSD NVMe 1TB", 449.90, 35, "informatica"),
            ("Camiseta Dev", "Camiseta estampa código", 59.90, 100, "vestuario"),
        ]
        cursor.executemany(
            "INSERT INTO produtos (nome, descricao, preco, estoque, categoria) VALUES (?, ?, ?, ?, ?)",
            produtos
        )
        conn.commit()

    # Seed de Usuários (com senhas criptografadas por hash seguro pbkdf2)
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        usuarios = [
            ("Admin", "admin@loja.com", generate_password_hash("admin123"), "admin"),
            ("João Silva", "joao@email.com", generate_password_hash("123456"), "cliente"),
            ("Maria Santos", "maria@email.com", generate_password_hash("senha123"), "cliente"),
        ]
        cursor.executemany(
            "INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
            usuarios
        )
        conn.commit()
    else:
        # Migração segura para senhas legadas que ainda estejam em texto plano
        cursor.execute("SELECT id, senha FROM usuarios")
        usuarios_existentes = cursor.fetchall()
        for row in usuarios_existentes:
            u_id = row["id"]
            u_senha = row["senha"]
            # Werkzeug hashes começam tipicamente com padrões como pbkdf2:, scrypt:, etc.
            if not u_senha.startswith(('pbkdf2:', 'scrypt:', 'bcrypt:', 'argon2:')):
                hashed_senha = generate_password_hash(u_senha)
                cursor.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (hashed_senha, u_id))
        conn.commit()

    conn.close()
