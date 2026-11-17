# 2. Modelagem UML (revisada)

Os diagramas estão escritos em **Mermaid**, que o GitHub desenha automaticamente ao abrir este arquivo.

## 2.1 Diagrama de casos de uso geral

```mermaid
flowchart LR
    Visitante(["👤 Visitante"])
    Cliente(["👤 Cliente"])
    Admin(["🏪 Administrador"])

    subgraph Sistema["Sistema Doce Nuvem Cupcakes"]
        UC1(["UC01 Ver vitrine / filtrar / buscar"])
        UC2(["UC02 Ver detalhes do cupcake"])
        UC3(["UC03 Criar conta"])
        UC4(["UC04 Entrar / Sair"])
        UC5(["UC05 Gerenciar carrinho"])
        UC6(["UC06 Finalizar pedido"])
        UC7(["UC07 Pagar pedido"])
        UC8(["UC08 Acompanhar pedido"])
        UC9(["UC09 Cancelar pedido"])
        UC10(["UC10 Gerenciar pedidos da loja"])
        UC11(["UC11 Gerenciar cupcakes"])
    end

    Visitante --- UC1
    Visitante --- UC2
    Visitante --- UC3
    Visitante --- UC5
    Cliente --- UC4
    Cliente --- UC6
    Cliente --- UC8
    Cliente --- UC9
    Admin --- UC4
    Admin --- UC10
    Admin --- UC11
    UC6 -. "«include»" .-> UC7
    UC6 -. "«include»" .-> UC4
    Cliente -. "herda de" .-> Visitante
```

> O Cliente herda tudo o que o Visitante pode fazer (generalização entre atores).

## 2.2 Casos de uso expandidos

### UC06 – Finalizar pedido

| Campo | Descrição |
|---|---|
| **Identificador** | UC06 |
| **Ator principal** | Cliente |
| **Descrição** | O cliente confirma os itens do carrinho, escolhe como receber e paga. |
| **Pré-condições** | Cliente logado; carrinho com subtotal ≥ R$ 20,00 (RN03). |
| **Pós-condições** | Pedido gravado com status "Recebido", pagamento registrado, estoque baixado e carrinho esvaziado. |

**Fluxo básico**

1. O caso de uso começa quando o cliente clica em "Finalizar pedido" na TELA05 – Carrinho.
2. O sistema verifica se o cliente está logado. *<Fluxo alternativo A>*
3. O sistema exibe a TELA06 – Checkout com o resumo dos itens, subtotal, taxa e total.
4. O cliente escolhe "Entrega em casa" ou "Retirar na loja". *<Fluxo alternativo B>*
5. O sistema recalcula o total na hora (RN04).
6. O cliente informa o endereço de entrega.
7. O cliente escolhe a forma de pagamento (inclui UC07 – Pagar pedido).
8. O cliente clica em "Confirmar pedido".
9. O sistema confere de novo o estoque de cada item (RN05). *<Fluxo alternativo C>*
10. O sistema confere o pedido mínimo (RN03) e o endereço. *<Fluxo alternativo D>*
11. O sistema processa o pagamento (RN06). *<Fluxo alternativo E>*
12. O sistema grava, numa única transação, o pedido, os itens, a baixa de estoque e o pagamento.
13. O sistema esvazia o carrinho e exibe a TELA08 – Detalhe do pedido com a mensagem "Pedido realizado com sucesso!".
14. O caso de uso termina.

**Fluxos alternativos**

- **A – Cliente não está logado:** A2. O sistema mostra "Entre na sua conta para continuar" e leva para a TELA03 – Login. A3. Depois do login, o cliente volta ao checkout com o carrinho mantido.
- **B – Retirada na loja:** B4. O sistema esconde o campo de endereço e zera a taxa. B5. O fluxo continua no passo 7.
- **C – Estoque insuficiente:** C9. O sistema mostra "Não há estoque suficiente de [cupcake]. Ajuste o carrinho." C10. Nada é gravado e o cliente continua no checkout.
- **D – Endereço incompleto:** D10. O sistema mostra "Informe o endereço completo para entrega (rua, número e bairro)." e mantém os dados já digitados.
- **E – Pagamento recusado:** E11. O sistema mostra o motivo (ex.: "Este cartão está vencido."). E12. Nada é gravado; o cliente pode corrigir os dados ou escolher outra forma.

