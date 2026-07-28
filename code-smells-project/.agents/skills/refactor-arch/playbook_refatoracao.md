# Playbook de Refatoração

Este playbook fornece receitas de refatoração para corrigir os anti-patterns catalogados.

---

## 1. SQL Injection para Consultas Parametrizadas

### Antes (Python)
```python
cursor.execute("SELECT * FROM produtos WHERE id = " + str(id))
```
### Depois (Python)
```python
cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
```

### Antes (Node.js)
```javascript
db.get(`SELECT * FROM users WHERE email = '${email}'`, (err, row) => { ... });
```
### Depois (Node.js)
```javascript
db.get("SELECT * FROM users WHERE email = ?", [email], (err, row) => { ... });
```

---

## 2. Hash MD5/Inseguro para Criptografia Segura com Salt

### Antes (Python MD5)
```python
def set_password(self, pwd):
    self.password = hashlib.md5(pwd.encode()).hexdigest()
```
### Depois (Python pbkdf2 com salt seguro)
```python
from werkzeug.security import generate_password_hash, check_password_hash

def set_password(self, pwd):
    self.password = generate_password_hash(pwd)

def check_password(self, pwd):
    return check_password_hash(self.password, pwd)
```

### Antes (Node.js badCrypto)
```javascript
function badCrypto(pwd) {
    let hash = "";
    for(let i = 0; i < 10000; i++) {
        hash += Buffer.from(pwd).toString('base64').substring(0, 2);
    }
    return hash.substring(0, 10);
}
```
### Depois (Node.js PBKDF2 ou bcrypt nativo)
```javascript
const crypto = require('crypto');

function hashPassword(pwd) {
    const salt = crypto.randomBytes(16).toString('hex');
    const hash = crypto.pbkdf2Sync(pwd, salt, 100000, 64, 'sha512').toString('hex');
    return `${salt}:${hash}`;
}

function checkPassword(pwd, savedPassword) {
    const [salt, hash] = savedPassword.split(':');
    const checkHash = crypto.pbkdf2Sync(pwd, salt, 100000, 64, 'sha512').toString('hex');
    return hash === checkHash;
}
```

---

## 3. Credenciais Hardcoded para Variáveis de Ambiente

### Antes (Python)
```python
app.config["SECRET_KEY"] = "minha-chave-super-secreta-123"
```
### Depois (Python)
```python
import os
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "chave-fallback-segura-desenvolvimento")
```

### Antes (Node.js)
```javascript
const config = {
    paymentGatewayKey: "pk_live_1234567890abcdef"
};
```
### Depois (Node.js)
```javascript
const config = {
    paymentGatewayKey: process.env.PAYMENT_GATEWAY_KEY || "pk_test_fallback"
};
```

---

## 4. Remoção de Endpoints de Backdoor Admin / Falta de Autenticação

### Antes
```python
@app.route("/admin/query", methods=["POST"])
def executar_query():
    query = request.json.get("sql")
    cursor.execute(query) # EXECUTA SQL LIVRE
```
### Depois
- **Remover completamente** a rota `/admin/query`. Para rotas administrativas cruciais como `/admin/reset-db` e `/api/admin/financial-report`, implementar validação de tokens administrativos recebidos em headers (ex: `Authorization: Bearer <token>`).

---

## 5. Eliminação de Queries N+1 para Joins Otimizados

### Antes (Python SQLAlchemy loop N+1)
```python
tasks = Task.query.all()
for t in tasks:
    user = User.query.get(t.user_id) # Query executada N vezes!
```
### Depois (SQLAlchemy joinedload)
```python
from sqlalchemy.orm import joinedload
tasks = Task.query.options(joinedload(Task.user)).all()
# Acessar t.user agora não gera novas queries!
```

