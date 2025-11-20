# WineBrain – Documento Técnico Integrado

Documento produzido em 19/11/2025 após análise integral do repositório `winebrain-sad`.

---

## 1. Visão Executivo-Estratégica
- **Objetivo de negócio**: reduzir churn (33% → 20%), elevar ticket médio (R$300 → R$450) e recuperar clientes inativos (40% da base) para a Adega Bom Sabor.
- **Abordagem**: Sistema de Apoio à Decisão (SAD) que combina modelos descritivo, preditivo, prescritivo e simulativo em uma única jornada dados → ML → regras → API → UI.
- **Indicadores atuais (summary.json)**: 100 clientes, engajamento médio 6,08 (1,63–9,88), gasto médio R$68,85 (máx. R$386,50), 45 cancelamentos ativos, 66 assinantes do clube.
- **Stack essencial**: FastAPI + Uvicorn, Pandas/Numpy/Openpyxl, Scikit-learn (Random Forest como modelo oficial), React 18 + Vite + Tailwind + Recharts.

### Valor entregue por camada
| Camada | Responsável | Motivo da escolha |
| --- | --- | --- |
| Processamento | `backend/load_data.py` | ETL declarativo (Excel→CSV), garante reprodutibilidade do dataset e geração de métricas usadas no relatório.
| Inteligência | `backend/models/churn_model.py` + `knowledge_base/rules.py` | Random Forest entrega melhor F1 em dados tabulares e o motor de regras torna as ações explicáveis para o time comercial.
| API | `backend/api/main.py` | FastAPI expõe endpoints tipados (Pydantic) com Swagger automático, reduzindo esforço de documentação.
| UI | `frontend/src` | React + Vite permitem HMR rápido em sala de aula e Tailwind reduz tempo de estilização mantendo consistência visual executiva.

---

## 2. Arquitetura End-to-End
```
┌─────────────────────────────┐
│ Camada de Apresentação     │ React 18 + Vite + Tailwind + Recharts
│  • Dashboard.jsx           │ KPIs e gráficos em tempo real
│  • Clientes.jsx            │ Lista com filtros e badges de risco
│  • ClienteDetalhes.jsx     │ Perfil + IA + recomendações
└───────────────┬────────────┘
                │ Axios REST (JSON)
┌───────────────▼────────────┐
│ Camada de API (FastAPI)    │ `backend/api/main.py`
│  • 11 endpoints HTTP       │ health, dashboard, clientes, analytics
│  • CORS + Pydantic + Docs  │ garante tipagem e contratos estáveis
└───────────────┬────────────┘
                │ Chamada síncrona em memória
┌───────────────▼────────────┐
│ Camada de Inteligência     │
│  • ChurnPredictor (ML)     │ probabilidade de cancelamento
│  • RuleEngine (Prescritivo)│ 6 regras com prioridades
└───────────────┬────────────┘
                │ Pandas DataFrames
┌───────────────▼────────────┐
│ Processamento & Dados      │ `data/raw`, `data/processed`, `data/models`
│  • ETL: load_data.py       │ Excel → CSV + agregações
│  • summary.json            │ estatísticas para auditoria
└────────────────────────────┘
```

### Fluxos principais
1. **Dashboard**: Frontend dispara `GET /api/dashboard/*` em paralelo → FastAPI agrega dados em memória (Pandas) → JSON alimenta KPIs, gráficos e tabelas.
2. **Recomendação individual**: `GET /api/clientes/{id}/recomendacao` → ChurnPredictor calcula `probabilidade_churn` → RuleEngine aplica regras → resposta contém segmento, prioridade e ações justificadas.

---

## 3. Pipeline de Dados e IA
| Etapa | Script/Função | Detalhes técnicos | Razão |
| --- | --- | --- | --- |
| 1. Coleta | `load_data.load_excel_data()` | Lê `docs/Cliente.xlsx`, `Compras.xlsx`, `produtos.xlsx` com Openpyxl. | Mantém fontes originais no diretório `docs/` (requisito acadêmico).
| 2. Conversão | `save_to_csv()` | Exporta para `data/raw/*.csv` em UTF-8. | CSV facilita versionamento e entrada no Pandas.
| 3. Enriquecimento | `analyze_data()` | Merge compras↔produtos↔clientes, cria agregados (`total_gasto`, `ticket_medio`, `n_compras`) e salva `clientes_agregado.csv`. | Garante features consistentes para ML e endpoints.
| 4. Resumo | `generate_summary_json()` | Persiste estatísticas (engajamento, finanças, segmentação). | Prova de auditoria rápida e base para relatórios.
| 5. Treinamento | `ChurnPredictor.prepare_features()` + `train()` | Label encoding de categóricas (cidade/clube), split estratificado 80/20, RandomForest (100 árvores) + DecisionTree + Logistic para comparação. | Combina interpretabilidade (Decision Tree) e performance (RF). | 
| 6. Seleção | `train_churn_model()` | Escolhe maior F1 e copia para `data/models/churn_model.pkl`. | Automatiza promoção de modelo sem intervenção manual.
| 7. Produção | `ChurnPredictor.load_model()` em `api/main.py` startup. | Mantém modelo na memória evitando IO a cada requisição. |

