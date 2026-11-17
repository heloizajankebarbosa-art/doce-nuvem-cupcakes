"""Model de Pagamento (simulado).

Não há cobrança real: o sistema valida os dados como um gateway faria
e decide se o pagamento é aprovado. Isso permite testar o fluxo completo.
"""
from datetime import date

from app.models.erros import ErroNegocio

FORMAS = {"pix": "PIX", "cartao": "Cartão de crédito", "dinheiro": "Dinheiro na entrega"}


def luhn_valido(numero):
    """Algoritmo de Luhn: confere se o número do cartão é válido."""
    digitos = [int(d) for d in numero]
    soma = 0
    for i, d in enumerate(reversed(digitos)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        soma += d
    return soma % 10 == 0


def validar_cartao(numero, validade, cvv, hoje=None):
    """RN06: cartão com 16 dígitos, número válido, não vencido e CVV de 3 dígitos."""
    hoje = hoje or date.today()
    numero = (numero or "").replace(" ", "").replace("-", "")
    if not numero.isdigit() or len(numero) != 16:
        raise ErroNegocio("O número do cartão deve ter 16 dígitos.")
    if not luhn_valido(numero):
        raise ErroNegocio("Número de cartão inválido. Confira os dígitos.")
    try:
        mes, ano = (validade or "").split("/")
        mes, ano = int(mes), int(ano)
        ano += 2000 if ano < 100 else 0
        if not 1 <= mes <= 12:
            raise ValueError
    except ValueError:
        raise ErroNegocio("Validade inválida. Use o formato MM/AA, por exemplo 08/28.")
    if (ano, mes) < (hoje.year, hoje.month):
        raise ErroNegocio("Este cartão está vencido.")
    if not (cvv or "").isdigit() or len(cvv) != 3:
        raise ErroNegocio("O CVV deve ter 3 dígitos (verso do cartão).")
    return numero[-4:]


def processar(forma, dados_cartao=None):
    """Retorna (status, final_cartao)."""
    if forma not in FORMAS:
        raise ErroNegocio("Escolha uma forma de pagamento.")
    if forma == "cartao":
        dados_cartao = dados_cartao or {}
        final = validar_cartao(dados_cartao.get("numero"), dados_cartao.get("validade"),
                               dados_cartao.get("cvv"))
        return "Aprovado", final
    if forma == "pix":
        return "Aprovado", None
    return "Pendente", None   # dinheiro: pago na entrega
