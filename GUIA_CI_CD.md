# 🚀 WineBrain - Guia de CI/CD com GitHub Actions

## 📋 Visão Geral

Este guia explica como configurar o **deploy automático** do WineBrain para o servidor UEG usando **GitHub Actions**.

Sempre que houver um `push` na branch `main`, o sistema automaticamente:
1. ✅ Testa o código (backend e frontend)
2. 🔨 Faz build das aplicações
3. 🚢 Faz deploy no servidor UEG
4. 🧪 Valida que tudo está funcionando

---

## 🎯 Requisitos

### No Servidor UEG
- ✅ SSH configurado (porta 8740)
- ✅ Docker e Docker Compose instalados
- ✅ Projeto já deve ter sido configurado manualmente ao menos uma vez
- ✅ Configurações do Nginx já devem estar no lugar

### No GitHub
- ✅ Repositório: `DevLucasCarvalhoCosta/winebrain-sad`
- ✅ Secrets configurados (ver seção abaixo)
- ✅ GitHub Actions habilitado

---

## 🔐 Passo 1: Configurar Secrets no GitHub

### 1.1 Acessar Configurações do Repositório

1. Acesse: https://github.com/DevLucasCarvalhoCosta/winebrain-sad
2. Clique em **Settings** (Configurações)
3. No menu lateral, clique em **Secrets and variables** → **Actions**
4. Clique em **New repository secret**

### 1.2 Adicionar os Secrets

Adicione os seguintes secrets:

#### `SSH_HOST`
- **Nome:** `SSH_HOST`
- **Valor:** `200.137.241.42`
- **Descrição:** IP do servidor UEG

#### `SSH_PORT`
- **Nome:** `SSH_PORT`
- **Valor:** `8740`
- **Descrição:** Porta SSH do servidor

#### `SSH_USER`
- **Nome:** `SSH_USER`
- **Valor:** `usuario` (substituir pelo usuário real)
- **Descrição:** Nome de usuário SSH

#### `SSH_PRIVATE_KEY`
- **Nome:** `SSH_PRIVATE_KEY`
- **Valor:** Sua chave privada SSH
- **Descrição:** Chave privada para autenticação SSH

**Como obter a chave SSH:**

**No seu PC Windows (PowerShell ou Git Bash):**
```bash
# Se você já tem uma chave SSH
cat ~/.ssh/id_rsa

# OU gerar uma nova chave (se não tiver)
ssh-keygen -t rsa -b 4096 -C "github-actions@winebrain"
cat ~/.ssh/id_rsa
```

**Copie TODO o conteúdo** (incluindo `-----BEGIN RSA PRIVATE KEY-----` e `-----END RSA PRIVATE KEY-----`)

### 1.3 Configurar Chave Pública no Servidor

A chave pública correspondente deve estar no servidor:

```bash
# Conectar ao servidor
ssh -p 8740 usuario@200.137.241.42

# Adicionar chave pública
nano ~/.ssh/authorized_keys
# Cole a chave pública (conteúdo de ~/.ssh/id_rsa.pub)

# Ajustar permissões
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

---

## 📝 Passo 2: Verificar Configuração

### 2.1 Estrutura de Arquivos

O workflow está em:
```
.github/
└── workflows/
    └── deploy.yml
```

### 2.2 Testar Conexão SSH

**No seu PC, teste a conexão:**
```bash
ssh -p 8740 -i ~/.ssh/id_rsa usuario@200.137.241.42 "echo 'Conexão OK'"
```

Se aparecer "Conexão OK", está tudo certo!

---

## 🚀 Passo 3: Fazer Deploy

### Opção A: Deploy Automático (Push na Main)

Sempre que você fizer push na branch `main`, o deploy acontece automaticamente:

```bash
git add .
git commit -m "feat: nova funcionalidade"
git push origin main
```

O GitHub Actions irá:
1. Executar testes
2. Fazer build
3. Fazer deploy no servidor
4. Validar funcionamento

### Opção B: Deploy Manual (Workflow Dispatch)

Você pode disparar o deploy manualmente pelo GitHub:

1. Acesse: https://github.com/DevLucasCarvalhoCosta/winebrain-sad/actions
2. Clique em **Deploy WineBrain to UEG Server**
3. Clique em **Run workflow**
4. Selecione a branch `main`
5. Clique em **Run workflow**

---

## 📊 Passo 4: Monitorar Deploy

### 4.1 Acompanhar Execução

1. Acesse: https://github.com/DevLucasCarvalhoCosta/winebrain-sad/actions
2. Clique na execução mais recente
3. Acompanhe cada job:
   - 🔨 **Build and Test** - Testa e compila o código
   - 🚢 **Deploy to UEG Server** - Faz deploy no servidor
   - 📢 **Notify** - Notifica resultado

### 4.2 Ver Logs Detalhados

Clique em cada step para ver logs detalhados:
- Logs de build
- Logs de deploy
- Logs dos containers no servidor
- Testes de health check

### 4.3 Verificar no Servidor

**SSH no servidor:**
```bash
ssh -p 8740 usuario@200.137.241.42

# Ver status dos containers
docker ps | grep winebrain