**Features usadas pelo modelo**: pontuação de engajamento, total gasto, número de compras, ticket médio, idade, indicador de assinatura no clube, cidade (codificada). A escolha cobre sinais de valor, frequência e perfil demográfico, balanceando explicabilidade e capacidade preditiva.

---

## 4. Backend (FastAPI + ML)
- `api/main.py`
  - Inicializa FastAPI (título, descrição e `/docs` habilitado) + `/redoc` customizado (CDN fixa).
  - Em `startup_event` carrega `clientes_agregado.csv`, `produtos.csv`, `compras.csv` e `churn_model.pkl`.
  - Endpoints-chave:
    - `/api/dashboard/stats`, `/api/dashboard/top-clientes`, `/api/dashboard/produtos/top`, `/api/dashboard/vendas/{tipo}` para visão executiva.
    - `/api/clientes`, `/api/clientes/{id}` e `/api/clientes/{id}/recomendacao` para gestão individual.
    - `/api/analytics/segmentacao` para alimentar gráficos de engajamento.
  - Conversões automáticas: campos "Sim/Não" → booleanos, preenchimento de NaN, tipagem via `ClienteResponse`, `RecomendacaoResponse`, `DashboardStats`.
- `knowledge_base/rules.py`
  - `AcaoRecomendada` e `NivelPrioridade` padronizam respostas.
  - `RuleEngine.avaliar_cliente()` centraliza o fluxo: classifica segmento, aplica regras na ordem, escolhe prioridade máxima e gera mensagem amigável.
- `models/churn_model.py`
  - Contém pipeline completo de treino, avaliação (accuracy, precision, recall, f1, confusion matrix) e persistência (Joblib).
  - `train_churn_model()` pode ser executado isoladamente para benchmarking.

Motivos técnicos:
- FastAPI garante baixa latência e validação automática; Uvicorn com `reload=True` facilita desenvolvimento.
- Escolha por DataFrames em memória reduz complexidade (sem banco relacional) e atende ao escopo acadêmico.

---

## 5. Frontend (React + Tailwind)
| Página/Componente | Arquivo | Função | Destaques |
| --- | --- | --- | --- |
| Shell + Rotas | `src/App.jsx` | Define layout, navbar, footer e rotas (`/`, `/clientes`, `/clientes/:id`). | Usa React Router 6 e ícones Lucide para linguagem visual consistente. |
| Dashboard Executivo | `pages/Dashboard.jsx` | KPIs, gráficos de barras/pizza, tabelas de top clientes/produtos, insights textuais. | Carrega dados em paralelo via `Promise.all`, utiliza Recharts com tema escuro. |
| Gestão de Clientes | `pages/Clientes.jsx` | Busca textual, badges de engajamento, status de clube/cancelamento, CTA para detalhes. | Paginação simplificada (`limit=100`) e filtros client-side para reduzir carga no backend. |
| Cliente Detalhes | `pages/ClienteDetalhes.jsx` | Cards financeiros, barra de risco, mensagens do motor de regras e lista de ações priorizadas. | Destaque visual por prioridade e explicação textual da regra/condição. |
| Cliente HTTP | `services/api.js` | Axios pré-configurado (`baseURL http://localhost:8000/api`). | Centraliza endpoints e garante timeouts/headers consistentes. |

Justificativa de design: Tailwind facilita criação de painéis em modo escuro (compatível com estética premium de vinhos) e Recharts oferece componentes responsivos usados em apresentações executivas.

---

