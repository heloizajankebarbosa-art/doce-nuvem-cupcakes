"""Testes unitários dos Models (regras de negócio)."""
from datetime import date

import pytest

from app.models import carrinho, pagamento, pedido, produto, usuario
from app.models.erros import ErroNegocio
from tests.conftest import CARTAO_VALIDO


# ---------- Usuário ----------
class TestUsuario:
    def test_validacao_cadastro_ok(self):
        assert usuario.validar_cadastro("Maria Silva", "maria@x.com", "123456", "123456") == []

    @pytest.mark.parametrize("nome,email,senha,conf,trecho", [
        ("Ma", "maria@x.com", "123456", "123456", "nome"),
        ("Maria", "maria-sem-arroba", "123456", "123456", "e-mail"),
        ("Maria", "maria@x.com", "123", "123", "6 caracteres"),
        ("Maria", "maria@x.com", "123456", "654321", "confirmação"),
    ])
    def test_validacao_cadastro_erros(self, nome, email, senha, conf, trecho):
        erros = usuario.validar_cadastro(nome, email, senha, conf)
        assert any(trecho in e for e in erros)

    def test_criar_e_autenticar(self, ctx):
        usuario.criar("Ana Souza", "Ana@Teste.com", "minhasenha")
        assert usuario.autenticar("ana@teste.com", "minhasenha") is not None
        assert usuario.autenticar("ana@teste.com", "errada") is None

    def test_senha_nao_fica_em_texto_puro(self, ctx):
        usuario.criar("Ana Souza", "ana@teste.com", "minhasenha")
        assert usuario.buscar_por_email("ana@teste.com")["senha_hash"] != "minhasenha"

    def test_email_duplicado(self, ctx):
        usuario.criar("Ana Souza", "ana@teste.com", "minhasenha")
        with pytest.raises(ErroNegocio, match="já está cadastrado"):
            usuario.criar("Outra Ana", "ANA@teste.com", "outrasenha")


# ---------- Produto ----------
class TestProduto:
    def test_vitrine_mostra_somente_ativos(self, ctx):
        produto.alternar_ativo(1)
        ids = [p["id_produto"] for p in produto.listar()]
        assert 1 not in ids and len(ids) == 9

    def test_filtro_por_categoria_e_busca(self, ctx):
        assert all(p["id_categoria"] == 3 for p in produto.listar(id_categoria=3))
        assert [p["nome"] for p in produto.listar(busca="pistache")] == ["Pistache"]

    @pytest.mark.parametrize("preco,estoque", [("0", "5"), ("abc", "5"), ("10", "-1")])
    def test_produto_invalido(self, ctx, preco, estoque):
        with pytest.raises(ErroNegocio):
            produto.salvar({"nome": "Teste", "preco": preco, "estoque": estoque, "id_categoria": "1"})

    def test_cadastrar_e_editar(self, ctx):
        novo = produto.salvar({"nome": "Coco", "preco": "9.5", "estoque": "4", "id_categoria": "1"})
        produto.salvar({"nome": "Coco Queimado", "preco": "10", "estoque": "4", "id_categoria": "2"}, novo)
        p = produto.buscar(novo)
        assert p["nome"] == "Coco Queimado" and p["preco"] == 10 and p["categoria"] == "Gourmet"


# ---------- Carrinho ----------
class TestCarrinho:
    def test_adicionar_soma_quantidade(self, ctx):
        c = carrinho.adicionar({}, 1, 2)
        c = carrinho.adicionar(c, 1, 3)
        assert c == {"1": 5}

    def test_nao_passa_do_estoque(self, ctx):
        with pytest.raises(ErroNegocio, match="Só temos 30"):
            carrinho.adicionar({}, 1, 31)

    def test_produto_esgotado(self, ctx):
        with pytest.raises(ErroNegocio, match="esgotado"):
            carrinho.adicionar({}, 10, 1)       # Natal Especial tem estoque 0

    def test_quantidade_zero_remove(self, ctx):
        assert carrinho.atualizar({"1": 3}, 1, 0) == {}

    def test_totais_entrega_e_retirada(self):
        assert carrinho.calcular_totais(30.0, "entrega", 7.0) == {"subtotal": 30.0, "taxa": 7.0, "total": 37.0}
        assert carrinho.calcular_totais(30.0, "retirada", 7.0)["total"] == 30.0