# Ver logs
docker logs -f winebrain-backend
docker logs -f winebrain-frontend

# Testar health check
curl http://localhost/winebrain/api/health
```

---

## 🎯 Fluxo Completo do CI/CD

```
┌─────────────────────────────────────────────────────────────┐
│  1. DESENVOLVEDOR                                            │
│     git push origin main                                     │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  2. GITHUB ACTIONS                                           │
│     ├─ Job: Build and Test                                  │
│     │   ├─ Setup Python 3.11                                │
│     │   ├─ Install backend dependencies                     │
│     │   ├─ Test backend imports                             │
│     │   ├─ Setup Node.js 18                                 │
│     │   ├─ Install frontend dependencies                    │
│     │   └─ Build frontend (npm run build)                   │
│     │                                                         │
│     ├─ Job: Deploy to UEG Server                            │
│     │   ├─ Setup SSH connection                             │
│     │   ├─ Connect to server via SSH                        │
│     │   ├─ Pull latest code from GitHub                     │
│     │   ├─ Build Docker images                              │
│     │   ├─ Stop old containers                              │
│     │   ├─ Start new containers                             │
│     │   ├─ Restart Nginx                                    │
│     │   └─ Test health checks                               │
│     │                                                         │
│     └─ Job: Notify                                           │
│         └─ Report deployment status                          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  3. SERVIDOR UEG (200.137.241.42:8740)                      │
│     ├─ Git pull from GitHub                                 │
│     ├─ Docker build images                                  │
│     ├─ Docker compose up -d                                 │
│     └─ Application running                                  │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│  4. APLICAÇÃO DISPONÍVEL                                     │
│     🌐 https://patrimonioueg.duckdns.org/winebrain/         │
│     📚 https://patrimonioueg.duckdns.org/winebrain/api/docs │
└─────────────────────────────────────────────────────────────┘
```

---

## ⚙️ Configurações Avançadas

### Ambientes (Environments)

O workflow usa um ambiente chamado `production` que pode ter:
- Proteções (aprovação manual)
- Secrets específicos
- URL de produção

**Para configurar:**
1. Settings → Environments → New environment
2. Nome: `production`
3. Configurar regras de proteção (opcional)

### Trigger Conditions

O workflow é disparado quando:

```yaml
on:
  push:
    branches:
      - main           # Push na branch main
    paths-ignore:
      - '**.md'        # Ignora arquivos .md
      - 'docs/**'      # Ignora pasta docs
  workflow_dispatch:   # Permite disparo manual
```

### Build Arguments

O frontend é buildado com a variável:
```yaml
VITE_API_BASE_URL: https://patrimonioueg.duckdns.org/winebrain/api
```

Se precisar mudar, edite em `.github/workflows/deploy.yml`.

---

## 🐛 Troubleshooting

### ❌ Erro: "Permission denied (publickey)"

**Causa:** Chave SSH não está configurada corretamente

**Solução:**
1. Verificar se `SSH_PRIVATE_KEY` está no GitHub Secrets
2. Verificar se chave pública está no servidor em `~/.ssh/authorized_keys`
3. Testar conexão manualmente: `ssh -p 8740 -i ~/.ssh/id_rsa usuario@200.137.241.42`

### ❌ Erro: "docker: command not found"

**Causa:** Docker não está instalado no servidor ou usuário não tem permissão

**Solução:**
```bash
# No servidor
sudo usermod -aG docker $USER
# Logout e login novamente
```

### ❌ Erro: "Build failed"

**Causa:** Dependências faltando ou erro no código

**Solução:**
1. Ver logs detalhados no GitHub Actions
2. Testar build localmente:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt
   python -c "from api.main import app"
   
   # Frontend
   cd frontend
   npm ci
   npm run build
   ```

### ❌ Erro: "Health check failed"

**Causa:** Containers iniciaram mas aplicação não responde

**Solução:**
```bash
# SSH no servidor
ssh -p 8740 usuario@200.137.241.42

# Ver logs
docker logs winebrain-backend
docker logs winebrain-frontend

# Verificar dados
ls -la ~/winebrain-sad/data/processed/
ls -la ~/winebrain-sad/data/models/

# Restart manual
cd ~/docker-ueg-projects
docker-compose restart winebrain-backend winebrain-frontend
```

### ❌ Deploy em Loop (sempre faz deploy)

**Causa:** Arquivos sendo modificados a cada deploy

**Solução:**
Adicionar ao `.gitignore`:
```
data/
*.pyc
__pycache__/
node_modules/
dist/
.env
```

---

## 📈 Monitoramento

### GitHub Actions Badge

Adicionar ao `README.md`:

```markdown
![Deploy Status](https://github.com/DevLucasCarvalhoCosta/winebrain-sad/actions/workflows/deploy.yml/badge.svg)
```

### Logs de Deploy

**Ver últimos deploys:**
https://github.com/DevLucasCarvalhoCosta/winebrain-sad/actions

**Ver logs do servidor:**
```bash
ssh -p 8740 usuario@200.137.241.42
docker logs -f winebrain-backend
```

### Métricas

