from flask import request, jsonify
import src.models as models

def listar_usuarios():
    usuarios = models.get_todos_usuarios()
    return jsonify({"dados": usuarios, "sucesso": True}), 200

def buscar_usuario(id):
    usuario = models.get_usuario_por_id(id)
    if usuario:
        return jsonify({"dados": usuario, "sucesso": True}), 200
    else:
        return jsonify({"erro": "Usuário não encontrado"}), 404

def criar_usuario():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    nome = dados.get("nome", "")
    email = dados.get("email", "")
    senha = dados.get("senha", "")

    if not nome or not email or not senha:
        return jsonify({"erro": "Nome, email e senha são obrigatórios"}), 400

    id = models.criar_usuario(nome, email, senha)
    print(f"Usuário criado: {email}")
    return jsonify({"dados": {"id": id}, "sucesso": True}), 201

def login():
    dados = request.get_json()
    email = dados.get("email", "")
    senha = dados.get("senha", "")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    usuario = models.login_usuario(email, senha)
    if usuario:
        print(f"Login bem-sucedido: {email}")
        return jsonify({"dados": usuario, "sucesso": True, "mensagem": "Login OK"}), 200
    else:
        print(f"Login falhou: {email}")
        return jsonify({"erro": "Email ou senha inválidos", "sucesso": False}), 401
