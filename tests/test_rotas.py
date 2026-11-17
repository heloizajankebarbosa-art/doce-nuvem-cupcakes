"""Testes de integração: simulam o navegador passando por Controller + Model + View."""
from tests.conftest import CARTAO_VALIDO, cadastrar_e_logar, logar_admin


def texto(resp):
    return resp.get_data(as_text=True)


def test_vitrine_abre(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert "Red Velvet" in texto(resp) and "Esgotado" in texto(resp)


def test_busca_sem_resultado(client):
    assert "Nenhum cupcake encontrado" in texto(client.get("/?busca=pizza"))


def test_produto_inexistente_mostra_404_amigavel(client):
    resp = client.get("/produto/999")
    assert resp.status_code == 404 and "Não encontramos" in texto(resp)


def test_cadastro_com_erros_mostra_mensagens(client):
    resp = client.post("/cadastro", data={"nome": "A", "email": "x", "senha": "1", "confirmacao": "2"})
    assert resp.status_code == 400
    assert "e-mail válido" in texto(resp) and "6 caracteres" in texto(resp)


def test_login_errado(client):
    resp = client.post("/login", data={"email": "ninguem@x.com", "senha": "123456"})
    assert resp.status_code == 401 and "incorretos" in texto(resp)


def test_checkout_exige_login(client):
    resp = client.get("/pedido/checkout")
    assert resp.status_code == 302 and "/login" in resp.headers["Location"]


def test_cliente_nao_acessa_admin(client):
    cadastrar_e_logar(client)
    assert client.get("/admin/pedidos").status_code == 403


def test_fluxo_completo_de_compra(client):
    """Cliente se cadastra, adiciona ao carrinho, paga com cartão e acompanha."""
    cadastrar_e_logar(client)
    client.post("/carrinho/adicionar/4", data={"quantidade": 2})   # 2 x 13,00
    assert "Nutella com Morango" in texto(client.get("/carrinho/"))

    resp = client.post("/pedido/checkout", data={
        "tipo_entrega": "entrega", "endereco": "Rua das Flores, 100, Centro",
        "forma_pagamento": "cartao", "numero_cartao": CARTAO_VALIDO,
        "validade": "12/35", "cvv": "123",
    }, follow_redirects=True)
    pagina = texto(resp)
    assert "Pedido realizado com sucesso" in pagina
    assert "R$ 33,00" in pagina and "final 1111" in pagina   # 26 + 7
    assert "Aprovado" in pagina
    assert "#1" in texto(client.get("/pedido/meus"))


def test_checkout_com_erro_mantem_dados(client):
    cadastrar_e_logar(client)
    client.post("/carrinho/adicionar/4", data={"quantidade": 2})
    resp = client.post("/pedido/checkout", data={
        "tipo_entrega": "entrega", "endereco": "Rua X, 1, Bairro Y",
        "forma_pagamento": "cartao", "numero_cartao": "1234", "validade": "12/35", "cvv": "123",
        "observacao": "tocar campainha",
    })
    assert resp.status_code == 400
    assert "16 dígitos" in texto(resp) and "tocar campainha" in texto(resp)


def test_cliente_nao_ve_pedido_de_outro(client, app):
    cadastrar_e_logar(client)
    client.post("/carrinho/adicionar/4", data={"quantidade": 2})
    client.post("/pedido/checkout", data={"tipo_entrega": "retirada", "forma_pagamento": "pix"})
    client.get("/logout")
    cadastrar_e_logar(client, email="joao@teste.com")
    assert client.get("/pedido/1").status_code == 404


def test_admin_avanca_status(client):
    cadastrar_e_logar(client)
    client.post("/carrinho/adicionar/9", data={"quantidade": 1})   # kit 55,00
    client.post("/pedido/checkout", data={"tipo_entrega": "retirada", "forma_pagamento": "pix"})
    client.get("/logout")
    logar_admin(client)
    resp = client.post("/admin/pedidos/1/avancar", follow_redirects=True)
    assert "Em preparo" in texto(resp)


def test_admin_cadastra_produto_invalido(client):
    logar_admin(client)
    resp = client.post("/admin/produtos/novo", data={"nome": "X", "preco": "0", "estoque": "1",
                                                     "id_categoria": "1"})
    assert resp.status_code == 400 and "maior que zero" in texto(resp)


def test_adicionar_volta_para_o_mesmo_cupcake(client):
    """FB-03: depois de adicionar, a página volta para o cupcake, e não para o topo."""
    resp = client.post("/carrinho/adicionar/7", data={"quantidade": 1, "ancora": "produto-7"},
                       headers={"Referer": "http://localhost/?categoria=3"})
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/?categoria=3#produto-7")
    assert 'id="produto-7"' in texto(client.get("/"))


def test_ancora_invalida_e_ignorada(client):
    resp = client.post("/carrinho/adicionar/7", data={"quantidade": 1, "ancora": "javascript:alert(1)"},
                       headers={"Referer": "http://localhost/"})
    assert "#" not in resp.headers["Location"]


def test_vitrine_tem_seletor_de_quantidade(client):
    """FB-04: a vitrine mostra os botões − e + em cada cupcake disponível."""
    pagina = texto(client.get("/"))
    assert pagina.count("data-seletor") == 9          # 10 cupcakes, 1 esgotado
    assert 'aria-label="Aumentar quantidade de Red Velvet"' in pagina


def test_adicionar_varias_unidades_de_uma_vez(client):
    """FB-04: escolher 2 unidades na vitrine coloca 2 no carrinho."""
    resp = client.post("/carrinho/adicionar/3", data={"quantidade": 2, "ancora": "produto-3"},
                       follow_redirects=True)
    assert "2 cupcakes adicionados ao carrinho" in texto(resp)
    carrinho = texto(client.get("/carrinho/"))
    assert 'value="2"' in carrinho and "R$ 20,00" in carrinho