**No GitHub Actions, você pode ver:**
- ⏱️ Tempo de build
- ⏱️ Tempo de deploy
- ✅ Taxa de sucesso
- 📊 Histórico de deploys

---

## 🔄 Workflow Detalhado

### Job 1: Build and Test (~3-5 minutos)

```yaml
1. Checkout code              # Baixa código do GitHub
2. Setup Python 3.11          # Instala Python
3. Install dependencies       # pip install -r requirements.txt
4. Test backend               # Valida imports
5. Setup Node.js 18           # Instala Node
6. Install frontend deps      # npm ci
7. Build frontend             # npm run build
8. Verify build               # Verifica se dist/ existe
```

### Job 2: Deploy to UEG Server (~2-4 minutos)

```yaml
1. Checkout code              # Baixa código
2. Setup SSH key              # Configura autenticação SSH
3. Deploy to server           # Conecta via SSH e executa:
   ├─ Git pull               # Atualiza código no servidor
   ├─ Build Docker images    # docker-compose build
   ├─ Stop old containers    # docker-compose stop
   ├─ Start new containers   # docker-compose up -d
   ├─ Restart Nginx          # docker-compose restart nginx
   └─ Test health checks     # curl health endpoints
4. Test deployment            # Valida que está funcionando
5. Deployment summary         # Gera resumo
```

### Job 3: Notify (~10 segundos)

```yaml
1. Check deploy status        # Verifica se passou
2. Show result                # Exibe resultado final
```

---

## 🎓 Boas Práticas

### 1. Commits Semânticos

Use prefixos para commits:
```bash
feat: nova funcionalidade
fix: correção de bug
docs: atualização de documentação
refactor: refatoração de código
test: adição de testes
chore: tarefas de manutenção
```

### 2. Testar Localmente Antes

Sempre teste antes de fazer push:
```bash
# Backend
cd backend
python -c "from api.main import app; print('OK')"

# Frontend
cd frontend
npm run build
```

### 3. Deploy em Horários Apropriados

- ✅ Evite deploy em horários de pico
- ✅ Faça backup antes de mudanças grandes
- ✅ Tenha um plano de rollback

### 4. Monitorar Após Deploy

Após cada deploy:
```bash
# Verificar containers
docker ps | grep winebrain

# Ver logs por 2 minutos
timeout 120 docker logs -f winebrain-backend

# Testar endpoints principais
curl https://patrimonioueg.duckdns.org/winebrain/api/health
curl https://patrimonioueg.duckdns.org/winebrain/api/dashboard/stats
```

### 5. Versionamento

Considere usar tags para releases:
```bash
git tag -a v1.0.0 -m "Release 1.0.0"
git push origin v1.0.0
```

---

## 📚 Recursos Adicionais

### Documentação Oficial

- **GitHub Actions:** https://docs.github.com/actions
- **Docker Compose:** https://docs.docker.com/compose/
- **FastAPI:** https://fastapi.tiangolo.com/
- **React + Vite:** https://vitejs.dev/

### Arquivos Relacionados

- `.github/workflows/deploy.yml` - Workflow principal
- `backend/Dockerfile` - Build do backend
- `frontend/Dockerfile` - Build do frontend
- `docker-compose.winebrain.yml` - Configuração Docker
- `deploy-ueg.sh` - Script de deploy manual
- `GUIA_DEPLOY_SERVIDOR_UEG.md` - Guia completo de deploy

### Comandos Úteis

```bash
# Ver status do workflow
gh workflow view deploy.yml

# Listar execuções
gh run list --workflow=deploy.yml

# Ver logs de uma execução
gh run view <run-id> --log

# Disparar workflow manualmente
gh workflow run deploy.yml
```

---

## ✅ Checklist de Configuração

- [ ] Secrets configurados no GitHub
  - [ ] `SSH_HOST`
  - [ ] `SSH_PORT`
  - [ ] `SSH_USER`
  - [ ] `SSH_PRIVATE_KEY`
- [ ] Chave pública no servidor (`~/.ssh/authorized_keys`)
- [ ] Testar conexão SSH manualmente
- [ ] Projeto já configurado no servidor (primeira vez manual)
- [ ] Docker e Docker Compose instalados no servidor
- [ ] Configurações Nginx no lugar
- [ ] GitHub Actions habilitado no repositório
- [ ] Fazer primeiro push para testar

---

## 🎉 Conclusão

Com o CI/CD configurado, você tem:

✅ **Deploy Automático** - Push na main = deploy automático
✅ **Testes Automatizados** - Valida antes de fazer deploy
✅ **Histórico Completo** - Todos os deploys registrados
✅ **Rollback Fácil** - Reverter para commit anterior
✅ **Monitoramento** - Logs e status em tempo real
✅ **Confiabilidade** - Processo padronizado e repetível

**Fluxo de Trabalho:**
1. Desenvolver localmente
2. Testar localmente
3. Commit e push
4. GitHub Actions faz o resto!
5. Aplicação atualizada em produção

---

**Criado em:** 20/11/2025  
**Servidor:** 200.137.241.42:8740  
**Aplicação:** https://patrimonioueg.duckdns.org/winebrain/
