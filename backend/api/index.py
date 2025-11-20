"""
API Principal do WineBrain - Versão Serverless Otimizada para Vercel
FastAPI sem dependências pesadas de ML
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import sys
import os

# Tentar importar pandas com tratamento de erro
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError as e:
    PANDAS_AVAILABLE = False
    print(f"Pandas não disponível: {e}")

from pathlib import Path

# Configuração
app = FastAPI(
    title="WineBrain API",
    description="Sistema de Apoio à Decisão para Adega Bom Sabor",
    version="1.0.0",
    docs_url="/docs"
)

# CORS
frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
allowed_origins = [
    "http://localhost:3000",
    "http://localhost:3001",
    frontend_url,
    "https://*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dados em memória
clientes_df = None
produtos_df = None
compras_df = None

# Modelos Pydantic
class ClienteResponse(BaseModel):
    cliente_id: int
    nome: str
    idade: int
    cidade: str
    pontuacao_engajamento: float
    assinante_clube: bool
    cancelou: bool
    total_gasto: float
    ticket_medio: float
    n_compras: int

class AcaoRecomendada(BaseModel):
    acao: str
    descricao: str
    prioridade: str

class RecomendacaoResponse(BaseModel):
    cliente_id: int
    segmento: str
    prioridade: str
    probabilidade_churn: float
    acoes_recomendadas: List[AcaoRecomendada]
    metricas: Dict[str, Any]
    mensagem: str

class DashboardStats(BaseModel):
    total_clientes: int
    receita_total: float
    ticket_medio: float
    taxa_cancelamento: float
    engajamento_medio: float
    total_clube: int

# Funções auxiliares
def calcular_probabilidade_churn(cliente: pd.Series) -> float:
    """Calcula probabilidade de churn baseada em regras"""
    score = 0.0
    
    if cliente['cancelou']:
        return 0.95
    
    if cliente['pontuacao_engajamento'] < 4:
        score += 0.4
    elif cliente['pontuacao_engajamento'] < 6:
        score += 0.2
    
    if cliente['n_compras'] <= 2:
        score += 0.3
    
    if not cliente['assinante_clube']:
        score += 0.1
    
    return min(score, 0.99)

def avaliar_cliente(cliente: pd.Series) -> Dict[str, Any]:
    """Avalia cliente e retorna recomendações"""
    prob_churn = calcular_probabilidade_churn(cliente)
    acoes = []
    prioridade = "baixa"
    
    # Regra 1: Cliente Premium
    if cliente['assinante_clube'] and cliente['pontuacao_engajamento'] >= 8:
        acoes.extend([
            {"acao": "recomendar_vinhos_premium", "descricao": "Oferecer vinhos premium exclusivos", "prioridade": "alta"},
            {"acao": "convidar_eventos_exclusivos", "descricao": "Convite para degustações VIP", "prioridade": "alta"}
        ])
        prioridade = "alta"
        segmento = "Premium"
        mensagem = "✨ Cliente Premium - Manter engajamento alto"
    
    # Regra 2: Risco de Cancelamento
    elif cliente['cancelou'] or cliente['pontuacao_engajamento'] < 4:
        acoes.extend([
            {"acao": "enviar_cupom_reativacao", "descricao": "Cupom de 20% de desconto", "prioridade": "critica"},
            {"acao": "enviar_pesquisa_satisfacao", "descricao": "Pesquisa para entender motivos", "prioridade": "critica"}
        ])
        prioridade = "critica"
        segmento = "Em Risco"
        mensagem = "⚠️ Cliente em risco de cancelamento - Ação imediata necessária"
    
    # Regra 3: Oportunidade de Upgrade
    elif 4 <= cliente['pontuacao_engajamento'] <= 7 and cliente['n_compras'] > 3:
        acoes.append(
            {"acao": "oferecer_upgrade_clube", "descricao": "Convidar para o clube de vinhos", "prioridade": "media"}
        )
        prioridade = "media"
        segmento = "Potencial"
        mensagem = "📈 Oportunidade de upgrade para clube"
    
    # Regra 4: Conversão para Clube
    elif not cliente['assinante_clube'] and cliente['total_gasto'] > clientes_df['total_gasto'].mean():
        acoes.append(
            {"acao": "recomendar_adesao_clube", "descricao": "Apresentar benefícios do clube", "prioridade": "alta"}
        )
        prioridade = "alta"
        segmento = "Alto Valor"
        mensagem = "💎 Cliente de alto valor - Converter para clube"
    
    # Regra 5: Alto Risco ML
    elif prob_churn >= 0.7:
        acoes.append(
            {"acao": "ativar_campanha_reengajamento", "descricao": "Campanha personalizada", "prioridade": "critica"}
        )
        prioridade = "critica"
        segmento = "Alto Risco"
        mensagem = "🚨 Alto risco de churn detectado"
    
    # Regra 6: Cliente Inativo
    elif cliente['n_compras'] <= 2 and cliente['pontuacao_engajamento'] < 4:
        acoes.append(
            {"acao": "incluir_programa_fidelidade", "descricao": "Newsletter e degustações", "prioridade": "media"}
        )
        prioridade = "media"
        segmento = "Inativo"
        mensagem = "💤 Cliente inativo - Reativar relacionamento"
    
    else:
        acoes.append(
            {"acao": "nenhuma_acao", "descricao": "Manter relacionamento padrão", "prioridade": "baixa"}
        )
        prioridade = "baixa"
        segmento = "Regular"
        mensagem = "✓ Cliente regular - Manter acompanhamento padrão"
    
    return {
        "segmento": segmento,
        "prioridade": prioridade,
        "probabilidade_churn": prob_churn,
        "acoes_recomendadas": acoes,
        "mensagem": mensagem,
        "metricas": {
            "engajamento": float(cliente['pontuacao_engajamento']),
            "n_compras": int(cliente['n_compras']),
            "total_gasto": float(cliente['total_gasto']),
            "clube": bool(cliente['assinante_clube'])
        }
    }

def carregar_dados():
    """Carrega dados com fallback para múltiplos caminhos"""
    global clientes_df, produtos_df, compras_df
    
    if not PANDAS_AVAILABLE:
        print("⚠️ Pandas não disponível - dados não serão carregados")
        return
    
    # Tentar múltiplos caminhos possíveis
    possible_paths = [
        Path(__file__).parent.parent / "app_data",  # Caminho local
        Path("/var/task/app_data"),  # Vercel serverless
        Path("./app_data"),  # Relativo
        Path("/var/task") / "app_data",  # Vercel alternativo
    ]
    
    data_dir = None
    for path in possible_paths:
        print(f"Verificando caminho: {path} (existe: {path.exists()})")
        if path.exists():
            data_dir = path
            print(f"✓ Caminho encontrado: {data_dir}")
            break
    
    if data_dir is None:
        print(f"⚠️ Nenhum diretório de dados encontrado.")
        print(f"   Current dir: {Path.cwd()}")
        print(f"   File location: {Path(__file__).resolve()}")
        # Listar arquivos no diretório atual
        try:
            print(f"   Arquivos em /var/task: {list(Path('/var/task').iterdir()) if Path('/var/task').exists() else 'N/A'}")
        except Exception as e:
            print(f"   Erro ao listar: {e}")
        return
    
    try:
        clientes_df = pd.read_csv(data_dir / "processed" / "clientes_agregado.csv")
        produtos_df = pd.read_csv(data_dir / "raw" / "produtos.csv")
        compras_df = pd.read_csv(data_dir / "raw" / "compras.csv")
        
        # Conversões
        clientes_df['assinante_clube'] = clientes_df['assinante_clube'].map({'Sim': True, 'Não': False})
        clientes_df['cancelou'] = clientes_df['cancelou'].map({'Sim': True, 'Não': False})
        clientes_df = clientes_df.fillna(0)
        
        print(f"✓ Dados carregados com sucesso de {data_dir}")
        print(f"  - {len(clientes_df)} clientes")
        print(f"  - {len(produtos_df)} produtos")
        print(f"  - {len(compras_df)} compras")
    except Exception as e:
        print(f"✗ Erro ao carregar dados: {e}")
        import traceback
        traceback.print_exc()

@app.on_event("startup")
async def startup_event():
    """Carrega dados na inicialização"""
    try:
        print("=== Iniciando carregamento de dados ===")
        carregar_dados()
        print("=== Carregamento concluído ===")
    except Exception as e:
        print(f"✗ Erro no startup: {e}")
        import traceback
        traceback.print_exc()

# Endpoints
@app.get("/")
async def root():
    """Endpoint raiz com informações de debug"""
    return {
        "app": "WineBrain API",
        "version": "1.0.0",
        "status": "online",
        "pandas_available": PANDAS_AVAILABLE,
        "python_version": sys.version,
        "current_dir": str(Path.cwd()),
        "file_location": str(Path(__file__).resolve())
    }

@app.get("/api/health")
async def health_check():
    """Health check com informações detalhadas"""
    health_info = {
        "status": "healthy",
        "pandas_available": PANDAS_AVAILABLE,
        "data_loaded": clientes_df is not None if PANDAS_AVAILABLE else False,
    }
    
    if PANDAS_AVAILABLE and clientes_df is not None:
        health_info["total_clientes"] = len(clientes_df)
    
    # Verificar caminhos de dados
    possible_paths = [
        Path(__file__).parent.parent / "app_data",
        Path("/var/task/app_data"),
        Path("./app_data"),
    ]
    
    health_info["checked_paths"] = [
        {"path": str(p), "exists": p.exists()} for p in possible_paths
    ]
    
    return health_info

@app.get("/api/dashboard/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    return DashboardStats(
        total_clientes=len(clientes_df),
        receita_total=float(clientes_df['total_gasto'].sum()),
        ticket_medio=float(clientes_df['ticket_medio'].mean()),
        taxa_cancelamento=float((clientes_df['cancelou'].sum() / len(clientes_df)) * 100),
        engajamento_medio=float(clientes_df['pontuacao_engajamento'].mean()),
        total_clube=int(clientes_df['assinante_clube'].sum())
    )

@app.get("/api/dashboard/top-clientes")
async def get_top_clientes(limit: int = Query(10, ge=1, le=100)):
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    top = clientes_df.nlargest(limit, 'total_gasto')[['cliente_id', 'nome', 'total_gasto']]
    return top.to_dict('records')

@app.get("/api/dashboard/produtos/top")
async def get_top_produtos(limit: int = Query(10, ge=1, le=100)):
    if compras_df is None or produtos_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    vendas = compras_df.merge(produtos_df, on='produto_id')
    vendas['valor_total'] = vendas['quantidade'] * vendas['preco']
    top = vendas.groupby(['produto_id', 'nome']).agg({
        'quantidade': 'sum',
        'valor_total': 'sum'
    }).reset_index().nlargest(limit, 'valor_total')
    
    return top.to_dict('records')

@app.get("/api/dashboard/vendas/{tipo}")
async def get_vendas_por_tipo(tipo: str):
    if compras_df is None or produtos_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    vendas = compras_df.merge(produtos_df, on='produto_id')
    vendas['valor_total'] = vendas['quantidade'] * vendas['preco']
    
    if tipo == "tipo-uva":
        resultado = vendas.groupby('tipo_uva')['valor_total'].sum().sort_values(ascending=False)
    elif tipo == "pais":
        resultado = vendas.groupby('pais_origem')['valor_total'].sum().sort_values(ascending=False)
    else:
        raise HTTPException(status_code=400, detail="Tipo inválido")
    
    return resultado.to_dict()

@app.get("/api/analytics/segmentacao")
async def get_segmentacao():
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    bins = [0, 4, 7, 10]
    labels = ['Baixo (0-4)', 'Médio (4-7)', 'Alto (7-10)']
    clientes_df['nivel_engajamento'] = pd.cut(
        clientes_df['pontuacao_engajamento'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )
    
    segmentacao = clientes_df.groupby('nivel_engajamento', observed=True).agg({
        'cliente_id': 'count',
        'total_gasto': 'mean',
        'n_compras': 'mean'
    }).reset_index()
    
    segmentacao.columns = ['nivel_engajamento', 'quantidade', 'gasto_medio', 'compras_medias']
    return segmentacao.to_dict('records')

@app.get("/api/clientes", response_model=List[ClienteResponse])
async def get_clientes(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    clientes = clientes_df.iloc[offset:offset+limit]
    return clientes.to_dict('records')

@app.get("/api/clientes/{cliente_id}", response_model=ClienteResponse)
async def get_cliente(cliente_id: int):
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    cliente = clientes_df[clientes_df['cliente_id'] == cliente_id]
    if cliente.empty:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    return cliente.iloc[0].to_dict()

@app.get("/api/clientes/{cliente_id}/recomendacao", response_model=RecomendacaoResponse)
async def get_recomendacao(cliente_id: int):
    if clientes_df is None:
        raise HTTPException(status_code=503, detail="Dados não carregados")
    
    cliente = clientes_df[clientes_df['cliente_id'] == cliente_id]
    if cliente.empty:
        raise HTTPException(status_code=404, detail="Cliente não encontrado")
    
    resultado = avaliar_cliente(cliente.iloc[0])
    resultado['cliente_id'] = cliente_id
    
    return resultado

# Handler para Vercel
handler = app
