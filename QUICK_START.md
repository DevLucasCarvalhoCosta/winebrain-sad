# 🚀 Guia de Início Rápido - WineBrain

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.10+** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18+** - [Download Node.js](https://nodejs.org/)
- **Git** (opcional) - [Download Git](https://git-scm.com/)

---

## 🔧 Instalação Rápida (Windows)

### Passo 1: Instalar Backend

1. Abra o terminal na pasta do projeto
2. Execute o script de instalação:

```cmd
cd backend
install.bat
```

Isso irá:
- Criar ambiente virtual Python
- Instalar todas as dependências
- Configurar o ambiente

### Passo 2: Processar Dados e Treinar Modelo

Na raiz do projeto, execute:

```cmd
process_data.bat
```

Isso irá:
- Converter dados Excel para CSV
- Realizar análise exploratória
- Treinar modelo de Machine Learning
- Salvar modelo treinado

**⏱️ Tempo estimado:** 2-5 minutos

### Passo 3: Instalar Frontend

Em outro terminal:

```cmd
cd frontend
install.bat
```

Isso irá instalar todas as dependências React.

---

## ▶️ Executando o Sistema

### 1. Iniciar Backend (Terminal 1)

```cmd
start_backend.bat
```

O servidor estará disponível em:
- **API:** http://localhost:8000
- **Documentação:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### 2. Iniciar Frontend (Terminal 2)

```cmd
start_frontend.bat
```

A aplicação estará disponível em:
- **Web App:** http://localhost:3000

---

## 🎯 Primeira Utilização

### 1. Acessar Dashboard

Abra http://localhost:3000 no navegador e você verá:

- **KPIs principais**: Total de clientes, compras, receita, ticket médio
- **Gráficos**: Vendas por tipo de uva e país
- **Segmentação**: Clientes por nível de engajamento
- **Rankings**: Top 5 clientes e produtos

### 2. Explorar Clientes

Clique em "Clientes" na navbar:

- Lista completa de clientes
- Busca por nome ou cidade
- Filtros de status (clube, cancelados, em risco)
- Métricas de engajamento

### 3. Ver Detalhes e Recomendações

Clique em "Ver Detalhes" em qualquer cliente:

- **Perfil completo**: dados, métricas, status
- **Análise de Risco**: probabilidade de churn
- **Segmento**: classificação inteligente
- **Recomendações**: ações automáticas baseadas em regras de negócio

---

## 🧪 Testando a API

### Usando o Swagger UI

Acesse http://localhost:8000/docs

Exemplos de endpoints:

```
GET /api/dashboard/stats           - Estatísticas gerais
GET /api/clientes                  - Listar clientes
GET /api/clientes/1                - Dados do cliente 1
GET /api/clientes/1/recomendacao   - Recomendações para cliente 1
GET /api/dashboard/top-clientes    - Top 5 clientes
GET /api/dashboard/produtos/top    - Top 5 produtos
```

### Usando cURL

```cmd
# Obter estatísticas
curl http://localhost:8000/api/dashboard/stats

# Obter recomendação para cliente
curl http://localhost:8000/api/clientes/1/recomendacao
```

---

## 📊 Estrutura dos Dados

Após processar os dados, você encontrará:

```
data/
├── raw/                           # Dados brutos
│   ├── clientes.csv
│   ├── produtos.csv
│   └── compras.csv
├── processed/                     # Dados processados
│   ├── clientes_agregado.csv     # Clientes com métricas
│   ├── compras_completo.csv      # Compras com joins
│   └── summary.json              # Resumo estatístico
└── models/                        # Modelos treinados
    ├── churn_model.pkl           # Melhor modelo
    ├── churn_model_random_forest.pkl
    ├── churn_model_decision_tree.pkl
    └── churn_model_logistic.pkl
```

---

## 🤖 Modelos de Machine Learning

O sistema treina 3 modelos automaticamente:

1. **Random Forest** (padrão) - Melhor desempenho geral
2. **Decision Tree** - Mais interpretável
3. **Logistic Regression** - Baseline

Métricas exibidas:
- Acurácia
- Precisão
- Recall
- F1-Score
- Importância das features

---

## 🎓 Recursos para o Relatório

### Dados Disponíveis

- **100 clientes** com métricas completas
- **100 produtos** (vinhos)
- **100 compras** registradas
- **Análises estatísticas** em `summary.json`

### Modelos Implementados

✅ **Descritivo**: Dashboard com KPIs e gráficos
✅ **Preditivo**: Modelo de churn com ML
✅ **Prescritivo**: Motor de regras (6 regras de negócio)
✅ **Simulativo**: Análise de cenários (pode expandir)

### Base de Conhecimento

6 regras implementadas:
1. Cliente Premium (engajamento alto + clube)
2. Risco de Cancelamento (baixo engajamento)
3. Oportunidade de Upgrade (médio engajamento)
4. Conversão para Clube (alto gasto sem clube)
5. Alto Risco de Churn (predição ML)
6. Cliente Inativo (poucas compras)

---

## 🐛 Solução de Problemas

### Backend não inicia

```cmd
# Verificar instalação do Python
python --version

# Reinstalar dependências
cd backend
venv\Scripts\activate
pip install -r requirements.txt --force-reinstall
```

### Frontend não inicia

```cmd
# Limpar cache e reinstalar
cd frontend
rmdir /s /q node_modules
del package-lock.json
npm install
```

### Modelo não carrega

```cmd
# Treinar modelo novamente
cd backend
venv\Scripts\activate
python models\churn_model.py
```

### Porta já em uso

- **Backend (8000)**: Alterar em `backend/.env`
- **Frontend (3000)**: Alterar em `frontend/vite.config.js`

---

## 📸 Screenshots para o Relatório

Capture telas de:

1. **Dashboard** - KPIs e gráficos
2. **Lista de Clientes** - Tabela com filtros
3. **Detalhes do Cliente** - Perfil e métricas
4. **Recomendações** - Ações sugeridas
5. **API Docs** - Swagger UI
6. **Código do Modelo** - Treinamento ML
7. **Regras de Negócio** - Motor de regras

---

## 📝 Checklist do Projeto

### ✅ Implementado

- [x] Análise exploratória dos dados
- [x] Dashboard descritivo
- [x] Modelo preditivo de churn
- [x] Motor de regras prescritivas
- [x] API REST completa
- [x] Interface web profissional
- [x] Documentação técnica
- [x] Scripts de instalação

### 🎯 Para o Relatório

- [ ] Adicionar screenshots
- [ ] Documentar resultados dos modelos
- [ ] Exemplo de caso de uso
- [ ] Análise de impacto de negócio
- [ ] Conclusões e próximos passos

---

## 🆘 Suporte

Se encontrar problemas:

1. Verifique os logs do terminal
2. Confirme que todos os pré-requisitos estão instalados
3. Execute novamente o script de instalação
4. Verifique se as portas 3000 e 8000 estão livres

---

## 🎉 Pronto!

Seu Sistema de Apoio à Decisão WineBrain está configurado e rodando!

**Próximos passos:**
1. Explore o dashboard
2. Analise alguns clientes
3. Teste as recomendações
4. Capture screenshots para o relatório
5. Documente os resultados

**Boa sorte com o projeto! 🍷**
