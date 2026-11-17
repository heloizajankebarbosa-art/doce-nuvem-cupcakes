"""Model de Usuário: cadastro, login e dados do cliente."""
import re

from werkzeug.security import check_password_hash, generate_password_hash

from app.database import get_db
from app.models.erros import ErroNegocio

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def validar_cadastro(nome, email, senha, confirmacao):
    """Retorna a lista de erros encontrados (vazia se estiver tudo certo)."""
    erros = []
    if not nome or len(nome.strip()) < 3:
        erros.append("Informe seu nome completo (mínimo 3 letras).")
    if not email or not EMAIL_REGEX.match(email.strip()):
        erros.append("Informe um e-mail válido, por exemplo: nome@email.com.")
    if not senha or len(senha) < 6:                       # RN02
        erros.append("A senha precisa ter pelo menos 6 caracteres.")
    if senha != confirmacao:
        erros.append("A confirmação de senha não confere.")
    return erros


def criar(nome, email, senha, telefone="", endereco=""):
    db = get_db()
    email = email.strip().lower()
    if buscar_por_email(email):                           # RN01
        raise ErroNegocio("Este e-mail já está cadastrado. Faça login ou use outro e-mail.")
    cur = db.execute(
        "INSERT INTO usuario (nome, email, senha_hash, telefone, endereco) VALUES (?, ?, ?, ?, ?)",
        (nome.strip(), email, generate_password_hash(senha), telefone.strip(), endereco.strip()),
    )
    db.commit()
    return cur.lastrowid


def buscar_por_email(email):
    return get_db().execute(
        "SELECT * FROM usuario WHERE email = ?", (email.strip().lower(),)
    ).fetchone()


def buscar_por_id(id_usuario):
    return get_db().execute(
        "SELECT * FROM usuario WHERE id_usuario = ?", (id_usuario,)
    ).fetchone()


def autenticar(email, senha):
    """Retorna o usuário se e-mail e senha estiverem corretos; senão, None."""
    usuario = buscar_por_email(email or "")
    if usuario and check_password_hash(usuario["senha_hash"], senha or ""):
        return usuario
    return None
