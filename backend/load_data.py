"""
Script para carregar e processar os dados do Excel
Converte os arquivos .xlsx para CSV e realiza análise exploratória inicial
"""

import pandas as pd
import numpy as np
from pathlib import Path
import json
from datetime import datetime

# Configuração de caminhos
BASE_DIR = Path(__file__).parent.parent
DOCS_DIR = BASE_DIR / "docs"
DATA_DIR = BASE_DIR / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Criar diretórios se não existirem
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def load_excel_data():
    """Carrega os dados dos arquivos Excel"""
    print("📂 Carregando dados do Excel...")
    
    # Carregar dados
    clientes = pd.read_excel(DOCS_DIR / "Cliente.xlsx")
    compras = pd.read_excel(DOCS_DIR / "Compras.xlsx")
    produtos = pd.read_excel(DOCS_DIR / "produtos.xlsx")
    
    # Converter pontuacao_engajamento para float
    if 'pontuacao_engajamento' in clientes.columns:
        clientes['pontuacao_engajamento'] = pd.to_numeric(clientes['pontuacao_engajamento'], errors='coerce')
    
    print(f"✅ Clientes: {len(clientes)} registros")
    print(f"✅ Compras: {len(compras)} registros")
    print(f"✅ Produtos: {len(produtos)} registros")
    
    return clientes, compras, produtos


def save_to_csv(clientes, compras, produtos):
    """Salva os dados em formato CSV"""
    print("\n💾 Salvando dados em CSV...")
    
    clientes.to_csv(RAW_DIR / "clientes.csv", index=False, encoding='utf-8-sig')
    compras.to_csv(RAW_DIR / "compras.csv", index=False, encoding='utf-8-sig')
    produtos.to_csv(RAW_DIR / "produtos.csv", index=False, encoding='utf-8-sig')
    
    print("✅ Dados salvos com sucesso!")


def analyze_data(clientes, compras, produtos):
    """Realiza análise exploratória dos dados"""
    print("\n📊 Análise Exploratória dos Dados\n")
    print("=" * 60)
    
    # ========== ANÁLISE DE CLIENTES ==========
    print("\n👥 ANÁLISE DE CLIENTES")
    print("-" * 60)
    print(f"Total de clientes: {len(clientes)}")
    print(f"\nColunas: {list(clientes.columns)}")
    
    if 'pontuacao_engajamento' in clientes.columns:
        print(f"\n📈 Engajamento:")
        print(clientes['pontuacao_engajamento'].describe())
    
    if 'cancelou_assinatura' in clientes.columns:
        print(f"\n❌ Cancelamentos:")
        print(clientes['cancelou_assinatura'].value_counts())
    
    if 'assinante_clube' in clientes.columns:
        print(f"\n⭐ Assinantes do Clube:")
        print(clientes['assinante_clube'].value_counts())
    
    if 'cidade' in clientes.columns:
        print(f"\n🌍 Distribuição por Cidade (Top 5):")
        print(clientes['cidade'].value_counts().head())
    
    # ========== ANÁLISE DE PRODUTOS ==========
    print("\n\n🍷 ANÁLISE DE PRODUTOS")
    print("-" * 60)
    print(f"Total de produtos: {len(produtos)}")
    print(f"\nColunas: {list(produtos.columns)}")
    
    if 'tipo_uva' in produtos.columns:
        print(f"\n🍇 Tipos de Uva:")
        print(produtos['tipo_uva'].value_counts())
    
    if 'pais' in produtos.columns:
        print(f"\n🌎 Países:")
        print(produtos['pais'].value_counts())
    
    if 'preco' in produtos.columns:
        print(f"\n💰 Preços:")
        print(produtos['preco'].describe())
    
    # ========== ANÁLISE DE COMPRAS ==========
    print("\n\n🛒 ANÁLISE DE COMPRAS")
    print("-" * 60)
    print(f"Total de compras: {len(compras)}")
    print(f"\nColunas: {list(compras.columns)}")
    
    if 'valor' in compras.columns:
        print(f"\n💵 Valores:")
        print(compras['valor'].describe())
    
    if 'quantidade' in compras.columns:
        print(f"\n📦 Quantidades:")
        print(compras['quantidade'].describe())
    
    # ========== ANÁLISE INTEGRADA ==========
    print("\n\n🔗 ANÁLISE INTEGRADA")
    print("-" * 60)
    
    # Merge das bases
    compras_produtos = compras.merge(produtos, on='produto_id', how='left')
    compras_completo = compras_produtos.merge(clientes, on='cliente_id', how='left')
    
    # Agregação por cliente
    cliente_agg = compras.groupby('cliente_id').agg({
        'valor': ['sum', 'mean', 'count'],
        'quantidade': 'sum'
    }).reset_index()
    
    cliente_agg.columns = ['cliente_id', 'total_gasto', 'ticket_medio', 'n_compras', 'quantidade_total']
    
    # Merge com dados do cliente - RIGHT JOIN para incluir todos os clientes
    cliente_completo = clientes.merge(cliente_agg, on='cliente_id', how='left')
    
    # Preencher valores NaN para clientes sem compras
    cliente_completo['total_gasto'] = cliente_completo['total_gasto'].fillna(0)
    cliente_completo['ticket_medio'] = cliente_completo['ticket_medio'].fillna(0)
    cliente_completo['n_compras'] = cliente_completo['n_compras'].fillna(0)
    cliente_completo['quantidade_total'] = cliente_completo['quantidade_total'].fillna(0)
    
    print(f"\n💰 Estatísticas de Gasto por Cliente:")
    print(cliente_completo[['total_gasto', 'ticket_medio', 'n_compras']].describe())
    
    # Salvar dados processados
    cliente_completo.to_csv(PROCESSED_DIR / "clientes_agregado.csv", index=False, encoding='utf-8-sig')
    compras_completo.to_csv(PROCESSED_DIR / "compras_completo.csv", index=False, encoding='utf-8-sig')
    
    # ========== ANÁLISE POR SEGMENTOS ==========
    print("\n\n📊 ANÁLISE POR SEGMENTOS")
    print("-" * 60)
    
    if 'cancelou_assinatura' in cliente_completo.columns:
        print("\n❌ Por Status de Cancelamento:")
        cancelamento_stats = cliente_completo.groupby('cancelou_assinatura').agg({
            'pontuacao_engajamento': 'mean',
            'total_gasto': 'mean',
            'n_compras': 'mean',
            'cliente_id': 'count'
        }).round(2)
        cancelamento_stats.columns = ['Eng. Médio', 'Gasto Médio', 'Compras Médias', 'Qtd Clientes']
        print(cancelamento_stats)
    
    if 'assinante_clube' in cliente_completo.columns:
        print("\n⭐ Por Tipo de Assinatura:")
        assinatura_stats = cliente_completo.groupby('assinante_clube').agg({
            'pontuacao_engajamento': 'mean',
            'total_gasto': 'mean',
            'n_compras': 'mean',
            'cliente_id': 'count'
        }).round(2)
        assinatura_stats.columns = ['Eng. Médio', 'Gasto Médio', 'Compras Médias', 'Qtd Clientes']
        print(assinatura_stats)
    
    # ========== TOP RANKINGS ==========
    print("\n\n🏆 TOP RANKINGS")
    print("-" * 60)
    
    print("\n💎 Top 5 Clientes por Faturamento:")
    top_clientes = cliente_completo.nlargest(5, 'total_gasto')[
        ['cliente_id', 'nome', 'cidade', 'total_gasto', 'n_compras', 'pontuacao_engajamento']
    ] if 'nome' in cliente_completo.columns else cliente_completo.nlargest(5, 'total_gasto')[
        ['cliente_id', 'total_gasto', 'n_compras']
    ]
    print(top_clientes)
    
    # Produtos mais vendidos
    if 'produto_id' in compras_produtos.columns:
        vendas_produto = compras_produtos.groupby(['produto_id', 'nome']).agg({
            'valor': 'sum',
            'quantidade': 'sum'
        }).reset_index().sort_values('valor', ascending=False)
        
        print("\n🍷 Top 5 Produtos por Faturamento:")
        print(vendas_produto.head())
    
    # Vendas por tipo de uva
    if 'tipo_uva' in compras_produtos.columns:
        vendas_uva = compras_produtos.groupby('tipo_uva')['valor'].sum().sort_values(ascending=False)
        print("\n🍇 Top 5 Tipos de Uva por Faturamento:")
        print(vendas_uva.head())
    
    # Vendas por país
    if 'pais' in compras_produtos.columns:
        vendas_pais = compras_produtos.groupby('pais')['valor'].sum().sort_values(ascending=False)
        print("\n🌎 Top 5 Países por Faturamento:")
        print(vendas_pais.head())
    
    print("\n\n✅ Análise concluída!")
    print("=" * 60)
    
    return cliente_completo, compras_completo


