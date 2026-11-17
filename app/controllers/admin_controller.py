"""Controller da área administrativa da loja."""
from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from app.controllers.auth_controller import admin_obrigatorio
from app.models import pedido as pedido_model
from app.models import produto as produto_model
from app.models.erros import ErroNegocio
from app.models.pagamento import FORMAS

bp = Blueprint("admin", __name__, url_prefix="/admin")


@bp.route("/pedidos")
@admin_obrigatorio
def pedidos():
    status = request.args.get("status") or None
    lista = pedido_model.listar_todos(status)
    return render_template("admin/pedidos.html", pedidos=lista, status_atual=status,
                           proximo=pedido_model.proximo_status, formas=FORMAS)


@bp.route("/pedidos/<int:id_pedido>/avancar", methods=["POST"])
@admin_obrigatorio
def avancar(id_pedido):
    try:
        novo = pedido_model.avancar_status(id_pedido)
        flash(f"Pedido #{id_pedido} atualizado para “{novo}”.", "sucesso")
    except ErroNegocio as e:
        flash(str(e), "erro")
    return redirect(request.referrer or url_for("admin.pedidos"))


@bp.route("/produtos")
@admin_obrigatorio
def produtos():
    return render_template("admin/produtos.html",
                           produtos=produto_model.listar(somente_ativos=False))


@bp.route("/produtos/novo", methods=["GET", "POST"])
@bp.route("/produtos/<int:id_produto>/editar", methods=["GET", "POST"])
@admin_obrigatorio
def produto_form(id_produto=None):
    prod = produto_model.buscar(id_produto) if id_produto else None
    if id_produto and not prod:
        abort(404)
    if request.method == "POST":
        try:
            produto_model.salvar(request.form, id_produto)
            flash("Cupcake salvo com sucesso.", "sucesso")
            return redirect(url_for("admin.produtos"))
        except ErroNegocio as e:
            flash(str(e), "erro")
            return render_template("admin/produto_form.html", produto=request.form,
                                   categorias=produto_model.listar_categorias(),
                                   id_produto=id_produto), 400
    return render_template("admin/produto_form.html", produto=prod or {"ativo": 1},
                           categorias=produto_model.listar_categorias(), id_produto=id_produto)


@bp.route("/produtos/<int:id_produto>/alternar", methods=["POST"])
@admin_obrigatorio
def alternar(id_produto):
    produto_model.alternar_ativo(id_produto)
    flash("Disponibilidade do cupcake alterada.", "sucesso")
    return redirect(url_for("admin.produtos"))
