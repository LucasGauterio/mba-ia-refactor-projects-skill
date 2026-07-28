from flask import request, jsonify
import src.models as models
from src.config.database import get_db

def criar_pedido():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    usuario_id = dados.get("usuario_id")
    itens = dados.get("itens", [])

    if not usuario_id:
        return jsonify({"erro": "Usuario ID é obrigatório"}), 400
    if not itens or len(itens) == 0:
        return jsonify({"erro": "Pedido deve ter pelo menos 1 item"}), 400

    resultado = models.criar_pedido(usuario_id, itens)

    if "erro" in resultado:
        return jsonify({"erro": resultado["erro"], "sucesso": False}), 400

    print(f"ENVIANDO EMAIL: Pedido {resultado['pedido_id']} criado para usuario {usuario_id}")
    print("ENVIANDO SMS: Seu pedido foi recebido!")
    print("ENVIANDO PUSH: Novo pedido recebido pelo sistema")

    return jsonify({
        "dados": resultado,
        "sucesso": True,
        "mensagem": "Pedido criado com sucesso"
    }), 201

def listar_pedidos_usuario(usuario_id):
    pedidos = models.get_pedidos_usuario(usuario_id)
    return jsonify({"dados": pedidos, "sucesso": True}), 200

def listar_todos_pedidos():
    pedidos = models.get_todos_pedidos()
    return jsonify({"dados": pedidos, "sucesso": True}), 200

def atualizar_status_pedido(pedido_id):
    dados = request.get_json()
    novo_status = dados.get("status", "")

    if novo_status not in ["pendente", "aprovado", "enviado", "entregue", "cancelado"]:
        return jsonify({"erro": "Status inválido"}), 400

    models.atualizar_status_pedido(pedido_id, novo_status)

    if novo_status == "aprovado":
        print(f"NOTIFICAÇÃO: Pedido {pedido_id} foi aprovado! Preparar envio.")
    elif novo_status == "cancelado":
        print(f"NOTIFICAÇÃO: Pedido {pedido_id} cancelado. Devolver estoque.")

    return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200

def relatorio_vendas():
    relatorio = models.relatorio_vendas()
    return jsonify({"dados": relatorio, "sucesso": True}), 200

def health_check():
    # Coleta contadores e estatísticas de forma segura do banco
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT 1")
    
    cursor.execute("SELECT COUNT(*) FROM produtos")
    produtos = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    usuarios = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM pedidos")
    pedidos = cursor.fetchone()[0]

    return jsonify({
        "status": "ok",
        "database": "connected",
        "counts": {
            "produtos": produtos,
            "usuarios": usuarios,
            "pedidos": pedidos
        },
        "versao": "1.0.0",
        "ambiente": "producao",
        "db_path": "[REDACTED]",
        "debug": False,
        "secret_key": "[REDACTED]"
    }), 200
