"""Camada de acesso ao banco de dados (SQLite).

Abre uma conexão por requisição (guardada em flask.g) e a fecha no final.
"""
import os
import sqlite3

from flask import current_app, g
from werkzeug.security import generate_password_hash

SQL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_erro=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Cria as tabelas e insere os dados iniciais."""
    db = get_db()
    with open(os.path.join(SQL_DIR, "schema.sql"), encoding="utf-8") as f:
        db.executescript(f.read())
    with open(os.path.join(SQL_DIR, "seed.sql"), encoding="utf-8") as f:
        db.executescript(f.read())
    db.execute(
        "INSERT INTO usuario (nome, email, senha_hash, perfil) VALUES (?, ?, ?, 'admin')",
        ("Administrador", "admin@docenuvem.com", generate_password_hash("admin123")),
    )
    db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)

    @app.cli.command("init-db")
    def init_db_command():
        """Recria o banco de dados: flask --app app init-db"""
        init_db()
        print("Banco de dados criado.")

    # Cria o banco automaticamente na primeira execução
    db_path = app.config["DATABASE"]
    if not app.config.get("TESTING") and not os.path.exists(db_path):
        with app.app_context():
            init_db()
