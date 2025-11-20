# 🚀 Guia Completo de Deploy na Vercel - WineBrain

Este guia detalha TODOS os passos necessários para subir o projeto do ambiente local para produção na Vercel.

---

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter:

- ✅ Conta no GitHub (gratuita)
- ✅ Conta na Vercel (gratuita - fazer login com GitHub)
- ✅ Git instalado na máquina
- ✅ Projeto funcionando localmente

---

## 🎯 PARTE 1: Preparar o Projeto Local

### Passo 1.1: Criar estrutura de dados para produção

```cmd
cd c:\Users\KUMA\Documents\winebrain-sad\winebrain-sad

# Criar diretório para dados de produção
mkdir backend\app_data
mkdir backend\app_data\processed
mkdir backend\app_data\raw
mkdir backend\app_data\models
```

### Passo 1.2: Processar dados e copiar arquivos necessários

```cmd
# Processar dados localmente
process_data.bat

# Copiar arquivos gerados para app_data
copy data\processed\clientes_agregado.csv backend\app_data\processed\
copy data\processed\summary.json backend\app_data\processed\
copy data\raw\compras.csv backend\app_data\raw\
copy data\raw\produtos.csv backend\app_data\raw\
copy data\models\churn_model.pkl backend\app_data\models\
```

### Passo 1.3: Criar arquivo de configuração Vercel para o backend

Crie o arquivo `backend\vercel.json` com este conteúdo:

```json
{
  "version": 2,
  "builds": [
    {
      "src": "api/main.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "api/main.py"
    }
  ]
}
```

### Passo 1.4: Atualizar caminhos no backend

Edite `backend\api\main.py` e localize estas linhas (próximo ao início):

```python
# Caminhos
BASE_DIR = Path(__file__).parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODEL_DIR = DATA_DIR / "models"
```

**Substitua por:**

```python
# Caminhos - ajustado para produção
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "app_data"
MODEL_DIR = DATA_DIR / "models"
```

Também localize a seção de CORS (próximo ao topo do arquivo):

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Substitua por:**

```python
import os

# CORS - permitir frontend da Vercel
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://localhost:3001",
        FRONTEND_URL,
        "https://*.vercel.app"  # Permite qualquer subdomínio vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Passo 1.5: Atualizar frontend para usar variável de ambiente

Edite `frontend\src\services\api.js`:

Localize:
```javascript
const API_BASE_URL = 'http://localhost:8000/api';
```

**Substitua por:**
```javascript
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';
```

### Passo 1.6: Criar arquivo .env.example no frontend

Crie `frontend\.env.example`:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

---

## 🐙 PARTE 2: Subir para o GitHub

### Passo 2.1: Inicializar repositório Git (se ainda não tiver)

```cmd
cd c:\Users\KUMA\Documents\winebrain-sad\winebrain-sad

# Inicializar Git (pular se já existir)
git init

# Criar .gitignore
echo node_modules/ > .gitignore
echo venv/ >> .gitignore
echo __pycache__/ >> .gitignore
echo *.pyc >> .gitignore
echo .env >> .gitignore
echo .DS_Store >> .gitignore
echo dist/ >> .gitignore
```

### Passo 2.2: Fazer commit das alterações

```cmd
git add .
git commit -m "Preparar projeto para deploy na Vercel"
```

### Passo 2.3: Criar repositório no GitHub

1. Abra https://github.com/new
2. Nome do repositório: `winebrain-sad`
3. Deixe como **Public** ou **Private** (sua escolha)
4. **NÃO marque** "Initialize with README"
5. Clique em **"Create repository"**

### Passo 2.4: Conectar e fazer push

```cmd
# Substitua SEU_USUARIO pelo seu usuário do GitHub
git remote add origin https://github.com/SEU_USUARIO/winebrain-sad.git
git branch -M main
git push -u origin main
```

---

## ☁️ PARTE 3: Deploy do Backend na Vercel

### Passo 3.1: Acessar Vercel

1. Vá para https://vercel.com
2. Clique em **"Sign Up"** ou **"Log In"**
3. Escolha **"Continue with GitHub"**
4. Autorize a Vercel a acessar seus repositórios

### Passo 3.2: Criar projeto do Backend

1. No dashboard da Vercel, clique em **"Add New..."** → **"Project"**
2. Localize o repositório `winebrain-sad` e clique em **"Import"**
3. Configure o projeto:

   **Nome do projeto:** `winebrain-backend`
   
   **Framework Preset:** Other
   
   **Root Directory:** Clique em **"Edit"** e selecione `backend`
   
   **Build Command:** (deixe vazio)
   
   **Output Directory:** (deixe vazio)
   
   **Install Command:** `pip install -r requirements.txt`

4. Clique em **"Environment Variables"** e adicione:

   | Name | Value |
   |------|-------|
   | `PYTHON_VERSION` | `3.11` |
   | `FRONTEND_URL` | `https://winebrain-frontend.vercel.app` |

5. Clique em **"Deploy"**

### Passo 3.3: Aguardar build e anotar URL

- Aguarde o processo de build (pode levar 2-5 minutos)
- Quando aparecer "Congratulations!", anote a URL do backend
- Exemplo: `https://winebrain-backend-xyz123.vercel.app`

### Passo 3.4: Testar o backend

Abra o navegador e acesse:
- `https://SEU-BACKEND.vercel.app/api/health`

Você deve ver:
```json
{
  "status": "healthy",
  "data_loaded": true,
  "model_loaded": true
}
```

Se der erro, vá para a seção de **Troubleshooting** no final deste guia.

---