### UC07 – Pagar pedido

| Campo | Descrição |
|---|---|
| **Identificador** | UC07 |
| **Ator principal** | Cliente |
| **Pré-condições** | Estar no passo 7 do UC06. |
| **Pós-condições** | Pagamento "Aprovado" (PIX/cartão) ou "Pendente" (dinheiro). |

**Fluxo básico (cartão)**

1. O cliente escolhe "Cartão de crédito".
2. O sistema exibe os campos número, validade e CVV, com máscara.
3. O cliente preenche os dados.
4. O sistema valida: 16 dígitos, algoritmo de Luhn, validade não vencida, CVV com 3 dígitos (RN06). *<Fluxo alternativo A>*
5. O sistema aprova o pagamento e guarda só os 4 últimos dígitos (RNF03).

**Fluxos alternativos**

- **A – Dado de cartão inválido:** A4. O sistema mostra a mensagem do erro específico e volta ao passo 3.
- **B – PIX:** o pagamento é aprovado na confirmação (simulação).
- **C – Dinheiro na entrega:** o pagamento fica "Pendente" e passa para "Aprovado" quando o administrador marca o pedido como "Entregue".

### UC10 – Gerenciar pedidos da loja

| Campo | Descrição |
|---|---|
| **Identificador** | UC10 |
| **Ator principal** | Administrador |
| **Pré-condições** | Usuário logado com perfil "admin". |
| **Pós-condições** | Status do pedido atualizado. |

**Fluxo básico**

1. O administrador acessa "Pedidos da loja".
2. O sistema lista os pedidos do mais novo para o mais antigo.
3. O administrador pode filtrar por status.
4. O administrador clica no botão da próxima etapa (ex.: "→ Em preparo").
5. O sistema atualiza o status seguindo a ordem da RN08 e mostra a confirmação.

**Fluxos alternativos**

- **A – Pedido já entregue ou cancelado:** o sistema não mostra botão de ação.
- **B – Usuário sem perfil admin:** o sistema mostra a página de erro 403.

## 2.3 Diagrama de classes (persistência)

```mermaid
classDiagram
    direction LR
    class Usuario {
        +int idUsuario
        +String nome
        +String email
        -String senhaHash
        +String telefone
        +String endereco
        +String perfil
        +DateTime criadoEm
        +autenticar(email, senha) Usuario
        +criar(nome, email, senha)
    }
    class Categoria {
        +int idCategoria
        +String nome
    }
    class Produto {
        +int idProduto
        +String nome
        +String descricao
        +Decimal preco
        +int estoque
        +String imagem
        +bool ativo
        +listar(categoria, busca)
        +salvar(dados)
        +alternarAtivo()
    }
    class Pedido {
        +int idPedido
        +DateTime dataPedido
        +String tipoEntrega
        +String enderecoEntrega
        +Decimal subtotal
        +Decimal taxaEntrega
        +Decimal total
        +String status
        +String observacao
        +criar(carrinho, entrega, pagamento)
        +avancarStatus()
        +cancelar()
    }
    class ItemPedido {
        +int idItem
        +int quantidade
        +Decimal precoUnitario
        +subtotal() Decimal
    }
    class Pagamento {
        +int idPagamento
        +String forma
        +Decimal valor
        +String status
        +String finalCartao
        +DateTime dataPagamento
        +processar(forma, cartao)
        +validarCartao(numero, validade, cvv)
    }
    class Carrinho {
        <<sessão>>
        +dict itens
        +adicionar(produto, qtd)
        +atualizar(produto, qtd)
        +remover(produto)
        +calcularTotais(tipoEntrega)
    }

    Usuario "1" --> "0..*" Pedido : faz
    Categoria "1" o-- "0..*" Produto : agrupa
    Pedido "1" *-- "1..*" ItemPedido : contém
    ItemPedido "0..*" --> "1" Produto : refere-se a
    Pedido "1" *-- "1" Pagamento : é pago por
    Carrinho ..> Produto : usa
    Carrinho ..> Pedido : gera
```

- **Composição** (losango cheio): `ItemPedido` e `Pagamento` não existem sem o `Pedido`. Se o pedido for apagado, eles também são (`ON DELETE CASCADE`).
- **Agregação** (losango vazio): o `Produto` pertence a uma `Categoria`, mas faz sentido sozinho.
- O `Carrinho` não é persistido no banco; ele vive na sessão do navegador até virar um `Pedido`.

