"""
API Principal do WineBrain
FastAPI para servir o Sistema de Apoio à Decisão
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import pandas as pd
from pathlib import Path
import sys
import os

# Adicionar diretório pai ao path
sys.path.append(str(Path(__file__).parent.parent))

from knowledge_base.rules import rule_engine, AcaoRecomendada, NivelPrioridade
from models.churn_model import ChurnPredictor

# Configuração
app = FastAPI(
    title="WineBrain API",
    description="Sistema de Apoio à Decisão para Adega Bom Sabor",
    version="1.0.0",
    redoc_url=None,  # Desabilitar URL padrão
    docs_url="/docs"
)

# CORS - Configuração para localhost e Vercel
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    frontend_url,
    "https://*.vercel.app"  # Permite todos os domínios da Vercel
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ReDoc customizado com CDN estável
from fastapi.openapi.docs import get_redoc_html

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
    )

# Caminhos - Usar app_data para deploy na Vercel
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "app_data"
MODEL_DIR = DATA_DIR / "models"

# Carregar dados globais
clientes_df = None
produtos_df = None
compras_df = None
churn_predictor = None


# ========== MODELS (Pydantic) ==========

class ClienteResponse(BaseModel):
    cliente_id: int
    nome: Optional[str] = None
    idade: Optional[int] = None
    cidade: Optional[str] = None
    pontuacao_engajamento: float
    assinante_clube: bool
    cancelou_assinatura: bool
    total_gasto: float
    n_compras: int
    ticket_medio: float


class RecomendacaoResponse(BaseModel):
    cliente_id: int
    segmento: str
    nivel_engajamento: str
    probabilidade_churn: float
    acoes_recomendadas: List[Dict[str, Any]]
    prioridade: str
    mensagem: str
    metricas: Dict[str, Any]


class DashboardStats(BaseModel):
    total_clientes: int
    total_produtos: int
    total_compras: int
    receita_total: float
    ticket_medio: float
    clientes_ativos: int
    clientes_clube: int
    taxa_cancelamento: float


# ========== STARTUP ==========

@app.on_event("startup")
async def startup_event():
    """Carrega dados e modelo na inicialização"""
    global clientes_df, produtos_df, compras_df, churn_predictor
    
    try:
        # Carregar dados
        clientes_df = pd.read_csv(DATA_DIR / "processed" / "clientes_agregado.csv")
        produtos_df = pd.read_csv(DATA_DIR / "raw" / "produtos.csv")
        compras_df = pd.read_csv(DATA_DIR / "raw" / "compras.csv")
        
        print("✅ Dados carregados com sucesso")
        
        # Carregar modelo de churn
        model_path = MODEL_DIR / "churn_model.pkl"
        if model_path.exists():
            churn_predictor = ChurnPredictor.load_model(str(model_path))
            print("✅ Modelo de churn carregado")
        else:
            print("⚠️ Modelo de churn não encontrado")
            
    except Exception as e:
        print(f"❌ Erro ao carregar dados: {e}")


# ========== ENDPOINTS ==========

@app.get("/")
async def root():
    """Endpoint raiz"""
    return {
        "message": "🍷 WineBrain API - Sistema de Apoio à Decisão",
        "version": "1.0.0",
        "status": "online"
    }


@app.get("/api/health")
async def health_check():
    """Verifica saúde da API"""
    return {
        "status": "healthy",
        "data_loaded": clientes_df is not None,
        "model_loaded": churn_predictor is not None
    }


@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Retorna estatísticas gerais para o dashboard"""
    
    if clientes_df is None or compras_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Converter strings para booleanos
    cancelou = clientes_df['cancelou_assinatura'].apply(lambda x: x == 'Sim' if isinstance(x, str) else bool(x))
    assinante = clientes_df['assinante_clube'].apply(lambda x: x == 'Sim' if isinstance(x, str) else bool(x))
    
    # Calcular estatísticas
    stats = {
        "total_clientes": int(len(clientes_df)),
        "total_produtos": int(len(produtos_df)),
        "total_compras": int(len(compras_df)),
        "receita_total": float(compras_df['valor'].sum()),
        "ticket_medio": float(clientes_df['ticket_medio'].mean()),
        "clientes_ativos": int((~cancelou).sum()),
        "clientes_clube": int(assinante.sum()),
        "taxa_cancelamento": float(cancelou.mean())
    }
    
    return stats