## 6. Scripts e Automações
| Script | Local | O que faz | Quando usar | Motivo |
| --- | --- | --- | --- | --- |
| `backend/install.bat` | raiz/backend | Cria `venv`, ativa e instala dependências do `requirements.txt`. | Primeira configuração do backend. | Padroniza ambiente Python 3.10+ em Windows (cmd.exe). |
| `process_data.bat` | raiz | Ativa `backend\venv`, roda `load_data.py` e `models\churn_model.py`. | Sempre que houver novos dados Excel ou necessidade de re-treino. | Garante que CSVs processados e modelo estejam alinhados antes de subir API. |
| `start_backend.bat` | raiz | Entra em `backend`, ativa `venv` e executa `python run.py`. | Antes de interagir com o frontend/API. | Expõe URLs úteis (API, Swagger) e evita esquecer ativação do virtualenv. |
| `frontend/install.bat` | raiz/frontend | Executa `npm install`. | Preparação do frontend. | Simplifica onboarding em Windows. |
| `start_frontend.bat` | raiz | Valida `node_modules` e chama `npm run dev`. | Após backend estar online. | Garante que o servidor Vite rode sempre em `http://localhost:3000`. |
| `backend/run.py` | backend | Instância oficial do Uvicorn com banners e reload. | Usado pelo script de start (ou manualmente). | Mantém host `0.0.0.0`, útil para demos em LAN. |
| `backend/load_data.py` | backend | ETL completo + análises + summary JSON. | Parte do `process_data.bat` ou execuções ad-hoc. | Documenta métricas em console para anexar ao relatório. |
| `backend/models/churn_model.py` | backend | Treinamento/teste e salvamento do modelo ML. | Inclusão no pipeline ou experimentos isolados. | Fornece métricas para justificar escolha do RF em relatórios. |

---

## 7. Guia de Execução (cmd.exe – Windows)
1. **Pré-requisitos**: Python 3.10+, Node.js 18+, Git.
2. **Instalar backend**
   ```cmd
   cd c:\Users\KUMA\Documents\winebrain-sad\winebrain-sad
   backend\install.bat
   ```
3. **Processar dados + treinar modelo** (gera CSVs e `churn_model.pkl`)
   ```cmd
   process_data.bat
   ```
   > Anote métricas exibidas (accuracy, precision, recall, f1, feature importance) para o relatório.
4. **Instalar frontend**
   ```cmd
   frontend\install.bat
   ```
5. **Executar backend** (Terminal 1)
   ```cmd
   start_backend.bat
   ```
   - URLs automáticas: `http://localhost:8000`, `/docs`, `/redoc`.
6. **Executar frontend** (Terminal 2)
   ```cmd
   start_frontend.bat
   ```
   - Vite mostra `Local:  http://localhost:3000`.
7. **Verificações rápidas**
   ```cmd
   curl http://localhost:8000/api/health
   curl http://localhost:8000/api/dashboard/stats
   ```
   Abra `http://localhost:3000` e percorra Dashboard → Clientes → Detalhes.

> **Ordem crítica**: `process_data.bat` deve rodar após qualquer atualização das planilhas originais para não servir dados defasados ou modelo inconsistente.

---

## 8. API e Contratos Principais
| Método | Endpoint | Uso na UI | Response chave |
| --- | --- | --- | --- |
| GET | `/api/health` | Diagnóstico pós-deploy | `{ status, data_loaded, model_loaded }` |
| GET | `/api/dashboard/stats` | KPIs do Dashboard | `{ total_clientes, receita_total, ticket_medio, taxa_cancelamento, ... }` |
| GET | `/api/dashboard/top-clientes?limit=n` | Tabela "Top Clientes" | Lista com `cliente_id`, `nome`, `total_gasto`. |
| GET | `/api/dashboard/produtos/top?limit=n` | Tabela "Top Produtos" | `produto_id`, `nome`, `quantidade`, `valor`. |
| GET | `/api/dashboard/vendas/tipo-uva` | Gráfico de barras | Dicionário `{tipo_uva: valor}` ordenado. |
| GET | `/api/dashboard/vendas/pais` | Gráfico de pizza | `{pais: valor}`. |
| GET | `/api/analytics/segmentacao` | Gráfico "Segmentação" | Lista com `nivel_engajamento`, `quantidade`, `gasto_medio`, `compras_medias`. |
| GET | `/api/clientes?limit=&offset=` | Lista de clientes | Array `ClienteResponse`. |
| GET | `/api/clientes/{id}` | Cabeçalho em ClienteDetalhes | Objeto `ClienteResponse`. |
| GET | `/api/clientes/{id}/recomendacao` | Cartões de risco e ações | `RecomendacaoResponse` com `segmento`, `prioridade`, `acoes_recomendadas[]`. |

Todos os retornos são validados por modelos Pydantic, reduzindo inconsistências entre backend e frontend e servindo como contrato oficial.

