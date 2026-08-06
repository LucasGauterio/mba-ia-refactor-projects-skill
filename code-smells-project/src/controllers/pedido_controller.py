from flask import request, jsonify
from src.models import pedido as pedido_model
from src.config.settings import STATUS_PEDIDO_VALIDOS

def criar_pedido():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400

    usuario_id = dados.get("usuario_id")
    itens = dados.get("itens", [])

    if not usuario_id:
        return jsonify({"erro": "Usuario ID é obrigatório", "sucesso": False}), 400
    if not itens or len(itens) == 0:
        return jsonify({"erro": "Pedido deve ter pelo menos 1 item", "sucesso": False}), 400

    resultado = pedido_model.criar_pedido(usuario_id, itens)

    if "erro" in resultado:
        return jsonify({"erro": resultado["erro"], "sucesso": False}), 400

    # Lógica de notificação simulada original (logs)
    print(f"ENVIANDO EMAIL: Pedido {resultado['pedido_id']} criado para usuario {usuario_id}")
    print("ENVIANDO SMS: Seu pedido foi recebido!")
    print("ENVIANDO PUSH: Novo pedido recebido pelo sistema")

    return jsonify({
        "dados": resultado,
        "sucesso": True,
        "mensagem": "Pedido criado com sucesso"
    }), 201

def listar_pedidos_usuario(usuario_id):
    pedidos = pedido_model.get_pedidos_usuario(usuario_id)
    return jsonify({"dados": pedidos, "sucesso": True}), 200

def listar_todos_pedidos():
    pedidos = pedido_model.get_todos_pedidos()
    return jsonify({"dados": pedidos, "sucesso": True}), 200

def atualizar_status_pedido(pedido_id):
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400
        
    novo_status = dados.get("status", "")

    if novo_status not in STATUS_PEDIDO_VALIDOS:
        return jsonify({"erro": "Status inválido", "sucesso": False}), 400

    pedido_model.atualizar_status_pedido(pedido_id, novo_status)

    if novo_status == "aprovado":
        print(f"NOTIFICAÇÃO: Pedido {pedido_id} foi aprovado! Preparar envio.")
    elif novo_status == "cancelado":
        print(f"NOTIFICAÇÃO: Pedido {pedido_id} cancelado. Devolver estoque.")

    return jsonify({"sucesso": True, "mensagem": "Status atualizado"}), 200