@app.get("/api/clientes", response_model=List[ClienteResponse])
async def get_clientes(
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0)
):
    """Lista clientes com paginação"""
    
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Paginar
    clientes_page = clientes_df.iloc[offset:offset+limit].copy()
    
    # Converter strings Sim/Não para booleanos
    if 'cancelou_assinatura' in clientes_page.columns:
        clientes_page['cancelou_assinatura'] = clientes_page['cancelou_assinatura'].apply(
            lambda x: x == 'Sim' if isinstance(x, str) else bool(x) if pd.notna(x) else False
        )
    if 'assinante_clube' in clientes_page.columns:
        clientes_page['assinante_clube'] = clientes_page['assinante_clube'].apply(
            lambda x: x == 'Sim' if isinstance(x, str) else bool(x) if pd.notna(x) else False
        )
    
    # Tratar NaN em strings
    string_cols = clientes_page.select_dtypes(include=['object']).columns
    clientes_page[string_cols] = clientes_page[string_cols].fillna('')
    
    # Tratar NaN em números
    numeric_cols = clientes_page.select_dtypes(include=['float64', 'int64']).columns
    clientes_page[numeric_cols] = clientes_page[numeric_cols].fillna(0)
    
    # Converter para lista de dicts
    clientes_list = clientes_page.to_dict('records')
    
    return clientes_list


@app.get("/api/clientes/{cliente_id}", response_model=ClienteResponse)
async def get_cliente(cliente_id: int):
    """Retorna dados de um cliente específico"""
    
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Buscar cliente
    cliente = clientes_df[clientes_df['cliente_id'] == cliente_id].copy()
    
    if len(cliente) == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    cliente_dict = cliente.iloc[0].to_dict()
    
    # Converter strings Sim/Não para booleanos
    if 'cancelou_assinatura' in cliente_dict:
        val = cliente_dict['cancelou_assinatura']
        cliente_dict['cancelou_assinatura'] = val == 'Sim' if isinstance(val, str) else bool(val) if pd.notna(val) else False
    if 'assinante_clube' in cliente_dict:
        val = cliente_dict['assinante_clube']
        cliente_dict['assinante_clube'] = val == 'Sim' if isinstance(val, str) else bool(val) if pd.notna(val) else False
    
    # Tratar NaN
    for key, value in cliente_dict.items():
        if pd.isna(value):
            if isinstance(value, (int, float)):
                cliente_dict[key] = 0
            else:
                cliente_dict[key] = ''
    
    return cliente_dict


@app.get("/api/clientes/{cliente_id}/recomendacao", response_model=RecomendacaoResponse)
async def get_recomendacao(cliente_id: int):
    """Gera recomendações para um cliente"""
    
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Buscar cliente
    cliente = clientes_df[clientes_df['cliente_id'] == cliente_id]
    
    if len(cliente) == 0:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    cliente_data = cliente.iloc[0].to_dict()
    
    # Predição de churn
    if churn_predictor:
        try:
            # Preparar features
            X = cliente[churn_predictor.feature_names]
            
            # Encoding se necessário
            for col in X.columns:
                if col in churn_predictor.label_encoders:
                    le = churn_predictor.label_encoders[col]
                    X[col] = le.transform(X[col].astype(str))
            
            # Predizer
            proba = churn_predictor.predict_proba(X)[0]
            cliente_data['probabilidade_churn'] = float(proba[1])
        except Exception as e:
            print(f"Erro na predição: {e}")
            cliente_data['probabilidade_churn'] = 0.0
    else:
        cliente_data['probabilidade_churn'] = 0.0
    
    # Valor médio geral (para comparação)
    cliente_data['valor_medio_geral'] = float(clientes_df['total_gasto'].mean())
    
    # Aplicar regras de negócio
    recomendacao = rule_engine.avaliar_cliente(cliente_data)
    
    return recomendacao


