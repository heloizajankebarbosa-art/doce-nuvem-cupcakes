# 4. Interface Humano-Computador (IHC)

## 4.1 Princípios aplicados

| Princípio (material da disciplina) | Como foi aplicado |
|---|---|
| **Clara** | Linguagem simples nos botões ("Adicionar", "Finalizar pedido"). Cada tela tem um título que diz onde o usuário está. |
| **Consistente** | Mesma cor (rosa) para todas as ações principais; mesmo menu e rodapé em todas as telas; mensagens sempre no topo, com a mesma cor por tipo. |
| **Simples** | Só três passos no checkout (receber → pagar → observações). Campos de cartão e endereço só aparecem quando são necessários (divulgação progressiva). |
| **Controlada pelo usuário** | Nada acontece sozinho; o usuário pode alterar ou remover itens a qualquer momento. |
| **Direta** | O total muda na hora ao trocar entrega/retirada; o contador do carrinho no topo muda ao adicionar. |
| **Empática e reversível** | Pode cancelar o pedido enquanto não está em preparo; o administrador "tira da vitrine" em vez de apagar; ação de cancelar pede confirmação. |
| **Dá resposta (feedback)** | Toda ação mostra mensagem verde (sucesso), amarela (aviso) ou vermelha (erro). Erros de formulário aparecem embaixo do campo. |
| **Esteticamente agradável** | Paleta rosa e chocolate (tema confeitaria), cartões com cantos arredondados, bastante espaço em branco. |

**Acessibilidade:** rótulos (`label`) em todos os campos, link "Pular para o conteúdo", foco visível ao navegar com Tab, mensagens com `aria-live` (lidas por leitores de tela), emojis decorativos com `aria-hidden`, idioma `pt-BR` declarado e layout que funciona a partir de 360 px.

## 4.2 Mapa navegacional

```mermaid
flowchart TD
    V["🏠 TELA01 Vitrine<br/>(filtro e busca)"]
    D["TELA02 Detalhe do cupcake"]
    L["TELA03 Login"]
    CA["TELA04 Cadastro"]
    CR["TELA05 Carrinho"]
    CK["TELA06 Checkout"]
    PD["TELA08 Detalhe do pedido<br/>(confirmação e acompanhamento)"]
    MP["TELA07 Meus pedidos"]
    AP["TELA09 Admin: Pedidos da loja"]
    APR["TELA10 Admin: Cupcakes"]
    APF["TELA11 Admin: Novo/editar cupcake"]
    E["TELA12 Páginas de erro 403/404/500"]

    V <--> D
    V --> CR
    D --> CR
    V <--> L
    L <--> CA
    CR --> CK
    CK -- "não logado" --> L
    CK -- "confirmar" --> PD
    V --> MP
    MP <--> PD
    L -- "admin" --> AP
    AP <--> PD
    AP <--> APR
    APR <--> APF
    E --> V
```

## 4.3 Mapa conceitual

```mermaid
mindmap
  root((Doce Nuvem<br/>Cupcakes))
    Vitrine
      Categorias
      Busca por sabor
      Detalhe e estoque
    Cliente
      Cadastro
      Login e logout
      Meus pedidos
    Pedido
      Carrinho
      Pedido mínimo R$ 20
      Checkout
    Pagamento
      PIX
      Cartão validado
      Dinheiro na entrega
    Entrega
      Em casa + R$ 7
      Retirada grátis
      Linha do tempo do status
    Loja
      Gerenciar pedidos
      Cadastrar cupcakes
      Tirar da vitrine
```

## 4.4 Telas (protótipo funcional)

As imagens abaixo são prints do sistema funcionando. Elas substituem os wireframes do PITE I, já que agora o protótipo virou o produto.

| Tela | Imagem |
|---|---|
| TELA01 – Vitrine | ![Vitrine](../imagens/01-vitrine.png) |
| TELA01 – Vitrine no celular | ![Celular](../imagens/16-celular-vitrine.png) |
| TELA02 – Detalhe do cupcake | ![Detalhe](../imagens/02-produto.png) |
| TELA04 – Cadastro com erros | ![Cadastro](../imagens/03-cadastro-erros-front.png) |
| TELA05 – Carrinho | ![Carrinho](../imagens/05-carrinho.png) |
| TELA06 – Checkout | ![Checkout](../imagens/07-checkout-preenchido.png) |
| TELA06 – Checkout com cartão inválido | ![Erro cartão](../imagens/06-checkout-cartao-invalido.png) |
| TELA08 – Pedido confirmado | ![Confirmado](../imagens/08-pedido-confirmado.png) |
| TELA07 – Meus pedidos | ![Meus pedidos](../imagens/09-meus-pedidos.png) |
| TELA03 – Login com erro | ![Login](../imagens/10-login-erro.png) |
| TELA09 – Admin: pedidos | ![Admin pedidos](../imagens/11-admin-pedidos.png) |
| TELA10 – Admin: cupcakes | ![Admin cupcakes](../imagens/12-admin-produtos.png) |
| TELA11 – Admin: novo cupcake | ![Novo cupcake](../imagens/13-admin-novo-produto.png) |
| TELA12 – Erro 404 | ![404](../imagens/15-erro-404.png) |

## 4.5 Catálogo de mensagens

| Situação | Mensagem | Tipo |
|---|---|---|
| Campo obrigatório vazio | Preencha este campo. | Erro (no campo) |
| E-mail mal digitado | Informe um e-mail válido, por exemplo: nome@email.com. | Erro |
| Senha curta | A senha precisa ter pelo menos 6 caracteres. | Erro |
| Senhas diferentes | A confirmação de senha não confere. | Erro |
| E-mail já usado | Este e-mail já está cadastrado. Faça login ou use outro e-mail. | Erro |
| Login errado | E-mail ou senha incorretos. | Erro |
| Página restrita sem login | Entre na sua conta para continuar. | Aviso |
| Acima do estoque | Só temos N unidade(s) de [cupcake] no momento. | Erro |
| Produto esgotado | [Cupcake] está esgotado. | Erro |
| Abaixo do mínimo | O pedido mínimo é de R$ 20,00. Faltam R$ X. | Aviso |
| Endereço incompleto | Informe o endereço completo para entrega (rua, número e bairro). | Erro |
| Cartão curto | O número do cartão deve ter 16 dígitos. | Erro |
| Cartão inválido | Número de cartão inválido. Confira os dígitos. | Erro |
| Cartão vencido | Este cartão está vencido. | Erro |
| Validade errada | Validade inválida. Use o formato MM/AA, por exemplo 08/28. | Erro |
| CVV errado | O CVV deve ter 3 dígitos (verso do cartão). | Erro |
| Pedido feito | Pedido realizado com sucesso! 🎉 | Sucesso |
| Cancelar em preparo | Este pedido já está em preparo e não pode mais ser cancelado. | Erro |
| Página inexistente | Ops! Não encontramos esta página. | Erro 404 |
| Sem permissão | Você não tem permissão para acessar esta página. | Erro 403 |
| Falha no servidor | Algo deu errado do nosso lado. Tente de novo em instantes. | Erro 500 |
