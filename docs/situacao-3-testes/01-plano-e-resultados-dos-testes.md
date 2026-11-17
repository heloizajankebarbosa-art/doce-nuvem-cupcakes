# Testes: verificação e validação

Seguindo o **Modelo V** do material da disciplina, cada nível de desenvolvimento tem um nível de teste correspondente:

| Desenvolvimento (verificação) | Teste correspondente (validação) | Como foi feito aqui |
|---|---|---|
| Requisitos (histórias US01–US20) | **Teste de aceitação** | Testes feitos por 5 colegas com o formulário ([03-formulario-teste-usuarios.md](03-formulario-teste-usuarios.md)). |
| Análise (casos de uso) | **Teste de sistema** | Roteiro manual de ponta a ponta no navegador (seção 3). |
| Arquitetura (MVC) | **Teste de integração** | `tests/test_rotas.py`: simula o navegador passando por Controller + Model + View + banco. |
| Código | **Teste unitário** | `tests/test_models.py`: testa cada regra de negócio isoladamente. |

## 1. Verificação (durante o desenvolvimento)

A verificação confere se o software foi construído **de acordo com a especificação**:

- [x] Cada regra de negócio (RN01–RN08) tem pelo menos um teste automatizado (tabela abaixo).
- [x] Revisão do código conferindo a separação MVC: nenhum Controller acessa o banco direto; nenhum Model gera HTML.
- [x] Todas as consultas SQL usam parâmetros (`?`), nunca texto concatenado (proteção contra SQL Injection).
- [x] Senhas conferidas no banco: só aparece o hash.
- [x] Conferido que o número completo do cartão não é gravado em nenhuma tabela.
- [x] Mensagens de erro conferidas contra o catálogo do documento de IHC.

### Rastreabilidade: regra → teste

| Regra | Teste(s) automatizado(s) |
|---|---|
| RN01 e-mail único | `test_email_duplicado` |
| RN02 senha ≥ 6 | `test_validacao_cadastro_erros` |
| RN03 pedido mínimo | `test_pedido_minimo` |
| RN04 taxa de entrega | `test_totais_entrega_e_retirada`, `test_retirada_nao_cobra_taxa` |
| RN05 estoque | `test_nao_passa_do_estoque`, `test_produto_esgotado`, `test_pedido_completo_baixa_estoque` |
| RN06 cartão | `test_luhn`, `test_cartao_valido`, `test_cartao_invalido` (5 casos), `test_cartao_recusado_nao_grava_pedido` |
| RN07 cancelamento | `test_cancelar_devolve_estoque`, `test_nao_cancela_em_preparo` |
| RN08 fluxo de status | `test_fluxo_de_status`, `test_admin_avanca_status` |
| RNF02 senha com hash | `test_senha_nao_fica_em_texto_puro` |
| RNF04 privacidade | `test_cliente_nao_ve_pedido_de_outro`, `test_cliente_nao_acessa_admin`, `test_checkout_exige_login` |
| RNF07 erros amigáveis | `test_produto_inexistente_mostra_404_amigavel`, `test_checkout_com_erro_mantem_dados` |

## 2. Testes automatizados (unitários e de integração)

**Ferramenta:** pytest · **Comando:** `pytest` · **Resultado:** ✅ **47 testes, 47 aprovados, 0 falhas**

Cada teste roda num banco de dados novo e temporário, então um teste não interfere no outro.

### Unitários – `tests/test_models.py` (35 testes)

| Classe | O que é testado | Qtde | Resultado |
|---|---|---|---|
| TestUsuario | Validação do cadastro (5 casos), criar e autenticar, hash da senha, e-mail duplicado | 8 | ✅ |
| TestProduto | Vitrine só com ativos, filtro e busca, produto inválido (3 casos), cadastrar e editar | 6 | ✅ |
| TestCarrinho | Somar quantidade, limite de estoque, esgotado, quantidade zero, totais | 5 | ✅ |
| TestPagamento | Algoritmo de Luhn, cartão válido, cartão inválido (5 casos), formas de pagamento | 8 | ✅ |
| TestPedido | Pedido completo, mínimo, endereço, retirada, cartão recusado, fluxo de status, cancelar | 8 | ✅ |

