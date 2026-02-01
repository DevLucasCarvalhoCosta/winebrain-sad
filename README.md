<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/React-18+-61DAFB?style=for-the-badge&logo=react&logoColor=black" alt="React"/>
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI"/>
  <img src="https://img.shields.io/badge/Scikit--Learn-ML-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn"/>
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License"/>
</p>

<h1 align="center">🍷 WineBrain</h1>

<p align="center">
  <strong>Sistema de Apoio à Decisão Inteligente para Gestão de Clientes</strong>
</p>

<p align="center">
  Sistema completo end-to-end que combina Machine Learning e Regras de Negócio para otimizar a retenção de clientes e maximizar resultados comerciais.
</p>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Funcionalidades](#-funcionalidades)
- [Arquitetura](#-arquitetura)
- [Tecnologias](#-tecnologias)
- [Instalação](#-instalação)
- [Uso](#-uso)
- [API Reference](#-api-reference)
- [Modelos de Decisão](#-modelos-de-decisão)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Licença](#-licença)

---

## 🎯 Sobre o Projeto

### Contexto

O **WineBrain** foi desenvolvido para resolver desafios críticos de negócio enfrentados por empresas do setor de varejo de vinhos:

| Desafio | Impacto | Solução WineBrain |
|---------|---------|-------------------|
| Alta taxa de churn (33%) | Perda de receita recorrente | Predição ML + ações preventivas |
| Recomendações genéricas | Baixa conversão | Personalização via regras de negócio |
| Clientes inativos (40%) | ROI de marketing baixo | Segmentação inteligente + reativação |

### Proposta de Valor

O sistema implementa um **SAD (Sistema de Apoio à Decisão)** completo que:

- 📊 **Diagnostica** a situação atual com dashboards e KPIs
- 🔮 **Prediz** comportamentos futuros usando Machine Learning
- 💡 **Prescreve** ações específicas baseadas em regras de negócio
- 📈 **Simula** cenários e projeta impacto de decisões

---

## ✨ Funcionalidades

### Dashboard Executivo
- KPIs em tempo real (clientes, receita, ticket médio)
- Gráficos interativos de vendas por categoria
- Ranking de top clientes e produtos
- Análise de segmentação de engajamento

### Gestão de Clientes
- Listagem com busca e filtros avançados
- Badges visuais de status (engajamento, risco, clube)
- Navegação para análise individual detalhada

### Análise Inteligente por Cliente
- Perfil completo com histórico de compras
- **Probabilidade de Churn** calculada por ML
- **Recomendações automáticas** priorizadas
- Justificativas claras para cada ação sugerida

### API RESTful Documentada
- 11 endpoints para integração
- Documentação Swagger automática
- Validação robusta de dados

---

## 🏗 Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (React + Vite)                   │
│         Dashboard • Clientes • Análise Individual           │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (FastAPI)                         │
│                  Endpoints • Validação                      │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                  CAMADA DE INTELIGÊNCIA                     │
│  ┌─────────────────────┐    ┌─────────────────────┐        │
│  │    ML Engine        │    │    Rule Engine      │        │
│  │  Random Forest      │───▶│    6 Regras         │        │
│  │  Predição Churn     │    │    Priorização      │        │
│  └─────────────────────┘    └─────────────────────┘        │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      DADOS (CSV)                            │
│           Clientes • Compras • Produtos                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tecnologias

### Backend
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.10+ | Linguagem principal |
| FastAPI | 0.100+ | Framework web assíncrono |
| Scikit-learn | 1.3+ | Machine Learning |
| Pandas | 2.0+ | Processamento de dados |
| Pydantic | 2.0+ | Validação de schemas |

### Frontend
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| React | 18+ | Interface de usuário |
| Vite | 4+ | Build tool |
| Tailwind CSS | 3+ | Estilização |
| Recharts | 2.5+ | Visualização de dados |
| Axios | 1.4+ | Cliente HTTP |

---

## 🚀 Instalação

### Pré-requisitos

- Python 3.10+
- Node.js 18+
- Git

### Passo a Passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/winebrain-sad.git
cd winebrain-sad

# 2. Configure o Backend
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac
pip install -r requirements.txt
cd ..

# 3. Processe os dados e treine o modelo
python backend/load_data.py

# 4. Configure o Frontend
cd frontend
npm install
cd ..
```

---

## 💻 Uso

### Iniciar o Sistema

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python run.py
```
> API disponível em: http://localhost:8000

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```
> Interface disponível em: http://localhost:3000

### Acessos Rápidos

| Recurso | URL |
|---------|-----|
| Interface Web | http://localhost:3000 |
| API REST | http://localhost:8000 |
| Documentação API | http://localhost:8000/docs |

---

## 📡 API Reference

### Endpoints Principais

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/health` | Status da API |
| GET | `/api/dashboard/stats` | KPIs do dashboard |
| GET | `/api/dashboard/top-clientes` | Top clientes por faturamento |
| GET | `/api/dashboard/produtos/top` | Top produtos |
| GET | `/api/clientes` | Lista de clientes (paginada) |
| GET | `/api/clientes/{id}` | Dados de um cliente |
| GET | `/api/clientes/{id}/recomendacao` | Recomendações IA para cliente |
| GET | `/api/analytics/segmentacao` | Segmentação de clientes |

### Exemplo de Response

```json
GET /api/clientes/1/recomendacao

{
  "cliente_id": 1,
  "segmento": "Em Risco",
  "probabilidade_churn": 0.78,
  "prioridade": "critica",
  "acoes_recomendadas": [
    {
      "acao": "enviar_cupom_reativacao",
      "descricao": "Cupom de 20% de desconto",
      "prioridade": "critica"
    }
  ],
  "mensagem": "Cliente em risco de cancelamento - Ação imediata necessária"
}
```

---

## 🧠 Modelos de Decisão

O WineBrain implementa os 4 tipos clássicos de modelos de decisão:

### 1. Modelo Descritivo
> "O que está acontecendo?"

- Dashboard com estatísticas históricas
- Gráficos de vendas e rankings
- Segmentação por engajamento

### 2. Modelo Preditivo
> "O que vai acontecer?"

- Algoritmo: **Random Forest Classifier**
- Target: Probabilidade de churn
- Features: engajamento, gasto total, frequência de compras, etc.
- Métricas: ~85% acurácia, ~81% F1-Score

### 3. Modelo Prescritivo
> "O que fazer?"

Motor de regras com 6 regras de negócio:

| Regra | Condição | Ação |
|-------|----------|------|
| Cliente Premium | Clube + Engajamento ≥ 8 | Vinhos exclusivos, eventos VIP |
| Risco Cancelamento | Cancelou ou Engajamento < 4 | Cupom 20%, contato urgente |
| Oportunidade Upgrade | Engajamento 4-7, Compras > 3 | Propor upgrade de plano |
| Conversão Clube | Não-assinante, Gasto > média | Apresentar benefícios do clube |
| Alto Risco Churn | Prob. churn ≥ 70% | Campanha reengajamento |
| Cliente Inativo | Compras ≤ 2, Engajamento < 4 | Programa de reativação |

### 4. Modelo Simulativo
> "E se...?"

- Projeção de impacto de ações
- Análise de cenários de desconto
- Cálculo de ROI esperado

---

## 📁 Estrutura do Projeto

```
winebrain-sad/
├── backend/
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py              # API FastAPI
│   ├── knowledge_base/
│   │   ├── __init__.py
│   │   └── rules.py             # Motor de regras
│   ├── models/
│   │   ├── __init__.py
│   │   └── churn_model.py       # Modelo ML
│   ├── app_data/                # Dados processados
│   ├── load_data.py             # ETL
│   ├── run.py                   # Entrypoint
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Clientes.jsx
│   │   │   └── ClienteDetalhes.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
├── docs/                        # Documentação adicional
├── .gitignore
├── LICENSE
└── README.md
```

---

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<p align="center">
  Desenvolvido com ❤️ para demonstração de Sistema de Apoio à Decisão
</p>
