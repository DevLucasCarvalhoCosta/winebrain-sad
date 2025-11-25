import pandas as pd

# Carregar dados
compras = pd.read_csv('data/raw/compras.csv')
clientes_agg = pd.read_csv('data/processed/clientes_agregado.csv')
produtos = pd.read_csv('data/raw/produtos.csv')

print('=' * 70)
print('📊 ANÁLISE COMPLETA DOS DADOS REAIS DO WINEBRAIN')
print('=' * 70)

print('\n👥 CLIENTES:')
print(f'  • Total de clientes cadastrados: {len(clientes_agg)}')
print(f'  • Clientes que FIZERAM compras: {(clientes_agg["n_compras"] > 0).sum()}')
print(f'  • Clientes que NÃO compraram: {(clientes_agg["n_compras"] == 0).sum()}')

print('\n❌ CANCELAMENTOS:')
cancelamentos = clientes_agg['cancelou_assinatura'].value_counts()
print(f'  • Sim: {cancelamentos.get("Sim", 0)}')
print(f'  • Não: {cancelamentos.get("Não", 0)}')
taxa_cancelamento = (clientes_agg['cancelou_assinatura'] == 'Sim').sum() / len(clientes_agg) * 100
print(f'  • Taxa de cancelamento: {taxa_cancelamento:.1f}%')

print('\n⭐ CLUBE DE VINHOS:')
assinantes = clientes_agg['assinante_clube'].value_counts()
print(f'  • Sim: {assinantes.get("Sim", 0)}')
print(f'  • Não: {assinantes.get("Não", 0)}')
taxa_assinantes = (clientes_agg['assinante_clube'] == 'Sim').sum() / len(clientes_agg) * 100
print(f'  • Taxa de assinantes: {taxa_assinantes:.1f}%')

print('\n🛒 COMPRAS:')
print(f'  • Total de transações: {len(compras)}')
print(f'  • Clientes únicos que compraram: {compras["cliente_id"].nunique()}')
print(f'  • Média de compras por cliente: {len(compras) / compras["cliente_id"].nunique():.2f}')

print('\n💰 FINANCEIRO:')
receita_total = compras['valor'].sum()
print(f'  • Receita total: R$ {receita_total:,.2f}')
print(f'  • Ticket médio (por transação): R$ {compras["valor"].mean():.2f}')
print(f'  • Gasto médio por cliente: R$ {clientes_agg["total_gasto"].mean():.2f}')
print(f'  • Maior compra: R$ {compras["valor"].max():.2f}')
print(f'  • Menor compra: R$ {compras["valor"].min():.2f}')

print('\n📈 ENGAJAMENTO:')
print(f'  • Média: {clientes_agg["pontuacao_engajamento"].mean():.2f}')
print(f'  • Mínimo: {clientes_agg["pontuacao_engajamento"].min():.2f}')
print(f'  • Máximo: {clientes_agg["pontuacao_engajamento"].max():.2f}')

print('\n🍷 PRODUTOS:')
print(f'  • Total de produtos: {len(produtos)}')

print('\n📊 SEGMENTAÇÃO POR ENGAJAMENTO:')
clientes_agg['faixa_eng'] = pd.cut(clientes_agg['pontuacao_engajamento'], 
                                     bins=[0, 4, 7, 10], 
                                     labels=['Baixo (0-4)', 'Médio (4-7)', 'Alto (7-10)'])
segmentacao = clientes_agg['faixa_eng'].value_counts().sort_index()
for faixa, count in segmentacao.items():
    print(f'  • {faixa}: {count} clientes ({count/len(clientes_agg)*100:.1f}%)')

print('\n' + '=' * 70)
print('✅ Análise concluída!')
print('=' * 70)
