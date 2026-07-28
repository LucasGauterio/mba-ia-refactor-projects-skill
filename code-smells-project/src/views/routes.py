from flask import jsonify, request
import src.controllers as controllers
from src.config.database import get_db

def register_routes(app):
    """
    Mapeia todos os endpoints HTTP às respectivas funções do controlador no padrão MVC.
    """
    # Rotas de Produtos
    app.add_url_rule("/produtos", "listar_produtos", controllers.listar_produtos, methods=["GET"])
    app.add_url_rule("/produtos/busca", "buscar_produtos", controllers.buscar_produtos, methods=["GET"])
    app.add_url_rule("/produtos/<int:id>", "buscar_produto", controllers.buscar_produto, methods=["GET"])
    app.add_url_rule("/produtos", "criar_produto", controllers.criar_produto, methods=["POST"])
    app.add_url_rule("/produtos/<int:id>", "atualizar_produto", controllers.atualizar_produto, methods=["PUT"])
    app.add_url_rule("/produtos/<int:id>", "deletar_produto", controllers.deletar_produto, methods=["DELETE"])

    # Rotas de Usuários e Autenticação
    app.add_url_rule("/usuarios", "listar_usuarios", controllers.listar_usuarios, methods=["GET"])
    app.add_url_rule("/usuarios/<int:id>", "buscar_usuario", controllers.buscar_usuario, methods=["GET"])
    app.add_url_rule("/usuarios", "criar_usuario", controllers.criar_usuario, methods=["POST"])
    app.add_url_rule("/login", "login", controllers.login, methods=["POST"])

    # Rotas de Pedidos
    app.add_url_rule("/pedidos", "criar_pedido", controllers.criar_pedido, methods=["POST"])
    app.add_url_rule("/pedidos", "listar_todos_pedidos", controllers.listar_todos_pedidos, methods=["GET"])
    app.add_url_rule("/pedidos/usuario/<int:usuario_id>", "listar_pedidos_usuario", controllers.listar_pedidos_usuario, methods=["GET"])
    app.add_url_rule("/pedidos/<int:pedido_id>/status", "atualizar_status_pedido", controllers.atualizar_status_pedido, methods=["PUT"])

    # Rota de Relatório de Vendas
    app.add_url_rule("/relatorios/vendas", "relatorio_vendas", controllers.relatorio_vendas, methods=["GET"])

    # Rota de Health Check
    app.add_url_rule("/health", "health_check", controllers.health_check, methods=["GET"])

    # Página Inicial (Index / Welcome)
    @app.route("/")
    def index():
        return jsonify({
            "mensagem": "Bem-vindo à API da Loja",
            "versao": "1.0.0",
            "endpoints": {
                "produtos": "/produtos",
                "usuarios": "/usuarios",
                "pedidos": "/pedidos",
                "login": "/login",
                "relatorios": "/relatorios/vendas",
                "health": "/health"
            }
        })

    # Rota de Administração: Reset do Banco de Dados
    @app.route("/admin/reset-db", methods=["POST"])
    def reset_database():
        # Validação de segurança conforme playbook_refatoracao.md
        auth_header = request.headers.get("Authorization")
        if not auth_header or auth_header != "Bearer admin-token-123":
            return jsonify({
                "erro": "Acesso não autorizado. Token administrativo ausente ou inválido.",
                "sucesso": False
            }), 401

        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM itens_pedido")
        cursor.execute("DELETE FROM pedidos")
        cursor.execute("DELETE FROM produtos")
        cursor.execute("DELETE FROM usuarios")
        db.commit()
        print("!!! BANCO DE DADOS RESETADO !!!")
        return jsonify({"mensagem": "Banco de dados resetado", "sucesso": True}), 200
        
    # A Rota '/admin/query' (backdoor de SQL Injection direto) foi COMPLETAMENTE REMOVIDA.
