# 🍷 WineBrain - Guia de Deploy no Servidor UEG

Este guia contém TODOS os passos para fazer deploy do WineBrain no servidor UEG (200.137.241.42:8740) usando Docker e Nginx, seguindo o padrão dos outros projetos.

---

## 📋 Pré-requisitos

- ✅ Acesso SSH ao servidor: `ssh -p 8740 usuario@200.137.241.42`
- ✅ Git configurado no servidor
- ✅ Docker e Docker Compose instalados
- ✅ Projeto funcionando localmente

---

## 🎯 PARTE 1: Preparar Projeto Localmente

### 1.1 Processar Dados

```cmd
cd c:\Users\KUMA\Documents\winebrain-sad\winebrain-sad
process_data.bat
```

Isso irá:
- Processar todos os dados
- Treinar o modelo de ML
- Copiar arquivos para `backend\app_data\`

### 1.2 Verificar Estrutura de Dados

Certifique-se que existem:
```
backend\app_data\
├── processed\
│   ├── clientes_agregado.csv
│   └── summary.json
├── raw\
│   ├── compras.csv
│   └── produtos.csv
└── models\
    └── churn_model.pkl
```

### 1.3 Fazer Commit no GitHub

```cmd
git add .
git commit -m "feat: adicionar configuração Docker para deploy no servidor UEG"
git push origin main
```

---

## 🚀 PARTE 2: Deploy no Servidor UEG

### 2.1 Conectar ao Servidor

```bash
ssh -p 8740 usuario@200.137.241.42
```

### 2.2 Clonar Projeto

```bash
cd ~/
git clone https://github.com/DevLucasCarvalhoCosta/winebrain-sad.git
cd winebrain-sad
```

Se já existir:
```bash
cd ~/winebrain-sad
git pull origin main
```

### 2.3 Copiar Dados Processados

```bash
# Criar estrutura de dados
mkdir -p data/processed data/raw data/models

# Se você tiver os dados no servidor, copie-os
# Caso contrário, precisará enviar via SCP do seu PC
```

**No seu PC Windows (CMD):**
```cmd
cd c:\Users\KUMA\Documents\winebrain-sad\winebrain-sad

:: Copiar dados processados
scp -P 8740 data\processed\clientes_agregado.csv usuario@200.137.241.42:~/winebrain-sad/data/processed/
scp -P 8740 data\processed\summary.json usuario@200.137.241.42:~/winebrain-sad/data/processed/

:: Copiar dados raw
scp -P 8740 data\raw\compras.csv usuario@200.137.241.42:~/winebrain-sad/data/raw/
scp -P 8740 data\raw\produtos.csv usuario@200.137.241.42:~/winebrain-sad/data/raw/

:: Copiar modelo treinado
scp -P 8740 data\models\churn_model.pkl usuario@200.137.241.42:~/winebrain-sad/data/models/
```

### 2.4 Integrar ao Docker Compose Principal

**No servidor, editar o docker-compose principal:**

```bash
cd ~/docker-ueg-projects
nano docker-compose.yml
```

**Adicionar na seção `networks:`:**
```yaml
  winebrain_network:
```

**Adicionar na seção `services:`:**
```yaml
  winebrain-backend:
    build:
      context: /home/usuario/winebrain-sad/backend
      dockerfile: Dockerfile
    container_name: winebrain-backend
    restart: unless-stopped
    environment:
      - PYTHONUNBUFFERED=1
      - API_ENV=production
    volumes:
      - /home/usuario/winebrain-sad/data/processed:/app/app_data/processed:ro
      - /home/usuario/winebrain-sad/data/raw:/app/app_data/raw:ro
      - /home/usuario/winebrain-sad/data/models:/app/app_data/models:ro
    networks:
      - winebrain_network
      - proxy_network
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:8000/api/health', timeout=5)"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  winebrain-frontend:
    build:
      context: /home/usuario/winebrain-sad/frontend
      dockerfile: Dockerfile
      args:
        VITE_API_BASE_URL: https://patrimonioueg.duckdns.org/winebrain/api
    container_name: winebrain-frontend
    restart: unless-stopped
    networks:
      - winebrain_network
      - proxy_network
    healthcheck:
      test: ["CMD", "wget", "--quiet", "--tries=1", "--spider", "http://localhost/health"]
      interval: 30s
      timeout: 3s
      retries: 3
      start_period: 5s
