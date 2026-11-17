"""Controller do carrinho de compras."""
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

from app.models import carrinho as carrinho_model
from app.models.erros import ErroNegocio

bp = Blueprint("carrinho", __name__, url_prefix="/carrinho")


def _carrinho():
    return dict(session.get("carrinho", {}))


@bp.route("/")
def ver():
    itens = carrinho_model.itens(_carrinho())
    subtotal = sum(i["subtotal"] for i in itens)
    return render_template("carrinho/carrinho.html", itens=itens, subtotal=subtotal,
                           pedido_minimo=current_app.config["PEDIDO_MINIMO"])


@bp.route("/adicionar/<int:id_produto>", methods=["POST"])
def adicionar(id_produto):
    quantidade = request.form.get("quantidade", 1, type=int) or 1
    try:
        session["carrinho"] = carrinho_model.adicionar(_carrinho(), id_produto, quantidade)
        flash("Cupcake adicionado ao carrinho! 🧁", "sucesso")
    except ErroNegocio as e:
        flash(str(e), "erro")
    return redirect(request.referrer or url_for("loja.vitrine"))


@bp.route("/atualizar/<int:id_produto>", methods=["POST"])
def atualizar(id_produto):
    quantidade = request.form.get("quantidade", 0, type=int)
    try:
        session["carrinho"] = carrinho_model.atualizar(_carrinho(), id_produto, quantidade)
        flash("Carrinho atualizado.", "sucesso")
    except ErroNegocio as e:
        flash(str(e), "erro")
    return redirect(url_for("carrinho.ver"))


@bp.route("/remover/<int:id_produto>", methods=["POST"])
def remover(id_produto):
    session["carrinho"] = carrinho_model.remover(_carrinho(), id_produto)
    flash("Item removido do carrinho.", "sucesso")
    return redirect(url_for("carrinho.ver"))
