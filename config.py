"""Configurações da aplicação."""
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "troque-esta-chave-em-producao")
    DATABASE = os.path.join(BASE_DIR, "database", "cupcakes.db")
    TAXA_ENTREGA = 7.00          # RN04 - taxa fixa de entrega
    PEDIDO_MINIMO = 20.00        # RN03 - valor mínimo do pedido
    TESTING = False


class TestConfig(Config):
    TESTING = True
    DATABASE = ":memory:"
    SECRET_KEY = "teste"