def generate_summary_json(cliente_completo):
    """Gera um JSON com resumo estatístico"""
    
    summary = {
        "data_analise": datetime.now().isoformat(),
        "total_clientes": int(len(cliente_completo)),
        "estatisticas_engajamento": {
            "media": float(cliente_completo['pontuacao_engajamento'].mean()) if 'pontuacao_engajamento' in cliente_completo.columns else None,
            "min": float(cliente_completo['pontuacao_engajamento'].min()) if 'pontuacao_engajamento' in cliente_completo.columns else None,
            "max": float(cliente_completo['pontuacao_engajamento'].max()) if 'pontuacao_engajamento' in cliente_completo.columns else None,
        },
        "estatisticas_financeiras": {
            "total_gasto_medio": float(cliente_completo['total_gasto'].mean()),
            "total_gasto_min": float(cliente_completo['total_gasto'].min()),
            "total_gasto_max": float(cliente_completo['total_gasto'].max()),
            "ticket_medio": float(cliente_completo['ticket_medio'].mean()),
        },
        "segmentacao": {
            "cancelamentos": cliente_completo['cancelou_assinatura'].value_counts().to_dict() if 'cancelou_assinatura' in cliente_completo.columns else {},
            "assinantes_clube": cliente_completo['assinante_clube'].value_counts().to_dict() if 'assinante_clube' in cliente_completo.columns else {},
        }
    }
    
    with open(PROCESSED_DIR / "summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resumo salvo em: {PROCESSED_DIR / 'summary.json'}")


def main():
    """Função principal"""
    print("\n" + "=" * 60)
    print("🍷 WINEBRAIN - PROCESSAMENTO DE DADOS")
    print("=" * 60)
    
    try:
        # Carregar dados
        clientes, compras, produtos = load_excel_data()
        
        # Salvar em CSV
        save_to_csv(clientes, compras, produtos)
        
        # Analisar dados
        cliente_completo, compras_completo = analyze_data(clientes, compras, produtos)
        
        # Gerar resumo JSON
        generate_summary_json(cliente_completo)
        
        print("\n✨ Processamento concluído com sucesso! ✨\n")
        
    except Exception as e:
        print(f"\n❌ Erro no processamento: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