@app.get("/api/dashboard/top-clientes")
async def get_top_clientes(limit: int = Query(default=5, ge=1, le=20)):
    """Retorna top clientes por faturamento"""
    
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    top = clientes_df.nlargest(limit, 'total_gasto')[
        ['cliente_id', 'nome', 'cidade', 'total_gasto', 'n_compras', 'pontuacao_engajamento']
    ]
    
    # Substituir NaN por None para serialização JSON
    result = top.fillna('').to_dict('records')
    
    return result


@app.get("/api/dashboard/produtos/top")
async def get_top_produtos(limit: int = Query(default=5, ge=1, le=20)):
    """Retorna top produtos por faturamento"""
    
    if compras_df is None or produtos_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Merge e agregação
    vendas = compras_df.merge(produtos_df, on='produto_id')
    vendas_agg = vendas.groupby(['produto_id', 'nome']).agg({
        'valor': 'sum',
        'quantidade': 'sum'
    }).reset_index().sort_values('valor', ascending=False).head(limit)
    
    return vendas_agg.to_dict('records')


@app.get("/api/dashboard/produtos/ranking-detalhado")
async def get_ranking_produtos_detalhado(
    limit: int = Query(default=10, ge=1, le=50),
    ordenar_por: str = Query("valor", regex="^(valor|quantidade|ticket_medio)$")
):
    """
    Retorna ranking detalhado de produtos com todas as métricas
    
    Parâmetros:
    - limit: quantidade de produtos a retornar
    - ordenar_por: valor (receita), quantidade, ticket_medio
    """
    
    if compras_df is None or produtos_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Merge completo
    vendas = compras_df.merge(produtos_df, on='produto_id')
    
    # Agregação com todas as métricas
    ranking = vendas.groupby(['produto_id', 'nome', 'pais', 'safra', 'tipo_uva']).agg({
        'valor': 'sum',
        'quantidade': 'sum',
        'compra_id': 'count'
    }).reset_index()
    
    # Calcular ticket médio
    ranking['ticket_medio'] = ranking['valor'] / ranking['compra_id']
    ranking = ranking.rename(columns={'compra_id': 'num_vendas'})
    
    # Ordenar
    ranking = ranking.sort_values(ordenar_por, ascending=False).head(limit)
    
    # Formatar para JSON
    resultado = ranking.to_dict('records')
    
    # Converter valores para tipos corretos
    for item in resultado:
        item['valor'] = float(item['valor'])
        item['quantidade'] = int(item['quantidade'])
        item['ticket_medio'] = float(item['ticket_medio'])
        item['num_vendas'] = int(item['num_vendas'])
        item['safra'] = int(item['safra'])
    
    return resultado


@app.get("/api/dashboard/vendas/tipo-uva")
async def get_vendas_tipo_uva():
    """Retorna vendas por tipo de uva"""
    
    if compras_df is None or produtos_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Merge e agregação
    vendas = compras_df.merge(produtos_df, on='produto_id')
    vendas_uva = vendas.groupby('tipo_uva')['valor'].sum().sort_values(ascending=False)
    
    return vendas_uva.to_dict()


@app.get("/api/dashboard/vendas/pais")
async def get_vendas_pais():
    """Retorna vendas por país"""
    
    if compras_df is None or produtos_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Merge e agregação
    vendas = compras_df.merge(produtos_df, on='produto_id')
    vendas_pais = vendas.groupby('pais')['valor'].sum().sort_values(ascending=False)
    
    return vendas_pais.to_dict()


