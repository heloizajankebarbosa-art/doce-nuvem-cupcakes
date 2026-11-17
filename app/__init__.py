"""Fábrica da aplicação Flask (padrão MVC).

Model      -> app/models       (regras de negócio e acesso aos dados)
View       -> app/templates    (HTML/CSS/JS que o usuário vê)
Controller -> app/controllers  (recebe a requisição, chama o model e escolhe a view)
"""
from flask import Flask, render_template, session

from config import Config
from app import database


def formatar_moeda(valor):
    return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_data(texto):
    """'2026-11-17 14:05:00' -> '17/11/2026 14:05'"""
    try:
        data, hora = str(texto).split(" ")
        ano, mes, dia = data.split("-")
        return f"{dia}/{mes}/{ano} {hora[:5]}"
    except ValueError:
        return texto


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    database.init_app(app)
    app.jinja_env.filters["moeda"] = formatar_moeda
    app.jinja_env.filters["data"] = formatar_data

    from app.controllers.loja_controller import bp as loja_bp
    from app.controllers.auth_controller import bp as auth_bp
    from app.controllers.carrinho_controller import bp as carrinho_bp
    from app.controllers.pedido_controller import bp as pedido_bp
    from app.controllers.admin_controller import bp as admin_bp

    app.register_blueprint(loja_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(carrinho_bp)
    app.register_blueprint(pedido_bp)
    app.register_blueprint(admin_bp)

    @app.context_processor
    def dados_globais():
        carrinho = session.get("carrinho", {})
        return {"qtd_carrinho": sum(carrinho.values())}

    # Tratamento de erros: páginas amigáveis em vez da tela padrão
    @app.errorhandler(403)
    def proibido(_e):
        return render_template("erros/erro.html", codigo=403,
                               mensagem="Você não tem permissão para acessar esta página."), 403

    @app.errorhandler(404)
    def nao_encontrado(_e):
        return render_template("erros/erro.html", codigo=404,
                               mensagem="Ops! Não encontramos esta página."), 404

    @app.errorhandler(500)
    def erro_interno(_e):
        return render_template("erros/erro.html", codigo=500,
                               mensagem="Algo deu errado do nosso lado. Tente de novo em instantes."), 500

    return app
