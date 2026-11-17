# Formulário de teste para usuários (laudo de qualidade)

Este modelo é enviado aos **5 colegas/profissionais** que testam o sistema. Ele pode ser usado como **Google Forms** (perguntas abaixo) ou copiado para um documento Word e devolvido preenchido.

## Instruções para quem vai testar

Obrigada por ajudar! 🧁 O sistema é uma loja virtual de cupcakes. Tente usar como um cliente de verdade e, se puder, tente "quebrar" o sistema: digite dados errados, volte páginas, clique duas vezes.

- **Endereço do sistema:** _(colar aqui o link)_
- **Usuário da loja (admin):** admin@docenuvem.com · senha: admin123
- **Cliente:** crie sua própria conta
- **Cartão de teste:** 4111 1111 1111 1111 · validade 12/30 · CVV 123 (nada é cobrado)

### Roteiro sugerido
1. Navegue pela vitrine, filtre por categoria e busque um sabor.
2. Crie uma conta (tente primeiro com dados errados).
3. Monte um carrinho abaixo de R$ 20 e depois acima.
4. Finalize um pedido com entrega e cartão (tente um cartão errado antes).
5. Faça outro pedido com retirada e PIX, e depois cancele-o.
6. Saia, entre como administrador e avance o status do primeiro pedido até "Entregue".
7. Volte como cliente e veja a linha do tempo do pedido.
8. Abra o sistema no celular.

---

## Laudo de teste

**1. Nome de quem testou:** ______________________________

**2. Curso / área de atuação:** ______________________________

**3. Data do teste:** ____/____/______

**4. Dispositivo e navegador usados:** ( ) Computador ( ) Celular · Navegador: __________

**5. O que testei e FUNCIONOU** (descreva a funcionalidade):

| Funcionalidade | Observação |
|---|---|
| | |
| | |
| | |

**6. O que testei e NÃO FUNCIONOU** (descreva a funcionalidade e o que deve ser corrigido):

| Funcionalidade | O que aconteceu | O que deveria acontecer | Print da tela |
|---|---|---|---|
| | | | |
| | | | |

**7. Funcionalidades NÃO testadas** (o que ficou faltando e por quê, ou o que existe no projeto mas você não conseguiu fazer):

______________________________________________________________

**8. Sugestões de melhoria:**

______________________________________________________________

**9. Nota geral de 1 a 5** (facilidade de uso): ( ) 1 ( ) 2 ( ) 3 ( ) 4 ( ) 5

**10. Anexe prints das telas com erro** (no Google Forms: pergunta do tipo "Upload de arquivo"; no Word: cole a imagem).

---

## Como montar no Google Forms (5 minutos)

1. Acesse **forms.google.com** → **Em branco**. Título: *Laudo de teste – Doce Nuvem Cupcakes*.
2. Cole as instruções e o roteiro acima na descrição do formulário.
3. Crie as perguntas:

| # | Pergunta | Tipo no Google Forms | Obrigatória |
|---|---|---|---|
| 1 | Nome de quem testou | Resposta curta | Sim |
| 2 | Curso / área de atuação | Resposta curta | Não |
| 3 | Data do teste | Data | Sim |
| 4 | Dispositivo e navegador | Caixas de seleção + "Outro" | Sim |
| 5 | O que testei e funcionou | Parágrafo | Sim |
| 6 | O que testei e não funcionou (o que deve ser corrigido) | Parágrafo | Sim |
| 7 | Funcionalidades não testadas e por quê | Parágrafo | Sim |
| 8 | Sugestões de melhoria | Parágrafo | Não |
| 9 | Nota de 1 a 5 | Escala linear 1–5 | Sim |
| 10 | Prints das telas com erro | Upload de arquivo (imagens) | Não |

4. Clique em **Enviar** → ícone de link → copie e mande para os colegas.
5. Depois, em **Respostas**, clique nos três pontinhos → **Imprimir todas as respostas** → **Salvar como PDF**. Esse é o PDF com as 5 opiniões pedido na entrega. Salve-o em `docs/situacao-3-testes/laudos-testes-usuarios/`.
