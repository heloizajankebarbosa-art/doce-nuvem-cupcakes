"""Controller de pedidos: checkout, confirmação e acompanhamento."""
from flask import (Blueprint, abort, current_app, flash, g, redirect, render_template, request,
                   session, url_for)

from app.controllers.auth_controller import login_obrigatorio
from app.models import carrinho as carrinho_model
from app.models import pedido as pedido_model
from app.models.erros import ErroNegocio
from app.models.pagamento import FORMAS

bp = Blueprint("pedido", __name__, url_prefix="/pedido")


@bp.route("/checkout", methods=["GET", "POST"])
@login_obrigatorio
def checkout():
    carrinho = dict(session.get("carrinho", {}))
    if not carrinho:
        flash("Seu carrinho está vazio. Escolha seus cupcakes primeiro.", "aviso")
        return redirect(url_for("loja.vitrine"))

    itens = carrinho_model.itens(carrinho)
    subtotal = sum(i["subtotal"] for i in itens)
    cfg = current_app.config

    if request.method == "POST":
        f = request.form
        try:
            id_pedido = pedido_model.criar(
                id_usuario=g.usuario["id_usuario"], carrinho=carrinho,
                tipo_entrega=f.get("tipo_entrega"), endereco=f.get("endereco", ""),
                forma_pagamento=f.get("forma_pagamento"),
                dados_cartao={"numero": f.get("numero_cartao"), "validade": f.get("validade"),
                              "cvv": f.get("cvv")},
                observacao=f.get("observacao", ""),
                taxa_entrega=cfg["TAXA_ENTREGA"], pedido_minimo=cfg["PEDIDO_MINIMO"],
            )
        except ErroNegocio as e:
            flash(str(e), "erro")
            return render_template("pedido/checkout.html", itens=itens, subtotal=subtotal,
                                   taxa=cfg["TAXA_ENTREGA"], formas=FORMAS, dados=f), 400
        session["carrinho"] = {}
        flash("Pedido realizado com sucesso! 🎉", "sucesso")
        return redirect(url_for("pedido.detalhe", id_pedido=id_pedido))

    return render_template("pedido/checkout.html", itens=itens, subtotal=subtotal,
                           taxa=cfg["TAXA_ENTREGA"], formas=FORMAS,
                           dados={"endereco": g.usuario["endereco"] or ""})


@bp.route("/meus")
@login_obrigatorio
def meus():
    return render_template("pedido/meus_pedidos.html",
                           pedidos=pedido_model.listar_do_usuario(g.usuario["id_usuario"]))


@bp.route("/<int:id_pedido>")
@login_obrigatorio
def detalhe(id_pedido):
    dados = pedido_model.buscar(id_pedido)
    if not dados:
        abort(404)
    eh_dono = dados["pedido"]["id_usuario"] == g.usuario["id_usuario"]
    if not eh_dono and g.usuario["perfil"] != "admin":
        abort(404)   # não revela que o pedido de outra pessoa existe
    fluxo = pedido_model.FLUXO_STATUS[dados["pedido"]["tipo_entrega"]]
    return render_template("pedido/detalhe.html", **dados, fluxo=fluxo, formas=FORMAS)


@bp.route("/<int:id_pedido>/cancelar", methods=["POST"])
@login_obrigatorio
def cancelar(id_pedido):
    try:
        pedido_model.cancelar(id_pedido, g.usuario["id_usuario"])
        flash("Pedido cancelado. O valor será estornado.", "sucesso")
    except ErroNegocio as e:
        flash(str(e), "erro")
    return redirect(url_for("pedido.detalhe", id_pedido=id_pedido))
