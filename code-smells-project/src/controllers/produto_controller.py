from flask import request, jsonify
from src.models import produto as produto_model
from src.config.settings import CATEGORIAS_VALIDAS

def listar_produtos():
    produtos = produto_model.get_todos_produtos()
    return jsonify({"dados": produtos, "sucesso": True}), 200

def buscar_produto(id):
    produto = produto_model.get_produto_por_id(id)
    if produto:
        return jsonify({"dados": produto, "sucesso": True}), 200
    else:
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404

def criar_produto():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400
    if "nome" not in dados:
        return jsonify({"erro": "Nome é obrigatório", "sucesso": False}), 400
    if "preco" not in dados:
        return jsonify({"erro": "Preço é obrigatório", "sucesso": False}), 400
    if "estoque" not in dados:
        return jsonify({"erro": "Estoque é obrigatório", "sucesso": False}), 400

    nome = dados["nome"]
    descricao = dados.get("descricao", "")
    preco = dados["preco"]
    estoque = dados["estoque"]
    categoria = dados.get("categoria", "geral")

    if preco < 0:
        return jsonify({"erro": "Preço não pode ser negativo", "sucesso": False}), 400
    if estoque < 0:
        return jsonify({"erro": "Estoque não pode ser negativo", "sucesso": False}), 400
    if len(nome) < 2:
        return jsonify({"erro": "Nome muito curto", "sucesso": False}), 400
    if len(nome) > 200:
        return jsonify({"erro": "Nome muito longo", "sucesso": False}), 400

    if categoria not in CATEGORIAS_VALIDAS:
        return jsonify({"erro": f"Categoria inválida. Válidas: {str(CATEGORIAS_VALIDAS)}", "sucesso": False}), 400

    id = produto_model.criar_produto(nome, descricao, preco, estoque, categoria)
    return jsonify({"dados": {"id": id}, "sucesso": True, "mensagem": "Produto criado"}), 201

def atualizar_produto(id):
    dados = request.get_json()
    produto_existente = produto_model.get_produto_por_id(id)
    if not produto_existente:
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404

    if not dados:
        return jsonify({"erro": "Dados inválidos", "sucesso": False}), 400
    if "nome" not in dados:
        return jsonify({"erro": "Nome é obrigatório", "sucesso": False}), 400
    if "preco" not in dados:
        return jsonify({"erro": "Preço é obrigatório", "sucesso": False}), 400
    if "estoque" not in dados:
        return jsonify({"erro": "Estoque é obrigatório", "sucesso": False}), 400

    nome = dados["nome"]
    descricao = dados.get("descricao", "")
    preco = dados["preco"]
    estoque = dados["estoque"]
    categoria = dados.get("categoria", "geral")

    if preco < 0:
        return jsonify({"erro": "Preço não pode ser negativo", "sucesso": False}), 400
    if estoque < 0:
        return jsonify({"erro": "Estoque não pode ser negativo", "sucesso": False}), 400

    produto_model.atualizar_produto(id, nome, descricao, preco, estoque, categoria)
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

def deletar_produto(id):
    produto = produto_model.get_produto_por_id(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404

    produto_model.deletar_produto(id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200

def buscar_produtos():
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria", None)
    preco_min = request.args.get("preco_min", None)
    preco_max = request.args.get("preco_max", None)

    if preco_min:
        preco_min = float(preco_min)
    if preco_max:
        preco_max = float(preco_max)

    resultados = produto_model.buscar_produtos(termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