# ---------- Pagamento ----------
class TestPagamento:
    def test_luhn(self):
        assert pagamento.luhn_valido(CARTAO_VALIDO)
        assert not pagamento.luhn_valido("4111111111111112")

    def test_cartao_valido(self):
        assert pagamento.validar_cartao("4111 1111 1111 1111", "12/30", "123",
                                        hoje=date(2026, 11, 17)) == "1111"

    @pytest.mark.parametrize("numero,validade,cvv,trecho", [
        ("4111", "12/30", "123", "16 dígitos"),
        ("4111111111111112", "12/30", "123", "inválido"),
        (CARTAO_VALIDO, "13/30", "123", "Validade"),
        (CARTAO_VALIDO, "10/26", "123", "vencido"),
        (CARTAO_VALIDO, "12/30", "12", "CVV"),
    ])
    def test_cartao_invalido(self, numero, validade, cvv, trecho):
        with pytest.raises(ErroNegocio, match=trecho):
            pagamento.validar_cartao(numero, validade, cvv, hoje=date(2026, 11, 17))

    def test_formas(self):
        assert pagamento.processar("pix") == ("Aprovado", None)
        assert pagamento.processar("dinheiro") == ("Pendente", None)
        with pytest.raises(ErroNegocio):
            pagamento.processar("bitcoin")


# ---------- Pedido ----------
class TestPedido:
    def _criar(self, **extra):
        id_u = usuario.criar("Cliente Teste", "cli@teste.com", "123456")
        args = dict(id_usuario=id_u, carrinho={"1": 3}, tipo_entrega="entrega",
                    endereco="Rua A, 10, Centro", forma_pagamento="pix")
        args.update(extra)
        return id_u, pedido.criar(**args)

    def test_pedido_completo_baixa_estoque(self, ctx):
        _, id_p = self._criar()
        dados = pedido.buscar(id_p)
        assert dados["pedido"]["total"] == 31.0          # 3 x 8,00 + 7,00
        assert dados["pedido"]["status_pagamento"] == "Aprovado"
        assert produto.buscar(1)["estoque"] == 27

    def test_pedido_minimo(self, ctx):
        with pytest.raises(ErroNegocio, match="pedido mínimo"):
            self._criar(carrinho={"1": 1})

    def test_endereco_obrigatorio_na_entrega(self, ctx):
        with pytest.raises(ErroNegocio, match="endereço"):
            self._criar(endereco="")

    def test_retirada_nao_cobra_taxa(self, ctx):
        _, id_p = self._criar(tipo_entrega="retirada", endereco="")
        assert pedido.buscar(id_p)["pedido"]["taxa_entrega"] == 0

    def test_cartao_recusado_nao_grava_pedido(self, ctx):
        with pytest.raises(ErroNegocio):
            self._criar(forma_pagamento="cartao", dados_cartao={"numero": "123"})
        assert produto.buscar(1)["estoque"] == 30
        assert pedido.listar_todos() == []

    def test_fluxo_de_status(self, ctx):
        _, id_p = self._criar(forma_pagamento="dinheiro")
        assert [pedido.avancar_status(id_p) for _ in range(3)] == \
            ["Em preparo", "Saiu para entrega", "Entregue"]
        assert pedido.buscar(id_p)["pedido"]["status_pagamento"] == "Aprovado"
        with pytest.raises(ErroNegocio, match="finalizado"):
            pedido.avancar_status(id_p)

    def test_cancelar_devolve_estoque(self, ctx):
        id_u, id_p = self._criar()
        pedido.cancelar(id_p, id_u)
        assert pedido.buscar(id_p)["pedido"]["status"] == "Cancelado"
        assert produto.buscar(1)["estoque"] == 30

    def test_nao_cancela_em_preparo(self, ctx):
        id_u, id_p = self._criar()
        pedido.avancar_status(id_p)
        with pytest.raises(ErroNegocio, match="não pode mais ser cancelado"):
            pedido.cancelar(id_p, id_u)
