# =====================================================================
# SUAS RESPOSTAS
# =====================================================================
# Escreva cada consulta SQL entre as aspas triplas, assim:
#
#     Q1 = """
#     SELECT ...
#     FROM ...
#     """
#
# Depois salve o arquivo (Ctrl+S) e veja o resultado no painel.
# Mexa só no que está ENTRE as aspas triplas.
# =====================================================================

# ---------------------------------------------------------------------
# NÍVEL 1 - AQUECIMENTO
# ---------------------------------------------------------------------

# Q1. Clientes no Centro
# Colunas do resultado: ClientesNoCentro
Q1 = """
SELECT COUNT(*) AS ClientesNoCentro
FROM Clientes
WHERE Bairro = 'Centro';
"""

# Q2. Hambúrgueres acima de R$ 30
# Colunas do resultado: NomeProduto, Preco
Q2 = """
SELECT NomeProduto, Preco
FROM Produtos
WHERE Categoria = 'Hambúrguer'
  AND Preco > 30
ORDER BY Preco DESC;
"""

# Q3. Pedidos por status
# Colunas do resultado: Status, QuantidadePedidos
Q3 = """
SELECT Status, COUNT(*) AS QuantidadePedidos
FROM Pedidos
WHERE Status IN ('Entregue', 'Cancelado')
GROUP BY Status;
"""

# Q4. Nota média e pedidos sem avaliação
# Colunas do resultado: PedidosEntregues, PedidosAvaliados, PedidosSemAvaliacao, NotaMedia
Q4 = """
SELECT
    COUNT(*) AS PedidosEntregues,
    COUNT(Avaliacao) AS PedidosAvaliados,
    COUNT(*) - COUNT(Avaliacao) AS PedidosSemAvaliacao,
    AVG(CAST(Avaliacao AS DECIMAL(4,2))) AS NotaMedia
FROM Pedidos
WHERE Status = 'Entregue';
"""

# Q5. Delivery x Retirada por mês
# Colunas do resultado: Mes, TipoEntrega, QuantidadePedidos
Q5 = """
SELECT 
    MONTH(DataPedido) AS Mes,
    TipoEntrega,
    COUNT(*) AS QuantidadePedidos
FROM Pedidos
WHERE Status = 'Entregue'
GROUP BY MONTH(DataPedido), TipoEntrega
ORDER BY Mes, TipoEntrega;
"""

# ---------------------------------------------------------------------
# NÍVEL 2 - CRUZANDO TABELAS
# ---------------------------------------------------------------------

# Q6. Pedidos de janeiro com cliente
# Colunas do resultado: IdPedido, DataPedido, Nome, Bairro, Status
Q6 = """
SELECT 
    p.IdPedido,
    p.DataPedido,
    c.Nome,
    c.Bairro,
    p.Status
FROM Pedidos p
INNER JOIN Clientes c ON p.IdCliente = c.IdCliente
WHERE p.DataPedido BETWEEN '2026-01-01' AND '2026-01-31'
ORDER BY p.DataPedido;
"""

# Q7. Entregas por entregador
# Colunas do resultado: Nome, Entregas
Q7 = """
SELECT 
    e.Nome,
    COUNT(p.IdPedido) AS Entregas
FROM Pedidos p
INNER JOIN Entregadores e ON p.IdEntregador = e.IdEntregador
WHERE p.Status = 'Entregue'
GROUP BY e.Nome
ORDER BY Entregas DESC;
"""

# Q8. Unidades e faturamento por produto
# Colunas do resultado: NomeProduto, UnidadesVendidas, Faturamento
Q8 = """
SELECT 
    pr.NomeProduto,
    SUM(i.Quantidade) AS UnidadesVendidas,
    SUM(i.Quantidade * i.PrecoUnitario) AS Faturamento
FROM ItensPedido i
INNER JOIN Produtos pr ON i.IdProduto = pr.IdProduto
INNER JOIN Pedidos pe ON i.IdPedido = pe.IdPedido
WHERE pe.Status = 'Entregue'
GROUP BY pr.NomeProduto
ORDER BY UnidadesVendidas DESC;
"""

# Q9. Faturamento por categoria
# Colunas do resultado: Categoria, Faturamento
Q9 = """
SELECT 
    pr.Categoria,
    SUM(i.Quantidade * i.PrecoUnitario) AS Faturamento
FROM ItensPedido i
INNER JOIN Produtos pr ON i.IdProduto = pr.IdProduto
INNER JOIN Pedidos pe ON i.IdPedido = pe.IdPedido
WHERE pe.Status = 'Entregue'
GROUP BY pr.Categoria
ORDER BY Faturamento DESC;
"""

