-- Dados iniciais da loja (categorias e cupcakes)
-- O usuário administrador é criado pelo código (app/database.py),
-- porque a senha precisa ser gravada criptografada.

INSERT INTO categoria (nome) VALUES ('Clássicos'), ('Gourmet'), ('Veganos'), ('Datas especiais');

INSERT INTO produto (id_categoria, nome, descricao, preco, estoque, imagem) VALUES
(1, 'Baunilha Clássico',   'Massa fofinha de baunilha com cobertura de buttercream.',            8.00, 30, '🧁'),
(1, 'Chocolate Intenso',   'Massa de cacau 50% com ganache de chocolate meio amargo.',           9.00, 30, '🍫'),
(1, 'Red Velvet',          'Massa aveludada com cobertura de cream cheese.',                     10.00, 25, '❤️'),
(2, 'Nutella com Morango', 'Recheio de Nutella, cobertura de chantilly e morango fresco.',       13.00, 20, '🍓'),
(2, 'Pistache',            'Massa de pistache com brigadeiro de pistache e castanhas.',          14.00, 15, '💚'),
(2, 'Doce de Leite',       'Recheio cremoso de doce de leite com flor de sal.',                  12.00, 20, '🍮'),
(3, 'Banana com Canela',   'Vegano: massa de banana, canela e cobertura de castanha de caju.',   11.00, 15, '🍌'),
(3, 'Limão Siciliano',     'Vegano: massa cítrica com merengue de aquafaba.',                    11.00, 15, '🍋'),
(4, 'Kit Aniversário (6)', 'Caixa com 6 cupcakes sortidos e velinha. Ideal para presentear.',    55.00, 10, '🎂'),
(4, 'Natal Especial',      'Massa de especiarias com cobertura branca e decoração natalina.',    12.00, 0,  '🎄');
