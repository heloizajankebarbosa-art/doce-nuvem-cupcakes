"""Model de Produto: vitrine de cupcakes e cadastro pelo administrador."""
from app.database import get_db
from app.models.erros import ErroNegocio


def listar(id_categoria=None, busca=None, somente_ativos=True):
    sql = """SELECT p.*, c.nome AS categoria
             FROM produto p JOIN categoria c ON c.id_categoria = p.id_categoria
             WHERE 1 = 1"""
    params = []
    if somente_ativos:
        sql += " AND p.ativo = 1"
    if id_categoria:
        sql += " AND p.id_categoria = ?"
        params.append(id_categoria)
    if busca:
        sql += " AND (p.nome LIKE ? OR p.descricao LIKE ?)"
        params += [f"%{busca}%", f"%{busca}%"]
    sql += " ORDER BY c.id_categoria, p.nome"
    return get_db().execute(sql, params).fetchall()


def buscar(id_produto):
    return get_db().execute(
        """SELECT p.*, c.nome AS categoria FROM produto p
           JOIN categoria c ON c.id_categoria = p.id_categoria
           WHERE p.id_produto = ?""",
        (id_produto,),
    ).fetchone()


def listar_categorias():
    return get_db().execute("SELECT * FROM categoria ORDER BY id_categoria").fetchall()


def validar(nome, preco, estoque, id_categoria):
    erros = []
    if not nome or len(nome.strip()) < 3:
        erros.append("O nome do cupcake precisa ter pelo menos 3 letras.")
    try:
        if float(preco) <= 0:
            erros.append("O preço precisa ser maior que zero.")
    except (TypeError, ValueError):
        erros.append("Informe um preço válido, por exemplo: 9.50.")
    try:
        if int(estoque) < 0:
            erros.append("O estoque não pode ser negativo.")
    except (TypeError, ValueError):
        erros.append("Informe o estoque como número inteiro.")
    if not id_categoria:
        erros.append("Escolha uma categoria.")
    return erros


def salvar(dados, id_produto=None):
    erros = validar(dados.get("nome"), dados.get("preco"), dados.get("estoque"),
                    dados.get("id_categoria"))
    if erros:
        raise ErroNegocio(" ".join(erros))
    valores = (
        int(dados["id_categoria"]), dados["nome"].strip(), (dados.get("descricao") or "").strip(),
        round(float(dados["preco"]), 2), int(dados["estoque"]), dados.get("imagem") or "🧁",
        1 if dados.get("ativo", "1") in ("1", "on", 1, True) else 0,
    )
    db = get_db()
    if id_produto:
        db.execute(
            """UPDATE produto SET id_categoria=?, nome=?, descricao=?, preco=?, estoque=?,
               imagem=?, ativo=? WHERE id_produto=?""",
            valores + (id_produto,),
        )
    else:
        cur = db.execute(
            """INSERT INTO produto (id_categoria, nome, descricao, preco, estoque, imagem, ativo)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            valores,
        )
        id_produto = cur.lastrowid
    db.commit()
    return id_produto


def alternar_ativo(id_produto):
    db = get_db()
    db.execute("UPDATE produto SET ativo = 1 - ativo WHERE id_produto = ?", (id_produto,))
    db.commit()
