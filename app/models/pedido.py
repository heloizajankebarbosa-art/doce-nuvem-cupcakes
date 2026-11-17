"""Model de Pedido: finalizar compra, acompanhar e atualizar status."""
from app.database import get_db
from app.models import carrinho as carrinho_model
from app.models import pagamento as pagamento_model
from app.models.erros import ErroNegocio

# RN08 - sequência permitida de status
FLUXO_STATUS = {
    "entrega":  ["Recebido", "Em preparo", "Saiu para entrega", "Entregue"],
    "retirada": ["Recebido", "Em preparo", "Pronto para retirada", "Entregue"],
}


def criar(id_usuario, carrinho, tipo_entrega, endereco, forma_pagamento,
          dados_cartao=None, observacao="", taxa_entrega=7.0, pedido_minimo=20.0):
    if not carrinho:
        raise ErroNegocio("Seu carrinho está vazio.")
    if tipo_entrega not in ("entrega", "retirada"):
        raise ErroNegocio("Escolha entrega em casa ou retirada na loja.")
    if tipo_entrega == "entrega" and len((endereco or "").strip()) < 10:
        raise ErroNegocio("Informe o endereço completo para entrega (rua, número e bairro).")

    db = get_db()
    linhas = carrinho_model.itens(carrinho)
    for item in linhas:                                    # RN05 - confere estoque de novo
        prod = item["produto"]
        if not prod["ativo"] or item["quantidade"] > prod["estoque"]:
            raise ErroNegocio(f"Não há estoque suficiente de {prod['nome']}. Ajuste o carrinho.")

    subtotal = sum(i["subtotal"] for i in linhas)
    if subtotal < pedido_minimo:                           # RN03
        raise ErroNegocio(
            f"O pedido mínimo é de R$ {pedido_minimo:.2f}".replace(".", ",")
            + f". Faltam R$ {pedido_minimo - subtotal:.2f}".replace(".", ",") + "."
        )
    totais = carrinho_model.calcular_totais(subtotal, tipo_entrega, taxa_entrega)

    # Valida o pagamento ANTES de gravar qualquer coisa
    status_pag, final_cartao = pagamento_model.processar(forma_pagamento, dados_cartao)

    try:
        cur = db.execute(
            """INSERT INTO pedido (id_usuario, tipo_entrega, endereco_entrega, subtotal,
               taxa_entrega, total, observacao) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (id_usuario, tipo_entrega,
             endereco.strip() if tipo_entrega == "entrega" else None,
             totais["subtotal"], totais["taxa"], totais["total"], (observacao or "").strip()),
        )
        id_pedido = cur.lastrowid
        for item in linhas:
            prod = item["produto"]
            db.execute(
                """INSERT INTO item_pedido (id_pedido, id_produto, quantidade, preco_unitario)
                   VALUES (?, ?, ?, ?)""",
                (id_pedido, prod["id_produto"], item["quantidade"], prod["preco"]),
            )
            db.execute("UPDATE produto SET estoque = estoque - ? WHERE id_produto = ?",
                       (item["quantidade"], prod["id_produto"]))
        db.execute(
            """INSERT INTO pagamento (id_pedido, forma, valor, status, final_cartao)
               VALUES (?, ?, ?, ?, ?)""",
            (id_pedido, forma_pagamento, totais["total"], status_pag, final_cartao),
        )
        db.commit()
    except Exception:
        db.rollback()
        raise
    return id_pedido


def buscar(id_pedido):
    db = get_db()
    ped = db.execute(
        """SELECT p.*, u.nome AS cliente, u.email, pg.forma, pg.status AS status_pagamento,
                  pg.final_cartao
           FROM pedido p
           JOIN usuario u ON u.id_usuario = p.id_usuario
           LEFT JOIN pagamento pg ON pg.id_pedido = p.id_pedido
           WHERE p.id_pedido = ?""",
        (id_pedido,),
    ).fetchone()
    if not ped:
        return None
    itens = db.execute(
        """SELECT i.*, pr.nome, pr.imagem FROM item_pedido i
           JOIN produto pr ON pr.id_produto = i.id_produto WHERE i.id_pedido = ?""",
        (id_pedido,),
    ).fetchall()
    return {"pedido": ped, "itens": itens}


def listar_do_usuario(id_usuario):
    return get_db().execute(
        "SELECT * FROM pedido WHERE id_usuario = ? ORDER BY id_pedido DESC", (id_usuario,)
    ).fetchall()


def listar_todos(status=None):
    sql = """SELECT p.*, u.nome AS cliente, pg.forma, pg.status AS status_pagamento
             FROM pedido p JOIN usuario u ON u.id_usuario = p.id_usuario
             LEFT JOIN pagamento pg ON pg.id_pedido = p.id_pedido"""
    params = []
    if status:
        sql += " WHERE p.status = ?"
        params.append(status)
    sql += " ORDER BY p.id_pedido DESC"
    return get_db().execute(sql, params).fetchall()


def proximo_status(pedido):
    fluxo = FLUXO_STATUS[pedido["tipo_entrega"]]
    if pedido["status"] not in fluxo or pedido["status"] == fluxo[-1]:
        return None
    return fluxo[fluxo.index(pedido["status"]) + 1]


def avancar_status(id_pedido):
    """RN08: o administrador só pode levar o pedido para o próximo passo do fluxo."""
    dados = buscar(id_pedido)
    if not dados:
        raise ErroNegocio("Pedido não encontrado.")
    novo = proximo_status(dados["pedido"])
    if not novo:
        raise ErroNegocio("Este pedido já foi finalizado.")
    db = get_db()
    db.execute("UPDATE pedido SET status = ? WHERE id_pedido = ?", (novo, id_pedido))
    if novo == "Entregue" and dados["pedido"]["forma"] == "dinheiro":
        db.execute("UPDATE pagamento SET status = 'Aprovado' WHERE id_pedido = ?", (id_pedido,))
    db.commit()
    return novo


def cancelar(id_pedido, id_usuario):
    """RN07: o cliente só cancela enquanto o pedido está 'Recebido'. O estoque volta."""
    dados = buscar(id_pedido)
    if not dados or dados["pedido"]["id_usuario"] != id_usuario:
        raise ErroNegocio("Pedido não encontrado.")
    if dados["pedido"]["status"] != "Recebido":
        raise ErroNegocio("Este pedido já está em preparo e não pode mais ser cancelado.")
    db = get_db()
    for item in dados["itens"]:
        db.execute("UPDATE produto SET estoque = estoque + ? WHERE id_produto = ?",
                   (item["quantidade"], item["id_produto"]))
    db.execute("UPDATE pedido SET status = 'Cancelado' WHERE id_pedido = ?", (id_pedido,))
    db.execute("UPDATE pagamento SET status = 'Estornado' WHERE id_pedido = ?", (id_pedido,))
    db.commit()
