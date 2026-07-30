from src.config.database import get_db

def criar_pedido(usuario_id, itens):
    """Cria um pedido com todos os seus itens associados e atualiza o estoque sob uma transação atômica."""
    db = get_db()
    cursor = db.cursor()

    try:
        # Inicia explicitamente a transação
        cursor.execute("BEGIN TRANSACTION;")
        
        total = 0
        itens_validados = []
        
        # Validação inicial dos itens e cálculo de preço total
        for item in itens:
            cursor.execute("SELECT * FROM produtos WHERE id = ?", (item["produto_id"],))
            produto = cursor.fetchone()
            if produto is None:
                db.rollback()
                return {"erro": f"Produto {item['produto_id']} não encontrado"}
            if produto["estoque"] < item["quantidade"]:
                db.rollback()
                return {"erro": f"Estoque insuficiente para {produto['nome']}"}
            
            total += produto["preco"] * item["quantidade"]
            itens_validados.append({
                "produto_id": item["produto_id"],
                "quantidade": item["quantidade"],
                "preco_unitario": produto["preco"]
            })

        # Insere a cabeceira do pedido
        cursor.execute(
            "INSERT INTO pedidos (usuario_id, status, total) VALUES (?, 'pendente', ?)",
            (usuario_id, total)
        )
        pedido_id = cursor.lastrowid

        # Insere os itens vinculados e realiza o decremento do estoque
        for item in itens_validados:
            cursor.execute(
                "INSERT INTO itens_pedido (pedido_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)",
                (pedido_id, item["produto_id"], item["quantidade"], item["preco_unitario"])
            )
            cursor.execute(
                "UPDATE produtos SET estoque = estoque - ? WHERE id = ?",
                (item["quantidade"], item["produto_id"])
            )

        # Efetiva todas as operações da transação no banco
        db.commit()
        return {"pedido_id": pedido_id, "total": total}

    except Exception as e:
        # Em caso de falha de conexão, lock ou erro SQL, desfaz todo o progresso do pedido
        db.rollback()
        raise e

def get_pedidos_usuario(usuario_id):
    """Retorna todos os pedidos de um usuário agrupando seus itens em uma consulta otimizada (Resolve N+1)."""
    db = get_db()
    cursor = db.cursor()
    
    # Executa LEFT JOIN para buscar o cabeçalho, itens e nomes dos produtos em uma única query
    query = """
        SELECT p.id AS pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
               i.produto_id, i.quantidade, i.preco_unitario, pr.nome AS produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido i ON p.id = i.pedido_id
        LEFT JOIN produtos pr ON i.produto_id = pr.id
        WHERE p.usuario_id = ?
        ORDER BY p.id DESC
    """
    cursor.execute(query, (usuario_id,))
    rows = cursor.fetchall()
    
    pedidos_dict = {}
    for row in rows:
        ped_id = row["pedido_id"]
        if ped_id not in pedidos_dict:
            pedidos_dict[ped_id] = {
                "id": ped_id,
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": []
            }
        
        # Adiciona o item se ele existir na tabela de junção
        if row["produto_id"] is not None:
            pedidos_dict[ped_id]["itens"].append({
                "produto_id": row["produto_id"],
                "produto_nome": row["produto_nome"] if row["produto_nome"] else "Desconhecido",
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"]
            })
            
    return list(pedidos_dict.values())

def get_todos_pedidos():
    """Retorna todos os pedidos cadastrados, resolvendo o gargalo de performance N+1."""
    db = get_db()
    cursor = db.cursor()
    
    # Junção otimizada para buscar todos os pedidos e seus itens associados de uma só vez
    query = """
        SELECT p.id AS pedido_id, p.usuario_id, p.status, p.total, p.criado_em,
               i.produto_id, i.quantidade, i.preco_unitario, pr.nome AS produto_nome
        FROM pedidos p
        LEFT JOIN itens_pedido i ON p.id = i.pedido_id
        LEFT JOIN produtos pr ON i.produto_id = pr.id
        ORDER BY p.id DESC
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    
    pedidos_dict = {}
    for row in rows:
        ped_id = row["pedido_id"]
        if ped_id not in pedidos_dict:
            pedidos_dict[ped_id] = {
                "id": ped_id,
                "usuario_id": row["usuario_id"],
                "status": row["status"],
                "total": row["total"],
                "criado_em": row["criado_em"],
                "itens": []
            }
        
        if row["produto_id"] is not None:
            pedidos_dict[ped_id]["itens"].append({
                "produto_id": row["produto_id"],
                "produto_nome": row["produto_nome"] if row["produto_nome"] else "Desconhecido",
                "quantidade": row["quantidade"],
                "preco_unitario": row["preco_unitario"]
            })
            
    return list(pedidos_dict.values())

def relatorio_vendas():
    """Gera um consolidado do relatório de vendas a partir do banco de dados."""
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT COUNT(*) FROM pedidos")
    total_pedidos = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(total) FROM pedidos")
    faturamento = cursor.fetchone()[0]
    if faturamento is None:
        faturamento = 0.0

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'pendente'")
    pendentes = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'aprovado'")
    aprovados = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM pedidos WHERE status = 'cancelado'")
    cancelados = cursor.fetchone()[0]

    # Regra de negócio para descontos aplicáveis
    desconto = 0.0
    if faturamento > 10000:
        desconto = faturamento * 0.1
    elif faturamento > 5000:
        desconto = faturamento * 0.05
    elif faturamento > 1000:
        desconto = faturamento * 0.02

    ticket_medio = (faturamento / total_pedidos) if total_pedidos > 0 else 0.0

    return {
        "total_pedidos": total_pedidos,
        "faturamento_bruto": round(faturamento, 2),
        "desconto_aplicavel": round(desconto, 2),
        "faturamento_liquido": round(faturamento - desconto, 2),
        "pedidos_pendentes": pendentes,
        "pedidos_aprovados": aprovados,
        "pedidos_cancelados": cancelados,
        "ticket_medio": round(ticket_medio, 2)
    }

def atualizar_status_pedido(pedido_id, novo_status):
    """Atualiza o status de um pedido com parâmetros limpos e seguros."""
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "UPDATE pedidos SET status = ? WHERE id = ?",
        (novo_status, pedido_id)
    )
    db.commit()
    return True