# Q10. Bairros com 7+ pedidos entregues
# Colunas do resultado: Bairro, PedidosEntregues
Q10 = """
SELECT 
    c.Bairro,
    COUNT(p.IdPedido) AS PedidosEntregues
FROM Pedidos p
INNER JOIN Clientes c ON p.IdCliente = c.IdCliente
WHERE p.Status = 'Entregue'
GROUP BY c.Bairro
HAVING COUNT(p.IdPedido) >= 7;
"""

# Q11. Preços praticados do X-Bacon
# Colunas do resultado: PrecoUnitario, Unidades, Faturamento
Q11 = """
SELECT 
    i.PrecoUnitario,
    SUM(i.Quantidade) AS Unidades,
    SUM(i.Quantidade * i.PrecoUnitario) AS Faturamento
FROM ItensPedido i
INNER JOIN Produtos pr ON i.IdProduto = pr.IdProduto
INNER JOIN Pedidos pe ON i.IdPedido = pe.IdPedido
WHERE pr.NomeProduto = 'X-Bacon'
  AND pe.Status = 'Entregue'
GROUP BY i.PrecoUnitario;
"""

# ---------------------------------------------------------------------
# NÍVEL 3 - DESAFIO
# ---------------------------------------------------------------------

# Q12. Top 3 clientes (fidelidade)
# Colunas do resultado: Nome, Pedidos, TotalGasto
Q12 = """
SELECT TOP 3
    c.Nome,
    COUNT(DISTINCT pe.IdPedido) AS Pedidos,
    SUM(i.Quantidade * i.PrecoUnitario) AS TotalGasto
FROM Pedidos pe
INNER JOIN Clientes c ON pe.IdCliente = c.IdCliente
INNER JOIN ItensPedido i ON pe.IdPedido = i.IdPedido
WHERE pe.Status = 'Entregue'
GROUP BY c.Nome
ORDER BY TotalGasto DESC;
"""

# Q13. Faturamento mês a mês
# Colunas do resultado: Mes, PedidosEntregues, Faturamento
Q13 = """
SELECT 
    MONTH(pe.DataPedido) AS Mes,
    COUNT(DISTINCT pe.IdPedido) AS PedidosEntregues,
    SUM(i.Quantidade * i.PrecoUnitario) AS Faturamento
FROM Pedidos pe
INNER JOIN ItensPedido i ON pe.IdPedido = i.IdPedido
WHERE pe.Status = 'Entregue'
GROUP BY MONTH(pe.DataPedido)
ORDER BY Mes;
"""

# Q14. Entregador do trimestre
# Colunas do resultado: Nome, Entregas, NotaMedia
Q14 = """
SELECT 
    e.Nome,
    COUNT(p.IdPedido) AS Entregas,
    AVG(CAST(p.Avaliacao AS DECIMAL(4,2))) AS NotaMedia
FROM Pedidos p
INNER JOIN Entregadores e ON p.IdEntregador = e.IdEntregador
WHERE p.Status = 'Entregue'
GROUP BY e.Nome
HAVING COUNT(p.IdPedido) >= 4 
   AND AVG(CAST(p.Avaliacao AS DECIMAL(4,2))) >= 4.0;
"""

# Q15. Valor total dos pedidos de março
# Colunas do resultado: IdPedido, Nome, ValorProdutos, TaxaEntrega, ValorTotal
Q15 = """
SELECT 
    p.IdPedido,
    c.Nome,
    SUM(i.Quantidade * i.PrecoUnitario) AS ValorProdutos,
    p.TaxaEntrega,
    SUM(i.Quantidade * i.PrecoUnitario) + p.TaxaEntrega AS ValorTotal
FROM Pedidos p
INNER JOIN Clientes c ON p.IdCliente = c.IdCliente
INNER JOIN ItensPedido i ON p.IdPedido = i.IdPedido
WHERE p.Status = 'Entregue'
  AND MONTH(p.DataPedido) = 3
GROUP BY p.IdPedido, c.Nome, p.TaxaEntrega
ORDER BY ValorTotal DESC;
"""

# Q16. Clientes sem nenhum pedido
# Colunas do resultado: Nome, Bairro, DataCadastro
Q16 = """
SELECT 
    c.Nome,
    c.Bairro,
    c.DataCadastro
FROM Clientes c
LEFT JOIN Pedidos p ON c.IdCliente = p.IdCliente
WHERE p.IdPedido IS NULL;
"""

# Q17. Produto que nunca foi vendido
# Colunas do resultado: NomeProduto, Categoria, Preco
Q17 = """
SELECT 
    pr.NomeProduto,
    pr.Categoria,
    pr.Preco
FROM Produtos pr
LEFT JOIN ItensPedido i ON pr.IdProduto = i.IdProduto
WHERE i.IdProduto IS NULL;
"""