# Roteiro do vídeo de apresentação (cerca de 5 minutos)

**Antes de gravar:** apague `database/cupcakes.db` e rode `python run.py` para começar com o banco limpo. Deixe abertas duas abas: o sistema e o repositório no GitHub. Grave a tela com o **OBS Studio**, a **Barra de Jogos do Windows** (Win + Alt + R) ou o **Loom**.

| Tempo | O que mostrar | O que falar (sugestão) |
|---|---|---|
| 0:00–0:30 | Repositório no GitHub | "Olá, eu sou [nome], do curso de Engenharia de Software. Este é o meu Projeto Integrador II: a Doce Nuvem, uma loja virtual de cupcakes com vitrine, pedido, pagamento e entrega. Está tudo neste repositório: código, banco de dados, testes e a documentação de cada situação-problema." |
| 0:30–1:00 | Pastas `app/models`, `controllers`, `templates` | "Usei Python com Flask no padrão MVC. Os models têm as regras de negócio, os controllers recebem as requisições e as views são o HTML, CSS e JavaScript. O banco é SQLite." |
| 1:00–1:40 | Vitrine, filtro, busca, celular | "Na vitrine o cliente filtra por categoria ou busca um sabor. O Natal Especial aparece como esgotado. A tela também funciona no celular." |
| 1:40–2:20 | Cadastro com erro e depois certo | "Se a pessoa erra o cadastro, o sistema mostra o erro embaixo de cada campo. Corrigindo, a conta é criada e ela já entra logada." |
| 2:20–3:20 | Carrinho → mínimo → checkout → cartão errado → cartão certo | "O pedido mínimo é de R$ 20. No checkout, ao escolher retirada o total muda na hora. Se o cartão for inválido o pedido não é criado. Com o cartão de teste, o pedido é confirmado." |
| 3:20–4:00 | Login admin → avançar status → voltar ao cliente | "A loja entra como administradora, vê os pedidos e avança o status. O cliente acompanha pela linha do tempo." |
| 4:00–4:30 | Terminal rodando `pytest` | "Fiz 47 testes automatizados com pytest, unitários e de integração, e todos passaram." |
| 4:30–5:00 | `04-melhorias-aplicadas.md` | "Cinco colegas testaram o sistema pelo formulário. As principais mudanças a partir do feedback foram: [citar 1 ou 2]. Obrigada!" |

**Dica:** se o vídeo passar de 5 minutos, encurte a parte do código; o mais importante é mostrar o sistema funcionando.
