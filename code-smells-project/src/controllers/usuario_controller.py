from flask import request, jsonify
import src.models.usuario as usuario_model

def listar_usuarios():
    """Retorna todos os usuários cadastrados."""
    usuarios = usuario_model.get_todos_usuarios()
    return jsonify({"dados": usuarios, "sucesso": True}), 200

def buscar_usuario(id):
    """Busca um usuário individual."""
    usuario = usuario_model.get_usuario_por_id(id)
    if usuario:
        return jsonify({"dados": usuario, "sucesso": True}), 200
    return jsonify({"erro": "Usuário não encontrado"}), 404

def criar_usuario():
    """Valida a estrutura de entrada e cria um novo usuário."""
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    nome = dados.get("nome", "").strip()
    email = dados.get("email", "").strip()
    senha = dados.get("senha", "")

    if not nome or not email or not senha:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    id = usuario_model.criar_usuario(nome, email, senha)
    return jsonify({"dados": {"id": id}, "sucesso": True}), 201

def login():
    """Valida as credenciais do usuário e realiza a autenticação."""
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400
        
    email = dados.get("email", "").strip()
    senha = dados.get("senha", "")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = usuario_model.login_usuario(email, senha)
    if usuario:
        return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
    return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