### Antes (SQL puro loop N+1)
```python
cursor.execute("SELECT * FROM pedidos")
pedidos = cursor.fetchall()
for p in pedidos:
    cursor.execute("SELECT * FROM itens_pedido WHERE pedido_id = " + str(p['id'])) # N queries!
```
### Depois (SQL com JOIN estruturado)
```python
cursor.execute("""
    SELECT p.id as pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
           i.produto_id, i.quantidade, i.preco_unitario, prod.nome as produto_nome
    FROM pedidos p
    LEFT JOIN itens_pedido i ON p.id = i.pedido_id
    LEFT JOIN produtos prod ON i.produto_id = prod.id
""")
rows = cursor.fetchall()
# Agrupar rows em dicionários por pedido no python (Single Query!)
```

---

## 6. Correção de Estado Global Mutável para Persistência ou Escopo Seguro

### Antes
```javascript
let totalRevenue = 0;
// No endpoint:
totalRevenue += payment.amount;
```
### Depois
- No Express/Node.js, migrar o banco em memória `:memory:` para arquivo persistente SQLite. Ler o faturamento calculando por meio de funções agregadoras diretamente do Banco de Dados no momento da requisição:
```javascript
db.get("SELECT SUM(amount) AS total FROM payments WHERE status = 'PAID'", [], (err, row) => {
    const totalRevenue = row.total || 0;
});
```

---

## 7. Limpeza de Matrículas e Chaves Órfãs (Cascade Delete)

### Antes
```javascript
app.delete('/api/users/:id', (req, res) => {
    db.run("DELETE FROM users WHERE id = ?", [id]); // Deixa enrollments órfãos
});
```
### Depois (Limpeza Manual no SQLite com constraints ativas)
```javascript
app.delete('/api/users/:id', (req, res) => {
    db.serialize(() => {
        db.run("DELETE FROM payments WHERE enrollment_id IN (SELECT id FROM enrollments WHERE user_id = ?)", [id]);
        db.run("DELETE FROM enrollments WHERE user_id = ?", [id]);
        db.run("DELETE FROM users WHERE id = ?", [id], (err) => {
            res.status(200).send("Usuário e todas as relações removidos com sucesso.");
        });
    });
});
```

---

## 8. Tratamento Centralizado de Erros (Middleware)

### Antes
```python
def listar_produtos():
    try:
        ...
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
```
### Depois (Python Decorator Global)
```python
@app.errorhandler(Exception)
def handle_exception(e):
    # Logar erro internamente
    print(f"Erro inesperado: {str(e)}")
    return jsonify({"erro": "Ocorreu um erro interno no servidor"}), 500
```

---

## 9. SQLite Thread-Safe Connection (Isolamento por Request Context)

### Antes (Python - Conexão Global Única)
```python
conn = sqlite3.connect("database.db", check_same_thread=False) # Inseguro
```
### Depois (Python - Usando `flask.g` para obter uma conexão por requisição)
```python
from flask import g
import sqlite3

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("database.db")
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()
```

---

## 10. Atomicidade de Transações (Rollback e Atômico)

### Antes (Python - Múltiplas inserções sem transação)
```python
cursor.execute("INSERT INTO pedidos ...")
cursor.execute("UPDATE estoque ...") # Se falhar aqui, o insert acima persiste erroneamente!
conn.commit()
```
### Depois (Python - Transação segura)
```python
conn = get_db()
cursor = conn.cursor()
try:
    cursor.execute("BEGIN TRANSACTION;")
    cursor.execute("INSERT INTO pedidos ...")
    cursor.execute("UPDATE estoque ...")
    conn.commit()
except Exception as e:
    conn.rollback() # Restaura o estado anterior do banco em caso de erros
    raise e
```

### Antes (Node.js - Múltiplas inserções assíncronas soltas)
```javascript
db.run("INSERT INTO enrollments ...", (err) => {
    db.run("INSERT INTO payments ...", (err) => { ... });
});
```
### Depois (Node.js - Transação sequencial serializada)
```javascript
db.serialize(() => {
    db.run("BEGIN TRANSACTION");
    db.run("INSERT INTO enrollments ...", function(err) {
        if (err) {
            db.run("ROLLBACK");
            return;
        }
        db.run("INSERT INTO payments ...", function(err) {
            if (err) {
                db.run("ROLLBACK");
                return;
            }
            db.run("COMMIT");
        });
    });
});
```

