"""Controller de autenticação: cadastro, login e logout."""
from functools import wraps

from flask import (Blueprint, abort, flash, g, redirect, render_template, request, session,
                   url_for)

from app.models import usuario as usuario_model
from app.models.erros import ErroNegocio

bp = Blueprint("auth", __name__)


@bp.before_app_request
def carregar_usuario():
    id_usuario = session.get("id_usuario")
    g.usuario = usuario_model.buscar_por_id(id_usuario) if id_usuario else None


def login_obrigatorio(view):
    @wraps(view)
    def envolvida(*args, **kwargs):
        if g.usuario is None:
            flash("Entre na sua conta para continuar.", "aviso")
            return redirect(url_for("auth.login", proximo=request.path))
        return view(*args, **kwargs)
    return envolvida


def admin_obrigatorio(view):
    @wraps(view)
    def envolvida(*args, **kwargs):
        if g.usuario is None:
            return redirect(url_for("auth.login", proximo=request.path))
        if g.usuario["perfil"] != "admin":
            abort(403)
        return view(*args, **kwargs)
    return envolvida


@bp.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        f = request.form
        erros = usuario_model.validar_cadastro(f.get("nome"), f.get("email"),
                                               f.get("senha"), f.get("confirmacao"))
        if not erros:
            try:
                id_usuario = usuario_model.criar(f["nome"], f["email"], f["senha"],
                                                 f.get("telefone", ""), f.get("endereco", ""))
                session["id_usuario"] = id_usuario
                flash("Conta criada com sucesso! Bem-vinda(o) à Doce Nuvem.", "sucesso")
                return redirect(url_for("loja.vitrine"))
            except ErroNegocio as e:
                erros.append(str(e))
        for erro in erros:
            flash(erro, "erro")
        return render_template("auth/cadastro.html", dados=f), 400
    return render_template("auth/cadastro.html", dados={})


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = usuario_model.autenticar(request.form.get("email"), request.form.get("senha"))
        if usuario is None:
            flash("E-mail ou senha incorretos.", "erro")
            return render_template("auth/login.html", email=request.form.get("email", "")), 401
        carrinho = session.get("carrinho", {})
        session.clear()
        session["id_usuario"] = usuario["id_usuario"]
        session["carrinho"] = carrinho          # mantém o carrinho de quem não estava logado
        flash(f"Olá, {usuario['nome'].split()[0]}!", "sucesso")
        proximo = request.args.get("proximo")
        if proximo and proximo.startswith("/") and not proximo.startswith("//"):
            return redirect(proximo)
        if usuario["perfil"] == "admin":
            return redirect(url_for("admin.pedidos"))
        return redirect(url_for("loja.vitrine"))
    return render_template("auth/login.html", email="")


@bp.route("/logout")
def logout():
    session.clear()
    flash("Você saiu da sua conta.", "sucesso")
    return redirect(url_for("loja.vitrine"))