```

**Adicionar winebrain_network ao nginx:**
```yaml
  nginx:
    # ... configuração existente ...
    networks:
      - proxy_network
      - patrimonio_network
      - estresse_network
      - ana_network
      - n8n_network
      - winebrain_network  # ← ADICIONAR
    depends_on:
      - patrimonio-backend
      - ana-backend
      - estresse-app
      - winebrain-backend  # ← ADICIONAR
```

### 2.5 Configurar Nginx

**Copiar arquivos de configuração:**

```bash
# Copiar config do nginx
sudo cp ~/winebrain-sad/docker/nginx/includes/app-winebrain.conf \
        ~/docker-ueg-projects/docker/nginx/includes/

# Copiar upstreams
sudo cp ~/winebrain-sad/docker/nginx/conf.d/winebrain-upstreams.conf \
        ~/docker-ueg-projects/docker/nginx/conf.d/
```

**Adicionar include no default.conf:**

```bash
nano ~/docker-ueg-projects/docker/nginx/conf.d/default.conf
```

Na seção HTTPS, adicionar:
```nginx
    # ✅ Incluir rotas dos projetos
    include /etc/nginx/includes/app-estresse.conf;
    include /etc/nginx/includes/app-patrimonio.conf;
    include /etc/nginx/includes/app-ana.conf;
    include /etc/nginx/includes/app-winebrain.conf;  # ← ADICIONAR
```

**Adicionar upstreams no upstreams.conf:**

```bash
nano ~/docker-ueg-projects/docker/nginx/conf.d/upstreams.conf
```

Adicionar no final:
```nginx
# WineBrain Backend
upstream winebrain_backend {
    least_conn;
    server winebrain-backend:8000 max_fails=3 fail_timeout=30s;
    keepalive 32;
}

# WineBrain Frontend
upstream winebrain_app {
    server winebrain-frontend:80;
}
```

### 2.6 Build e Deploy

```bash
cd ~/docker-ueg-projects

# Build das imagens WineBrain
docker-compose build winebrain-backend winebrain-frontend

# Iniciar serviços
docker-compose up -d winebrain-backend winebrain-frontend

# Reiniciar nginx para aplicar novas rotas
docker-compose restart nginx
```

### 2.7 Verificar Deploy

```bash
# Ver logs do backend
docker logs -f winebrain-backend

# Ver logs do frontend
docker logs -f winebrain-frontend

# Verificar status dos containers
docker ps | grep winebrain

# Testar health check do backend
curl http://localhost:8000/api/health

# Testar via nginx
curl http://localhost/winebrain/api/health
```

---

## ✅ PARTE 3: Validação

### 3.1 Testar Endpoints

**No servidor:**
```bash
# Health check
curl http://localhost/winebrain/api/health

# Dashboard stats
curl http://localhost/winebrain/api/dashboard/stats

# Listar clientes
curl http://localhost/winebrain/api/clientes
```

### 3.2 Acessar Aplicação

**No navegador:**
```
https://patrimonioueg.duckdns.org/winebrain/
```

Você deve ver:
- ✅ Dashboard com KPIs
- ✅ Gráficos carregando
- ✅ Lista de clientes funcionando
- ✅ Recomendações de IA disponíveis

### 3.3 Verificar Logs

```bash
# Backend
docker logs --tail=100 winebrain-backend

# Frontend
docker logs --tail=100 winebrain-frontend

# Nginx
docker logs --tail=100 nginx-gateway
```

---

## 🔄 PARTE 4: Atualizações Futuras

### 4.1 Atualizar Código

**No seu PC:**
```cmd
git add .
git commit -m "feat: nova funcionalidade"
git push origin main
```

**No servidor:**
```bash
cd ~/winebrain-sad
git pull origin main

