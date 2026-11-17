"""Model do Carrinho.

O carrinho fica guardado na sessão do navegador como um dicionário
{ "id_produto": quantidade }. As funções abaixo não dependem do Flask
para calcular valores, o que facilita os testes unitários.
"""
from app.models import produto as produto_model
from app.models.erros import ErroNegocio

QTD_MAXIMA_POR_ITEM = 50


def adicionar(carrinho, id_produto, quantidade=1):
    prod = produto_model.buscar(id_produto)
    if not prod or not prod["ativo"]:
        raise ErroNegocio("Este cupcake não está disponível.")
    if quantidade < 1:
        raise ErroNegocio("A quantidade precisa ser pelo menos 1.")
    chave = str(id_produto)
    nova_qtd = carrinho.get(chave, 0) + quantidade
    if nova_qtd > prod["estoque"]:                        # RN05
        raise ErroNegocio(
            f"Só temos {prod['estoque']} unidade(s) de {prod['nome']} no momento."
            if prod["estoque"] > 0 else f"{prod['nome']} está esgotado."
        )
    if nova_qtd > QTD_MAXIMA_POR_ITEM:
        raise ErroNegocio(f"O máximo por cupcake é {QTD_MAXIMA_POR_ITEM} unidades por pedido.")
    carrinho[chave] = nova_qtd
    return carrinho


def atualizar(carrinho, id_produto, quantidade):
    chave = str(id_produto)
    if quantidade <= 0:
        carrinho.pop(chave, None)
        return carrinho
    carrinho.pop(chave, None)
    return adicionar(carrinho, id_produto, quantidade)


def remover(carrinho, id_produto):
    carrinho.pop(str(id_produto), None)
    return carrinho


def itens(carrinho):
    """Lista de itens com produto, quantidade e subtotal da linha."""
    resultado = []
    for chave, qtd in carrinho.items():
        prod = produto_model.buscar(int(chave))
        if prod:
            resultado.append({
                "produto": prod,
                "quantidade": qtd,
                "subtotal": round(prod["preco"] * qtd, 2),
            })
    return resultado


def calcular_totais(subtotal, tipo_entrega, taxa_entrega):
    """RN04: entrega tem taxa fixa; retirada na loja é grátis."""
    taxa = taxa_entrega if tipo_entrega == "entrega" else 0.0
    return {"subtotal": round(subtotal, 2), "taxa": round(taxa, 2),
            "total": round(subtotal + taxa, 2)}