### Integração – `tests/test_rotas.py` (12 testes)

| Teste | Cenário | Resultado |
|---|---|---|
| test_vitrine_abre | Vitrine carrega e mostra "Esgotado" | ✅ |
| test_busca_sem_resultado | Busca sem resultado mostra mensagem | ✅ |
| test_produto_inexistente_mostra_404_amigavel | URL inexistente mostra página 404 própria | ✅ |
| test_cadastro_com_erros_mostra_mensagens | Cadastro inválido mostra todos os erros | ✅ |
| test_login_errado | Login errado retorna 401 com mensagem | ✅ |
| test_checkout_exige_login | Checkout sem login redireciona | ✅ |
| test_cliente_nao_acessa_admin | Cliente recebe 403 na área da loja | ✅ |
| test_fluxo_completo_de_compra | Cadastro → carrinho → cartão → confirmação (R$ 33,00) | ✅ |
| test_checkout_com_erro_mantem_dados | Erro no cartão mantém o que foi digitado | ✅ |
| test_cliente_nao_ve_pedido_de_outro | Pedido de outro cliente retorna 404 | ✅ |
| test_admin_avanca_status | Admin muda o pedido para "Em preparo" | ✅ |
| test_admin_cadastra_produto_invalido | Preço zero é recusado | ✅ |

## 3. Teste de sistema (manual, no navegador)

Feito no Google Chrome (computador 1280 px e celular 390 px), com prints salvos em [`docs/imagens/`](../imagens/).

| # | Passo | Resultado esperado | Obtido |
|---|---|---|---|
| 1 | Abrir a vitrine | 10 cupcakes, "Natal Especial" esgotado | ✅ |
| 2 | Abrir a vitrine no celular | Menu vira botão ☰, cartões em uma coluna | ✅ |
| 3 | Enviar o cadastro vazio | Erro embaixo de cada campo obrigatório | ✅ |
| 4 | Corrigir e enviar o cadastro | Conta criada e usuário logado | ✅ (após correção do BUG-01) |
| 5 | Adicionar 2 Nutella + 1 Red Velvet | Carrinho com R$ 36,00 | ✅ |
| 6 | Pagar com cartão 1234 5678 9012 3456 | "Número de cartão inválido" e nada gravado | ✅ |
| 7 | Pagar com 4111 1111 1111 1111, 12/30 | Pedido #1, R$ 43,00, "Aprovado", final 1111 | ✅ |
| 8 | Login de admin com senha errada | "E-mail ou senha incorretos." | ✅ |
| 9 | Admin avança o pedido #1 | Status "Em preparo" e cliente vê a linha do tempo atualizada | ✅ |
| 10 | Acessar /pagina-que-nao-existe | Página 404 da loja | ✅ |

## 4. Bugs encontrados nos testes internos

| ID | Onde | Descrição | Causa | Correção | Status |
|---|---|---|---|---|---|
| BUG-01 | Cadastro (front-end) | Depois de enviar o formulário com campos vazios e depois preenchê-los, o primeiro clique em "Criar conta" não fazia nada; era preciso clicar duas vezes. | As mensagens de erro só sumiam quando o campo perdia o foco. Ao clicar no botão, a mensagem sumia, a página "subia" alguns pixels e o clique caía fora do botão. | As mensagens agora somem enquanto a pessoa digita (evento `input`) e mensagens vazias não ocupam espaço (CSS `:empty`). | ✅ Corrigido |

## 5. Validação com usuários (teste de aceitação)

Ver [03-formulario-teste-usuarios.md](03-formulario-teste-usuarios.md) (modelo do formulário), a pasta [`laudos-testes-usuarios/`](laudos-testes-usuarios/) (os 5 laudos) e [04-melhorias-aplicadas.md](04-melhorias-aplicadas.md) (o que foi corrigido a partir deles).
