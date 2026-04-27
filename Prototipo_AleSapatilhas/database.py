import sqlite3
from datetime import datetime

def conectar():
    """Conecta ao banco de dados aleSapatilhas.db"""
    return sqlite3.connect("aleSapatilhas.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    try:
        # 1. Tabela de Itens (Produtos)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT UNIQUE NOT NULL,
            cor TEXT NOT NULL,
            tamanho TEXT NOT NULL,
            precocusto REAL,
            precovenda REAL NOT NULL,
            quantidade INTEGER DEFAULT 0,
            categoria TEXT,
            fornecedor TEXT,
            status_item TEXT DEFAULT 'Disponível'
        )""")

        # 2. Tabela de Clientes
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            aniversario TEXT NOT NULL,
            tamanho_cliente INTEGER NOT NULL,
            logradouro TEXT NOT NULL,
            numero INTEGER,
            bairro TEXT,
            cidade TEXT,
            ponto_referencia TEXT,
            observacao TEXT,
            status_cliente TEXT DEFAULT 'Ativo'
        )""")

        # 3. Tabela de Vendas (Financeiro + Entrega)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            valor_total REAL NOT NULL,
            forma_pagamento TEXT,
            data_venda TEXT DEFAULT (datetime('now', 'localtime')),
            status_venda TEXT DEFAULT 'Pendente',
            status_entrega TEXT DEFAULT 'À Entregar',
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )""")

        # 4. Detalhes da Venda
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_venda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            venda_id INTEGER NOT NULL,
            produto_id INTEGER NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unitario REAL NOT NULL,
            FOREIGN KEY (venda_id) REFERENCES vendas (id),
            FOREIGN KEY (produto_id) REFERENCES itens (id)
        )""")
        
        conn.commit()
    finally:
        conn.close()

# --- GESTÃO DE CLIENTES ---

def salvar_cliente(nome, telefone, aniversario, tamanho, logra, num, bairro, cidade, ref, obs, status='Ativo'):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO clientes (nome, telefone, aniversario, tamanho_cliente, logradouro, 
            numero, bairro, cidade, ponto_referencia, observacao, status_cliente) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
            (nome, telefone, aniversario, tamanho, logra, num, bairro, cidade, ref, obs, status))    
        conn.commit()
    finally:
        conn.close()

def listar_clientes():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY nome ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- GESTÃO DE PRODUTOS ---

def salvar_item(produto, cor, tamanho, custo, venda, quantidade, categoria, fornecedor, status='Disponível'):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO itens (produto, cor, tamanho, precocusto, precovenda, quantidade, categoria, fornecedor, status_item) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
            (produto, cor, tamanho, custo, venda, quantidade, categoria, fornecedor, status))
        conn.commit()
    finally:
        conn.close()

def listar_itens():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM itens ORDER BY produto ASC")
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- GESTÃO DE VENDAS E STATUS ---

def registrar_venda(cliente_id, lista_produtos, forma_pagamento, status_v='Pendente', status_e='À Entregar'):
    """
    Registra venda, abate estoque e define status de pagamento e entrega.
    lista_produtos: [(produto_id, quantidade, preco_unitario), ...]
    """
    conn = conectar()
    cursor = conn.cursor()
    try:
        # Validação de Estoque
        for p_id, qtd, _ in lista_produtos:
            cursor.execute("SELECT quantidade, produto FROM itens WHERE id = ?", (p_id,))
            res = cursor.fetchone()
            if not res or res[0] < qtd:
                print(f"Erro: Estoque insuficiente para {res[1] if res else 'ID '+str(p_id)}")
                return False

        valor_total = sum(item[1] * item[2] for item in lista_produtos)
        
        cursor.execute("""
            INSERT INTO vendas (cliente_id, valor_total, forma_pagamento, status_venda, status_entrega) 
            VALUES (?, ?, ?, ?, ?)""", (cliente_id, valor_total, forma_pagamento, status_v, status_e))
        venda_id = cursor.lastrowid

        for p_id, qtd, p_unit in lista_produtos:
            cursor.execute("INSERT INTO itens_venda (venda_id, produto_id, quantidade, preco_unitario) VALUES (?, ?, ?, ?)", 
                           (venda_id, p_id, qtd, p_unit))
            cursor.execute("UPDATE itens SET quantidade = quantidade - ? WHERE id = ?", (qtd, p_id))

        conn.commit()
        print(f"Venda nº {venda_id} registrada com sucesso!")
        return True
    except Exception as e:
        conn.rollback()
        print(f"Erro no processamento: {e}")
        return False
    finally:
        conn.close()

def atualizar_status_venda_financeiro(id_venda, novo_status):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("UPDATE vendas SET status_venda = ? WHERE id = ?", (novo_status, id_venda))
    conn.commit(); conn.close()

def atualizar_status_entrega(id_venda, novo_status):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("UPDATE vendas SET status_entrega = ? WHERE id = ?", (novo_status, id_venda))
    conn.commit(); conn.close()

def listar_vendas_controle():
    conn = conectar()
    cursor = conn.cursor()
    query = """
    SELECT v.id, c.nome, v.valor_total, v.status_venda, v.status_entrega, v.data_venda
    FROM vendas v
    JOIN clientes c ON v.cliente_id = c.id
    ORDER BY v.id DESC
    """
    cursor.execute(query)
    dados = cursor.fetchall()
    conn.close()
    return dados

# --- RELATÓRIOS E ESTOQUE ---

def relatorio_lucro_detalhado():
    conn = conectar(); cursor = conn.cursor()
    query = "SELECT SUM((iv.preco_unitario - i.precocusto) * iv.quantidade) FROM itens_venda iv JOIN itens i ON iv.produto_id = i.id"
    cursor.execute(query)
    lucro = cursor.fetchone()[0]
    conn.close()
    return lucro if lucro else 0.0

def adicionar_estoque(produto_id, qtd_adicional):
    conn = conectar(); cursor = conn.cursor()
    cursor.execute("UPDATE itens SET quantidade = quantidade + ? WHERE id = ?", (qtd_adicional, produto_id))
    conn.commit(); conn.close()

if __name__ == "__main__":
    criar_tabelas()
    print("=== Sistema Alê Sapatilhas: Banco de Dados Pronto! ===")