import os

# Configurações do Servidor
SECRET_KEY = os.getenv("SECRET_KEY", "minha-chave-super-secreta-123")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() in ("true", "1", "t")
PORT = int(os.getenv("PORT", 5000))

# Configurações do Banco de Dados
DATABASE_PATH = os.getenv("DATABASE_PATH", "loja.db")

# Chave de Acesso para Rota Administrativa /admin/reset-db
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "admin-token-secreto-123")

# Constantes de Domínio
STATUS_PEDIDO_PENDENTE = "pendente"
STATUS_PEDIDO_APROVADO = "aprovado"
STATUS_PEDIDO_ENVIADO = "enviado"
STATUS_PEDIDO_ENTREGUE = "entregue"
STATUS_PEDIDO_CANCELADO = "cancelado"

STATUS_PEDIDO_VALIDOS = [
    STATUS_PEDIDO_PENDENTE,
    STATUS_PEDIDO_APROVADO,
    STATUS_PEDIDO_ENVIADO,
    STATUS_PEDIDO_ENTREGUE,
    STATUS_PEDIDO_CANCELADO
]

CATEGORIAS_VALIDAS = ["informatica", "moveis", "vestuario", "geral", "eletronicos", "livros"]

TIPO_USUARIO_CLIENTE = "cliente"
TIPO_USUARIO_ADMIN = "admin"
TIPOS_USUARIO_VALIDOS = [TIPO_USUARIO_CLIENTE, TIPO_USUARIO_ADMIN]
