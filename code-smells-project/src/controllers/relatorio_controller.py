from flask import jsonify
import src.models.pedido as pedido_model

def relatorio_vendas():
    """Gera o consolidado do relatório de vendas a partir dos modelos."""
    relatorio = pedido_model.relatorio_vendas()
    return jsonify({"dados": relatorio, "sucesso": True}), 200