cd ~/docker-ueg-projects
docker-compose build winebrain-backend winebrain-frontend
docker-compose up -d winebrain-backend winebrain-frontend
```

### 4.2 Atualizar Dados e Modelo

**No seu PC:**
```cmd
process_data.bat

:: Enviar novos dados via SCP
scp -P 8740 data\processed\* usuario@200.137.241.42:~/winebrain-sad/data/processed/
scp -P 8740 data\raw\* usuario@200.137.241.42:~/winebrain-sad/data/raw/
scp -P 8740 data\models\* usuario@200.137.241.42:~/winebrain-sad/data/models/
```

**No servidor:**
```bash
cd ~/docker-ueg-projects
docker-compose restart winebrain-backend
```

### 4.3 Ver Logs em Tempo Real

```bash
# Backend
docker logs -f winebrain-backend

# Frontend
docker logs -f winebrain-frontend

# Todos os containers
docker-compose logs -f winebrain-backend winebrain-frontend
```

---

## 🐛 TROUBLESHOOTING

### Erro: "Container não inicia"

```bash
# Ver logs detalhados
docker logs winebrain-backend

# Verificar se os dados existem
ls -la ~/winebrain-sad/data/processed/
ls -la ~/winebrain-sad/data/models/

# Rebuild forçado
docker-compose build --no-cache winebrain-backend
docker-compose up -d winebrain-backend
```

### Erro: "API não responde"

```bash
# Testar dentro do container
docker exec -it winebrain-backend bash
curl http://localhost:8000/api/health
exit

# Verificar redes
docker network inspect docker-ueg-projects_winebrain_network
docker network inspect docker-ueg-projects_proxy_network
```

### Erro: "Frontend carrega mas não conecta na API"

```bash
# Verificar variável de ambiente do build
docker inspect winebrain-frontend | grep VITE_API_BASE_URL

# Rebuild com variável correta
cd ~/docker-ueg-projects
docker-compose build --build-arg VITE_API_BASE_URL=https://patrimonioueg.duckdns.org/winebrain/api winebrain-frontend
docker-compose up -d winebrain-frontend
```

### Erro: "502 Bad Gateway"

```bash
# Verificar se backend está rodando
docker ps | grep winebrain-backend

# Verificar logs do nginx
docker logs nginx-gateway | grep winebrain

# Testar upstream diretamente
docker exec -it nginx-gateway sh
wget -O- http://winebrain-backend:8000/api/health
exit
```

### Erro: "Permissão negada nos volumes"

```bash
# Verificar permissões
ls -la ~/winebrain-sad/data/

# Corrigir permissões se necessário
chmod -R 755 ~/winebrain-sad/data/
```

---

## 📊 Comandos Úteis

```bash
# Status de todos os containers
docker ps

# Uso de recursos
docker stats

# Reiniciar apenas WineBrain
docker-compose restart winebrain-backend winebrain-frontend

# Parar WineBrain
docker-compose stop winebrain-backend winebrain-frontend

# Remover e recriar
docker-compose down winebrain-backend winebrain-frontend
docker-compose up -d winebrain-backend winebrain-frontend

# Ver configuração do docker-compose
docker-compose config

# Limpar volumes e cache do Docker (cuidado!)
docker system prune -a --volumes
```

---

## 🎉 Conclusão

O WineBrain está agora rodando no servidor UEG em:

**URL Pública:** `https://patrimonioueg.duckdns.org/winebrain/`

**Endpoints API:**
- Health: `https://patrimonioueg.duckdns.org/winebrain/api/health`
- Dashboard: `https://patrimonioueg.duckdns.org/winebrain/api/dashboard/stats`
- Clientes: `https://patrimonioueg.duckdns.org/winebrain/api/clientes`
- Docs: `https://patrimonioueg.duckdns.org/winebrain/api/docs`

**Arquitetura:**
- ✅ Backend FastAPI em Python 3.11
- ✅ Frontend React + Vite com Nginx
- ✅ Isolado em rede Docker própria
- ✅ Proxy reverso via Nginx Gateway
- ✅ SSL/HTTPS automático via Let's Encrypt
- ✅ Health checks configurados
- ✅ Restart automático em caso de falha

---

**Última atualização:** 20/11/2025