---

## 9. Base de Conhecimento e Regras de Risco
| Regra | Condição (síntese) | Ações (`AcaoRecomendada`) | Prioridade padrão | Motivo de negócio |
| --- | --- | --- | --- | --- |
| **REGRA 1 – Cliente Premium** | `assinante_clube == True` ∧ `engajamento ≥ 8` | `recomendar_vinhos_premium`, `convidar_eventos_exclusivos`. | Alta | Manter clientes VIP reduz churn e gera upsell em rótulos premium. |
| **REGRA 2 – Risco de Cancelamento** | `cancelou == True` ∨ `engajamento < 4` | `enviar_cupom_reativacao` (20%), `enviar_pesquisa_satisfacao`. | Crítica | Ação imediata sobre clientes perdidos ou desmotivados evita perda definitiva de receita recorrente. |
| **REGRA 3 – Oportunidade de Upgrade** | `4 ≤ engajamento ≤ 7` ∧ `n_compras > 3` | `oferecer_upgrade_clube`. | Média | Clientes já habituados respondem bem a benefícios extras, elevando ticket médio. |
| **REGRA 4 – Conversão para Clube** | `assinante_clube == False` ∧ `total_gasto > valor_medio_geral` | `recomendar_adesao_clube`. | Alta | Converte compradores de alto valor em receita recorrente (LTV ↑). |
| **REGRA 5 – Alto Risco ML** | `probabilidade_churn ≥ 0.7` | `ativar_campanha_reengajamento`. | Crítica | Modelo detecta padrões de abandono iminente; requer contato personalizado.
| **REGRA 6 – Cliente Inativo** | `n_compras ≤ 2` ∧ `engajamento < 4` | `incluir_programa_fidelidade` (degustação/newsletter). | Média | Campanhas educativas ativam base dormente sem alto custo.
| **Fallback** | Nenhuma regra disparada | `nenhuma_acao` | Baixa | Mantém relacionamento padrão, evitando comunicações desnecessárias.

Cada resposta inclui `mensagem` interpretável (ex.: "⚠️ Cliente em risco!"), além de `metricas` para rastrear fatores que dispararam a recomendação. A prioridade máxima encontrada entre as regras aplicadas conduz o SLA da equipe (Critica → contato ≤24h, Alta → ≤72h, etc.).

---

## 10. Governança e Monitoramento Operacional
- **Health Check**: `/api/health` confirma carregamento dos DataFrames e do modelo.
- **Logs de inicialização**: `run.py` imprime URLs úteis e confirmações (dados/modelo) em cada boot.
- **Verificações manuais recomendadas**:
  1. Após `process_data.bat`, abrir `data/processed/summary.json` e verificar timestamp/estatísticas.
  2. Executar `python backend/models/churn_model.py` isoladamente quando testar novos hiperparâmetros.
  3. Rodar `curl http://localhost:8000/api/clientes/1/recomendacao` para validar saída antes de demonstrar.
- **Segurança**: CORS restrito a `http://localhost:3000` e `3001`, evitando consumo não autorizado durante aulas/demos.

---

## 11. Próximos Passos Sugeridos
1. **Automatizar coleta de métricas**: salvar resultados do treinamento em `data/models/metrics.json` para histórico.
2. **Adicionar testes unitários** para `RuleEngine` (garantir que cada regra dispare conforme esperado ao alterar limiares).
3. **Containerização**: gerar Dockerfile (base Python 3.11-slim + Node 18) para simplificar deploy em apresentações.
4. **Integração com banco relacional** caso o volume de dados cresça (usar SQLAlchemy já listado em `requirements.txt`).
5. **Simulador interativo** no frontend permitindo ajustar limiares de engajamento e observar impacto direto nos KPIs (modelo simulativo).

---

### Referências internas consultadas
- `backend/api/main.py`, `backend/knowledge_base/rules.py`, `backend/models/churn_model.py`, `backend/load_data.py`.
- Scripts `.bat` na raiz e em `backend/` e `frontend/`.
- `frontend/src/App.jsx`, `pages/Dashboard.jsx`, `Clientes.jsx`, `ClienteDetalhes.jsx`, `services/api.js`.
- Dados em `data/processed/summary.json` e dependências listadas em `backend/requirements.txt` e `frontend/package.json`.

> Este documento resume e justifica todas as decisões técnicas e operacionais do WineBrain, servindo como referência única para instalação, execução, auditoria e defesa acadêmica/profissional do projeto.