## 🎨 PARTE 4: Deploy do Frontend na Vercel

### Passo 4.1: Criar novo projeto

1. No dashboard da Vercel, clique em **"Add New..."** → **"Project"** novamente
2. Localize o mesmo repositório `winebrain-sad` e clique em **"Import"**
3. Configure o projeto:

   **Nome do projeto:** `winebrain-frontend`
   
   **Framework Preset:** Vite
   
   **Root Directory:** Clique em **"Edit"** e selecione `frontend`
   
   **Build Command:** `npm run build`
   
   **Output Directory:** `dist`
   
   **Install Command:** `npm install`

4. Clique em **"Environment Variables"** e adicione:

   | Name | Value |
   |------|-------|
   | `VITE_API_BASE_URL` | `https://SEU-BACKEND.vercel.app/api` |
   | `NODE_VERSION` | `18` |

   ⚠️ **IMPORTANTE:** Substitua `SEU-BACKEND.vercel.app` pela URL real do seu backend (anotada no Passo 3.3)

5. Clique em **"Deploy"**

### Passo 4.2: Aguardar build

- Aguarde o processo de build (1-3 minutos)
- Quando aparecer "Congratulations!", clique em **"Visit"** para ver sua aplicação

### Passo 4.3: Atualizar URL do frontend no backend

Agora que você tem a URL do frontend, volte para o projeto do backend:

1. Na Vercel, vá para **"winebrain-backend"** → **"Settings"** → **"Environment Variables"**
2. Edite a variável `FRONTEND_URL`
3. Cole a URL completa do frontend (ex: `https://winebrain-frontend-xyz456.vercel.app`)
4. Clique em **"Save"**
5. Vá para **"Deployments"** → clique nos 3 pontinhos do último deploy → **"Redeploy"**

---

## ✅ PARTE 5: Validação Final

### Passo 5.1: Testar Dashboard

1. Acesse `https://SEU-FRONTEND.vercel.app`
2. Verifique se os KPIs aparecem
3. Confira se os gráficos carregam
4. Olhe no console do navegador (F12) para erros

### Passo 5.2: Testar gestão de clientes

1. Clique em **"Clientes"** no menu
2. Verifique se a lista carrega
3. Clique em **"Ver Detalhes"** de um cliente
4. Confirme que as recomendações aparecem

### Passo 5.3: Testar API diretamente

Abra o navegador e teste:

```
https://SEU-BACKEND.vercel.app/api/dashboard/stats
https://SEU-BACKEND.vercel.app/api/clientes
https://SEU-BACKEND.vercel.app/api/clientes/1/recomendacao
```

---

## 🔄 PARTE 6: Atualizações Futuras

Sempre que quiser atualizar o projeto:

### 6.1: Atualizar dados

```cmd
# Local
cd c:\Users\KUMA\Documents\winebrain-sad\winebrain-sad
process_data.bat

# Copiar novos arquivos
copy data\processed\clientes_agregado.csv backend\app_data\processed\
copy data\processed\summary.json backend\app_data\processed\
copy data\raw\compras.csv backend\app_data\raw\
copy data\raw\produtos.csv backend\app_data\raw\
copy data\models\churn_model.pkl backend\app_data\models\

# Fazer commit
git add .
git commit -m "Atualizar dados e modelo"
git push
```

A Vercel detecta automaticamente e faz o redeploy!

### 6.2: Atualizar código

```cmd
# Fazer alterações nos arquivos
# Depois:
git add .
git commit -m "Descrição das alterações"
git push
```

---

## 🐛 TROUBLESHOOTING

### Erro: "Module not found"

**Solução:**
- Vá para **Settings** → **Environment Variables**
- Adicione `PYTHON_VERSION = 3.11`
- Faça **Redeploy**

### Erro de CORS no console

**Sintoma:** `Access to XMLHttpRequest has been blocked by CORS policy`

**Solução:**
1. Verifique se a variável `FRONTEND_URL` no backend está correta
2. Certifique-se de ter atualizado o código CORS em `api/main.py`
3. Faça redeploy do backend

### Frontend não carrega dados

**Solução:**
1. Abra o console (F12) e veja o erro
2. Verifique se `VITE_API_BASE_URL` está correta nas env vars
3. Teste a API diretamente no navegador
4. Se API funciona mas frontend não, faça redeploy do frontend

### Erro: "data_loaded: false"

**Solução:**
- Os arquivos CSV não foram copiados para `backend/app_data/`
- Copie novamente e faça commit/push

### Erro: "model_loaded: false"

**Solução:**
- O arquivo `.pkl` não foi copiado para `backend/app_data/models/`
- Execute `process_data.bat` novamente
- Copie o modelo e faça commit/push

### Build falha com erro de memória

**Solução:**
- Remova dependências desnecessárias do `requirements.txt` (matplotlib, seaborn)
- O modelo `.pkl` pode estar muito grande (limite ~50MB)

---

## 📞 Suporte

Se encontrar problemas:

1. **Logs da Vercel:** Cada projeto tem aba "Logs" com detalhes
2. **Console do navegador:** Pressione F12 para ver erros JavaScript
3. **Documentação Vercel:** https://vercel.com/docs

---

## 🎉 Conclusão

Parabéns! Seu projeto WineBrain está online e acessível globalmente.

**URLs finais:**
- Frontend: `https://winebrain-frontend.vercel.app`
- Backend API: `https://winebrain-backend.vercel.app/api`
- Swagger Docs: `https://winebrain-backend.vercel.app/docs`

Compartilhe os links com seu time ou professores!

---

**Última atualização:** 19/11/2025
