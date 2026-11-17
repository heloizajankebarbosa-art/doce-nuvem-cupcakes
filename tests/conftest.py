"""Configuração dos testes: cada teste usa um banco novo, em arquivo temporário."""
import pytest

from app import create_app
from app.database import init_db
from config import TestConfig


@pytest.fixture
def app(tmp_path):
    class Cfg(TestConfig):
        DATABASE = str(tmp_path / "teste.db")

    app = create_app(Cfg)
    with app.app_context():
        init_db()
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def ctx(app):
    """Contexto da aplicação para testar os models diretamente."""
    with app.app_context():
        yield


def cadastrar_e_logar(client, email="maria@teste.com", senha="segredo1"):
    client.post("/cadastro", data={"nome": "Maria Silva", "email": email, "senha": senha,
                                   "confirmacao": senha, "endereco": "Rua das Flores, 100, Centro"})
    return client


def logar_admin(client):
    client.post("/login", data={"email": "admin@docenuvem.com", "senha": "admin123"})
    return client


CARTAO_VALIDO = "4111111111111111"
