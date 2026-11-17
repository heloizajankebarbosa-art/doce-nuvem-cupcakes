-- =====================================================================
-- Doce Nuvem Cupcakes - Projeto físico do banco de dados
-- SGBD: SQLite 3 (o mesmo script roda em MySQL/PostgreSQL com ajustes
-- mínimos de tipos; ver docs/03-banco-de-dados.md)
-- =====================================================================

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS item_pedido;
DROP TABLE IF EXISTS pagamento;
DROP TABLE IF EXISTS pedido;
DROP TABLE IF EXISTS produto;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS usuario;

-- Usuários do sistema (clientes e administradores da loja)
CREATE TABLE usuario (
    id_usuario     INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           VARCHAR(100) NOT NULL,
    email          VARCHAR(120) NOT NULL UNIQUE,
    senha_hash     VARCHAR(255) NOT NULL,
    telefone       VARCHAR(20),
    endereco       VARCHAR(200),
    perfil         VARCHAR(10)  NOT NULL DEFAULT 'cliente'
                   CHECK (perfil IN ('cliente', 'admin')),
    criado_em      DATETIME     NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- Categorias da vitrine (Clássicos, Gourmet, Veganos...)
CREATE TABLE categoria (
    id_categoria   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome           VARCHAR(50)  NOT NULL UNIQUE
);

-- Cupcakes à venda
CREATE TABLE produto (
    id_produto     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_categoria   INTEGER      NOT NULL,
    nome           VARCHAR(80)  NOT NULL,
    descricao      VARCHAR(300),
    preco          DECIMAL(8,2) NOT NULL CHECK (preco > 0),
    estoque        INTEGER      NOT NULL DEFAULT 0 CHECK (estoque >= 0),
    imagem         VARCHAR(10)  NOT NULL DEFAULT '🧁',
    ativo          INTEGER      NOT NULL DEFAULT 1 CHECK (ativo IN (0, 1)),
    FOREIGN KEY (id_categoria) REFERENCES categoria(id_categoria)
);

-- Pedidos feitos pelos clientes
CREATE TABLE pedido (
    id_pedido        INTEGER PRIMARY KEY AUTOINCREMENT,
    id_usuario       INTEGER      NOT NULL,
    data_pedido      DATETIME     NOT NULL DEFAULT (datetime('now', 'localtime')),
    tipo_entrega     VARCHAR(10)  NOT NULL CHECK (tipo_entrega IN ('entrega', 'retirada')),
    endereco_entrega VARCHAR(200),
    subtotal         DECIMAL(8,2) NOT NULL CHECK (subtotal >= 0),
    taxa_entrega     DECIMAL(8,2) NOT NULL DEFAULT 0 CHECK (taxa_entrega >= 0),
    total            DECIMAL(8,2) NOT NULL CHECK (total >= 0),
    status           VARCHAR(20)  NOT NULL DEFAULT 'Recebido'
                     CHECK (status IN ('Recebido', 'Em preparo', 'Saiu para entrega',
                                       'Pronto para retirada', 'Entregue', 'Cancelado')),
    observacao       VARCHAR(200),
    FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario)
);

-- Itens de cada pedido (composição: só existem dentro de um pedido)
CREATE TABLE item_pedido (
    id_item          INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido        INTEGER      NOT NULL,
    id_produto       INTEGER      NOT NULL,
    quantidade       INTEGER      NOT NULL CHECK (quantidade > 0),
    preco_unitario   DECIMAL(8,2) NOT NULL CHECK (preco_unitario > 0),
    FOREIGN KEY (id_pedido)  REFERENCES pedido(id_pedido) ON DELETE CASCADE,
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

-- Pagamento do pedido (1 para 1)
CREATE TABLE pagamento (
    id_pagamento     INTEGER PRIMARY KEY AUTOINCREMENT,
    id_pedido        INTEGER      NOT NULL UNIQUE,
    forma            VARCHAR(10)  NOT NULL CHECK (forma IN ('pix', 'cartao', 'dinheiro')),
    valor            DECIMAL(8,2) NOT NULL CHECK (valor >= 0),
    status           VARCHAR(12)  NOT NULL DEFAULT 'Pendente'
                     CHECK (status IN ('Pendente', 'Aprovado', 'Recusado', 'Estornado')),
    final_cartao     VARCHAR(4),
    data_pagamento   DATETIME     NOT NULL DEFAULT (datetime('now', 'localtime')),
    FOREIGN KEY (id_pedido) REFERENCES pedido(id_pedido) ON DELETE CASCADE
);

CREATE INDEX idx_produto_categoria ON produto(id_categoria);
CREATE INDEX idx_pedido_usuario    ON pedido(id_usuario);
CREATE INDEX idx_item_pedido       ON item_pedido(id_pedido);
