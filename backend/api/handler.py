"""
WineBrain API - Handler principal para Vercel
Versão otimizada sem Pandas - usando CSV nativo
"""
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from pathlib import Path
import csv
import json

app = FastAPI(
    title="WineBrain API",
    description="Sistema de Apoio à Decisão para Adega Bom Sabor",
    version="1.0.0",
    docs_url="/docs"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dados em memória
clientes_data = []
produtos_data = []
compras_data = []
dados_carregados = False

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

def carregar_csv(filepath):
    """Carrega CSV e retorna lista de dicts"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
    except Exception:
        return []

def carregar_dados():
    """Carrega dados dos CSVs"""
    global clientes_data, produtos_data, compras_data, dados_carregados
    
    if dados_carregados:
        return True
    
    possible_paths = [
        Path(__file__).parent.parent / "app_data",
        Path("/var/task/app_data"),
        Path("./app_data"),
    ]
    
    data_dir = None
    for path in possible_paths:
        try:
            if path.exists():
                data_dir = path
                break
        except Exception:
            continue
    
    if data_dir is None:
        return False
    
    try:
        clientes_data = carregar_csv(data_dir / "processed" / "clientes_agregado.csv")
        produtos_data = carregar_csv(data_dir / "raw" / "produtos.csv")
        compras_data = carregar_csv(data_dir / "raw" / "compras.csv")
        
        # Converter tipos
        for c in clientes_data:
            c['cliente_id'] = int(c['cliente_id'])
            c['idade'] = int(c['idade'])
            c['pontuacao_engajamento'] = float(c['pontuacao_engajamento'])
            c['assinante_clube'] = c['assinante_clube'] == 'Sim'
            c['cancelou'] = c['cancelou'] == 'Sim'
            c['total_gasto'] = float(c['total_gasto'])
            c['ticket_medio'] = float(c['ticket_medio'])
            c['n_compras'] = int(c['n_compras'])
        
        dados_carregados = True
        return True
    except Exception:
        return False

def calcular_probabilidade_churn(cliente):
    """Calcula probabilidade de churn"""
    if cliente['cancelou']:
        return 0.95
    
    score = 0.0
    if cliente['pontuacao_engajamento'] < 4:
        score += 0.4
    elif cliente['pontuacao_engajamento'] < 6:
        score += 0.2
    
    if cliente['n_compras'] <= 2:
        score += 0.3
    
    if not cliente['assinante_clube']:
        score += 0.1
    
    return min(score, 0.99)

def avaliar_cliente(cliente):
    """Avalia cliente e retorna recomendações"""
    prob_churn = calcular_probabilidade_churn(cliente)
    acoes = []
    
    if cliente['assinante_clube'] and cliente['pontuacao_engajamento'] >= 8:
        acoes.extend([
            {"acao": "recomendar_vinhos_premium", "descricao": "Oferecer vinhos premium exclusivos", "prioridade": "alta"},
            {"acao": "convidar_eventos_exclusivos", "descricao": "Convite para degustações VIP", "prioridade": "alta"}
        ])
        prioridade = "alta"
        segmento = "Premium"
        mensagem = "✨ Cliente Premium - Manter engajamento alto"
    elif cliente['cancelou'] or cliente['pontuacao_engajamento'] < 4:
        acoes.extend([
            {"acao": "enviar_cupom_reativacao", "descricao": "Cupom de 20% de desconto", "prioridade": "critica"},
            {"acao": "enviar_pesquisa_satisfacao", "descricao": "Pesquisa para entender motivos", "prioridade": "critica"}
        ])
        prioridade = "critica"
        segmento = "Em Risco"
        mensagem = "⚠️ Cliente em risco de cancelamento"
    elif 4 <= cliente['pontuacao_engajamento'] <= 7 and cliente['n_compras'] > 3:
        acoes.append({"acao": "oferecer_upgrade_clube", "descricao": "Convidar para o clube de vinhos", "prioridade": "media"})
        prioridade = "media"
        segmento = "Potencial"
        mensagem = "📈 Oportunidade de upgrade para clube"
    elif not cliente['assinante_clube'] and cliente['total_gasto'] > 150:
        acoes.append({"acao": "recomendar_adesao_clube", "descricao": "Apresentar benefícios do clube", "prioridade": "alta"})
        prioridade = "alta"
        segmento = "Alto Valor"
        mensagem = "💎 Cliente de alto valor - Converter para clube"
    elif prob_churn >= 0.7:
        acoes.append({"acao": "ativar_campanha_reengajamento", "descricao": "Campanha personalizada", "prioridade": "critica"})
        prioridade = "critica"
        segmento = "Alto Risco"
        mensagem = "🚨 Alto risco de churn detectado"
    elif cliente['n_compras'] <= 2 and cliente['pontuacao_engajamento'] < 4:
        acoes.append({"acao": "incluir_programa_fidelidade", "descricao": "Newsletter e degustações", "prioridade": "media"})
        prioridade = "media"
        segmento = "Inativo"
        mensagem = "💤 Cliente inativo - Reativar relacionamento"
    else:
        acoes.append({"acao": "nenhuma_acao", "descricao": "Manter relacionamento padrão", "prioridade": "baixa"})
        prioridade = "baixa"
        segmento = "Regular"
        mensagem = "✓ Cliente regular"
    
    return {
        "segmento": segmento,
        "prioridade": prioridade,
        "probabilidade_churn": prob_churn,
        "acoes_recomendadas": acoes,
        "mensagem": mensagem,
        "metricas": {
            "engajamento": cliente['pontuacao_engajamento'],
            "n_compras": cliente['n_compras'],
            "total_gasto": cliente['total_gasto'],
            "clube": cliente['assinante_clube']
        }
    }

@app.get("/")
def root():
    return {"app": "WineBrain API", "version": "1.0.0", "status": "online"}

@app.get("/api/health")
def health():
    carregar_dados()
    return {
        "status": "healthy",
        "data_loaded": dados_carregados,
        "total_clientes": len(clientes_data)
    }

@app.get("/api/dashboard/stats", response_model=DashboardStats)
def get_stats():
    carregar_dados()
    if not dados_carregados:
        raise HTTPException(503, "Dados não carregados")
    
    total = len(clientes_data)
    receita = sum(c['total_gasto'] for c in clientes_data)
    ticket = sum(c['ticket_medio'] for c in clientes_data) / total
    cancelados = sum(1 for c in clientes_data if c['cancelou'])
    engajamento = sum(c['pontuacao_engajamento'] for c in clientes_data) / total
    clube = sum(1 for c in clientes_data if c['assinante_clube'])
    
    return DashboardStats(
        total_clientes=total,
        receita_total=receita,
        ticket_medio=ticket,
        taxa_cancelamento=(cancelados / total) * 100,
        engajamento_medio=engajamento,
        total_clube=clube
    )

@app.get("/api/clientes", response_model=List[ClienteResponse])
def get_clientes(limit: int = Query(100, ge=1, le=1000), offset: int = Query(0, ge=0)):
    carregar_dados()
    if not dados_carregados:
        raise HTTPException(503, "Dados não carregados")
    return clientes_data[offset:offset+limit]

@app.get("/api/clientes/{cliente_id}", response_model=ClienteResponse)
def get_cliente(cliente_id: int):
    carregar_dados()
    if not dados_carregados:
        raise HTTPException(503, "Dados não carregados")
    
    cliente = next((c for c in clientes_data if c['cliente_id'] == cliente_id), None)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")
    return cliente

@app.get("/api/clientes/{cliente_id}/recomendacao", response_model=RecomendacaoResponse)
def get_recomendacao(cliente_id: int):
    carregar_dados()
    if not dados_carregados:
        raise HTTPException(503, "Dados não carregados")
    
    cliente = next((c for c in clientes_data if c['cliente_id'] == cliente_id), None)
    if not cliente:
        raise HTTPException(404, "Cliente não encontrado")
    
    resultado = avaliar_cliente(cliente)
    resultado['cliente_id'] = cliente_id
    return resultado

# Handler para Vercel
handler = app