@app.get("/api/dashboard/vendas/temporal")
async def get_vendas_temporal(
    periodo: str = Query("mensal", regex="^(diario|semanal|mensal)$"),
    metrica: str = Query("valor", regex="^(valor|quantidade|ticket_medio|num_compras)$"),
    data_inicio: Optional[str] = None,
    data_fim: Optional[str] = None
):
    """
    Retorna vendas ao longo do tempo com filtros
    
    Parâmetros:
    - periodo: diario, semanal, mensal
    - metrica: valor (R$), quantidade (itens), ticket_medio, num_compras
    - data_inicio: formato YYYY-MM-DD (opcional)
    - data_fim: formato YYYY-MM-DD (opcional)
    """
    
    if compras_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Converter data_compra para datetime
    df = compras_df.copy()
    df['data_compra'] = pd.to_datetime(df['data_compra'])
    
    # Filtrar por período se especificado
    if data_inicio:
        df = df[df['data_compra'] >= pd.to_datetime(data_inicio)]
    if data_fim:
        df = df[df['data_compra'] <= pd.to_datetime(data_fim)]
    
    # Agrupar por período
    if periodo == "diario":
        df['periodo'] = df['data_compra'].dt.strftime('%Y-%m-%d')
    elif periodo == "semanal":
        # Formato: "02/01 a 08/01"
        df['inicio_semana'] = df['data_compra'] - pd.to_timedelta(df['data_compra'].dt.dayofweek, unit='d')
        df['fim_semana'] = df['inicio_semana'] + pd.Timedelta(days=6)
        df['periodo'] = df['inicio_semana'].dt.strftime('%d/%m') + ' a ' + df['fim_semana'].dt.strftime('%d/%m')
    else:  # mensal
        df['periodo'] = df['data_compra'].dt.to_period('M').astype(str)
    
    # Calcular métrica escolhida
    if metrica == "valor":
        resultado_df = df.groupby('periodo')['valor'].sum().reset_index()
        resultado_df.columns = ['periodo', 'valor']
    elif metrica == "quantidade":
        resultado_df = df.groupby('periodo')['quantidade'].sum().reset_index()
        resultado_df.columns = ['periodo', 'quantidade']
    elif metrica == "ticket_medio":
        agrupado = df.groupby('periodo').agg({'valor': 'sum', 'compra_id': 'count'}).reset_index()
        agrupado['ticket_medio'] = agrupado['valor'] / agrupado['compra_id']
        resultado_df = agrupado[['periodo', 'ticket_medio']]
    else:  # num_compras
        resultado_df = df.groupby('periodo')['compra_id'].count().reset_index()
        resultado_df.columns = ['periodo', 'num_compras']
    
    # Ordenar por período
    resultado_df = resultado_df.sort_values('periodo')
    
    # Formatar para o frontend
    resultado = resultado_df.to_dict('records')
    
    # Converter valores para float
    for item in resultado:
        for key, value in item.items():
            if key != 'periodo' and pd.notna(value):
                item[key] = float(value)
    
    # Log para debug
    print(f"📊 Vendas Temporal - Período: {periodo}, Métrica: {metrica}")
    print(f"   Total de registros retornados: {len(resultado)}")
    if len(resultado) > 0:
        print(f"   Primeiro: {resultado[0]}")
        print(f"   Último: {resultado[-1]}")
    
    return resultado


@app.get("/api/analytics/segmentacao")
async def get_segmentacao():
    """Retorna análise de segmentação de clientes"""
    
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    # Segmentação por engajamento
    def classify_engagement(score):
        # Converter para float se for string
        try:
            score_num = float(score) if isinstance(score, str) else score
        except (ValueError, TypeError):
            return "Desconhecido"
        
        if pd.isna(score_num):
            return "Desconhecido"
        elif score_num >= 8:
            return "Alto"
        elif score_num >= 4:
            return "Médio"
        else:
            return "Baixo"
    
    clientes_df['nivel_engajamento'] = clientes_df['pontuacao_engajamento'].apply(classify_engagement)
    
    segmentacao = clientes_df.groupby('nivel_engajamento').agg({
        'cliente_id': 'count',
        'total_gasto': 'mean',
        'n_compras': 'mean'
    }).reset_index()
    
    segmentacao.columns = ['nivel_engajamento', 'quantidade', 'gasto_medio', 'compras_medias']
    
    return segmentacao.to_dict('records')


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
