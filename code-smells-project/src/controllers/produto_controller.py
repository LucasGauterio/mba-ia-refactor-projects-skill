from flask import request, jsonify
import src.models.produto as produto_model
from src.config.settings import CATEGORIAS_VALIDAS

def listar_produtos():
    """Busca e retorna a lista de todos os produtos."""
    produtos = produto_model.get_todos_produtos()
    return jsonify({"dados": produtos, "sucesso": True}), 200

def buscar_produto(id):
    """Busca um produto específico pelo ID e trata caso não exista."""
    produto = produto_model.get_produto_por_id(id)
    if produto:
        return jsonify({"dados": produto, "sucesso": True}), 200
    return jsonify({"erro": "Produto não encontrado", "sucesso": False}), 404

def criar_produto():
    """Valida e cria um novo produto."""
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400
    
    # Validações estruturais obrigatórias
    if "nome" not in dados or "preco" not in dados or "estoque" not in dados:
        return jsonify({"erro": "Nome, preço e estoque são obrigatórios"}), 400

    nome = dados["nome"]
    descricao = dados.get("descricao", "")
    preco = dados["preco"]
    estoque = dados["estoque"]
    categoria = dados.get("categoria", "geral")

    # Validações de limites e tipos de dados
    if preco < 0:
        return jsonify({"erro": "Preço não pode ser negativo"}), 400
    if estoque < 0:
        return jsonify({"erro": "Estoque não pode ser negativo"}), 400
    if len(nome) < 2:
        return jsonify({"erro": "Nome muito curto"}), 400
    if len(nome) > 200:
        return jsonify({"erro": "Nome muito longo"}), 400

    if categoria not in CATEGORIAS_VALIDAS:
        return jsonify({"erro": f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}"}), 400

    id = produto_model.criar_produto(nome, descricao, preco, estoque, categoria)
    return jsonify({"dados": {"id": id}, "sucesso": True, "mensagem": "Produto criado"}), 201

def atualizar_produto(id):
    """Atualiza os campos de um produto existente após validações."""
    dados = request.get_json()
    produto_existente = produto_model.get_produto_por_id(id)
    if not produto_existente:
        return jsonify({"erro": "Produto não encontrado"}), 404

    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400
    if "nome" not in dados or "preco" not in dados or "estoque" not in dados:
        return jsonify({"erro": "Nome, preço e estoque são obrigatórios"}), 400

    nome = dados["nome"]
    descricao = dados.get("descricao", "")
    preco = dados["preco"]
    estoque = dados["estoque"]
    categoria = dados.get("categoria", "geral")

    if preco < 0:
        return jsonify({"erro": "Preço não pode ser negativo"}), 400
    if estoque < 0:
        return jsonify({"erro": "Estoque não pode ser negativo"}), 400

    if categoria not in CATEGORIAS_VALIDAS:
        return jsonify({"erro": f"Categoria inválida. Válidas: {CATEGORIAS_VALIDAS}"}), 400

    produto_model.atualizar_produto(id, nome, descricao, preco, estoque, categoria)
    return jsonify({"sucesso": True, "mensagem": "Produto atualizado"}), 200

def deletar_produto(id):
    """Exclui um produto cadastrado."""
    produto = produto_model.get_produto_por_id(id)
    if not produto:
        return jsonify({"erro": "Produto não encontrado"}), 404

    produto_model.deletar_produto(id)
    return jsonify({"sucesso": True, "mensagem": "Produto deletado"}), 200

def buscar_produtos():
    """Busca produtos utilizando critérios flexíveis via query parameters."""
    termo = request.args.get("q", "")
    categoria = request.args.get("categoria", None)
    preco_min = request.args.get("preco_min", None)
    preco_max = request.args.get("preco_max", None)

    # Conversão segura de tipos numéricos
    if preco_min:
        try:
            preco_min = float(preco_min)
        except ValueError:
            return jsonify({"erro": "preco_min deve ser um número decimal válido"}), 400
    if preco_max:
        try:
            preco_max = float(preco_max)
        except ValueError:
            return jsonify({"erro": "preco_max deve ser um número decimal válido"}), 400

    resultados = produto_model.buscar_produtos(termo, categoria, preco_min, preco_max)
    return jsonify({"dados": resultados, "total": len(resultados), "sucesso": True}), 200