## 2.4 Diagrama de sequência – Finalizar pedido (MVC)

```mermaid
sequenceDiagram
    autonumber
    actor C as Cliente
    participant V as View (checkout.html)
    participant PC as PedidoController
    participant PM as Pedido (Model)
    participant PG as Pagamento (Model)
    participant DB as Banco SQLite

    C->>V: Preenche entrega e pagamento e clica "Confirmar pedido"
    V->>V: JavaScript valida campos obrigatórios
    V->>PC: POST /pedido/checkout
    PC->>PM: criar(usuario, carrinho, entrega, pagamento)
    PM->>DB: SELECT produtos do carrinho (estoque atual)
    DB-->>PM: produtos
    alt estoque insuficiente ou abaixo do mínimo
        PM-->>PC: ErroNegocio("...")
        PC-->>V: checkout.html com mensagem de erro (HTTP 400)
        V-->>C: Mostra o erro e mantém os dados digitados
    else dados válidos
        PM->>PG: processar(forma, dadosCartao)
        alt cartão inválido
            PG-->>PM: ErroNegocio("Este cartão está vencido.")
            PM-->>PC: ErroNegocio
            PC-->>V: checkout.html com erro (HTTP 400)
        else pagamento aprovado
            PG-->>PM: ("Aprovado", "1111")
            PM->>DB: INSERT pedido, itens, pagamento + UPDATE estoque (transação)
            DB-->>PM: id do pedido
            PM-->>PC: idPedido
            PC->>PC: Esvazia carrinho da sessão
            PC-->>V: Redireciona para /pedido/{id}
            V-->>C: "Pedido realizado com sucesso! 🎉"
        end
    end
```

## 2.5 Diagrama de sequência – Login

```mermaid
sequenceDiagram
    autonumber
    actor U as Usuário
    participant V as View (login.html)
    participant AC as AuthController
    participant UM as Usuario (Model)
    participant DB as Banco SQLite

    U->>V: Digita e-mail e senha
    V->>AC: POST /login
    AC->>UM: autenticar(email, senha)
    UM->>DB: SELECT usuario WHERE email = ?
    DB-->>UM: usuário (com senha_hash)
    UM->>UM: check_password_hash()
    alt senha correta
        UM-->>AC: usuario
        AC->>AC: Guarda id na sessão (mantém carrinho)
        AC-->>U: Redireciona para vitrine (cliente) ou pedidos (admin)
    else e-mail ou senha errados
        UM-->>AC: None
        AC-->>V: "E-mail ou senha incorretos." (HTTP 401)
    end
```

## 2.6 Diagrama de atividades – Processo de compra

```mermaid
flowchart TD
    I((Início)) --> A[Ver vitrine]
    A --> B[Adicionar cupcake ao carrinho]
    B --> E1{Tem estoque?}
    E1 -- Não --> M1[/Mostrar 'Só temos N unidades'/] --> A
    E1 -- Sim --> C{Quer mais?}
    C -- Sim --> A
    C -- Não --> D{Subtotal ≥ R$ 20?}
    D -- Não --> M2[/Mostrar quanto falta/] --> A
    D -- Sim --> L{Está logado?}
    L -- Não --> LG[Entrar ou criar conta] --> F
    L -- Sim --> F[Escolher entrega ou retirada]
    F --> G[Escolher forma de pagamento]
    G --> H{Pagamento válido?}
    H -- Não --> M3[/Mostrar motivo/] --> G
    H -- Sim --> J[Gravar pedido e baixar estoque]
    J --> K[Mostrar confirmação]
    K --> P[Loja prepara e atualiza status]
    P --> Fim((Fim))
```

## 2.7 Diagrama de estados – Pedido

```mermaid
stateDiagram-v2
    [*] --> Recebido
    Recebido --> EmPreparo : admin avança
    Recebido --> Cancelado : cliente cancela (RN07)
    EmPreparo --> SaiuParaEntrega : se entrega
    EmPreparo --> ProntoParaRetirada : se retirada
    SaiuParaEntrega --> Entregue
    ProntoParaRetirada --> Entregue
    Entregue --> [*]
    Cancelado --> [*]
```
