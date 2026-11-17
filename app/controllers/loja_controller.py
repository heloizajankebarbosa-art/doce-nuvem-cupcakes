"""Controller da vitrine virtual."""
from flask import Blueprint, abort, render_template, request

from app.models import produto as produto_model

bp = Blueprint("loja", __name__)


@bp.route("/")
def vitrine():
    id_categoria = request.args.get("categoria", type=int)
    busca = request.args.get("busca", "").strip()
    produtos = produto_model.listar(id_categoria=id_categoria, busca=busca or None)
    return render_template("loja/vitrine.html", produtos=produtos,
                           categorias=produto_model.listar_categorias(),
                           categoria_atual=id_categoria, busca=busca)


@bp.route("/produto/<int:id_produto>")
def detalhe(id_produto):
    prod = produto_model.buscar(id_produto)
    if not prod or not prod["ativo"]:
        abort(404)
    return render_template("loja/produto.html", produto=prod)
