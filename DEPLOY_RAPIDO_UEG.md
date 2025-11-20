# 🚀 WineBrain - Deploy Rápido no Servidor UEG

## 📋 Resumo Executivo

O WineBrain será hospedado no servidor UEG (200.137.241.42:8740) usando Docker, seguindo o mesmo padrão do PatrimônioUEG e outros projetos.

**URL Final:** `https://patrimonioueg.duckdns.org/winebrain/`

---

## ⚡ Deploy Rápido (5 minutos)

### 1️⃣ No seu PC - Preparar e Enviar

```cmd
:: Processar dados
cd c:\Users\KUMA\Documents\winebrain-sad\winebrain-sad
process_data.bat

:: Fazer commit
git add .
git commit -m "feat: configuração Docker para servidor UEG"
git push origin main

:: Enviar dados via SCP
scp -P 8740 data\processed\*.csv usuario@200.137.241.42:~/winebrain-sad/data/processed/
scp -P 8740 data\processed\*.json usuario@200.137.241.42:~/winebrain-sad/data/processed/
scp -P 8740 data\raw\*.csv usuario@200.137.241.42:~/winebrain-sad/data/raw/
scp -P 8740 data\models\*.pkl usuario@200.137.241.42:~/winebrain-sad/data/models/
```

### 2️⃣ No Servidor - Deploy Automático

```bash
ssh -p 8740 usuario@200.137.241.42

# Clonar projeto (primeira vez)
git clone https://github.com/DevLucasCarvalhoCosta/winebrain-sad.git
cd winebrain-sad

# Dar permissão e executar deploy
chmod +x deploy-ueg.sh
./deploy-ueg.sh
```

Pronto! 🎉

---

## 📁 Arquivos Criados

### Docker
- ✅ `backend/Dockerfile` - Container Python FastAPI
- ✅ `frontend/Dockerfile` - Build React + Nginx
- ✅ `frontend/nginx.conf` - Config Nginx para SPA
- ✅ `docker-compose.winebrain.yml` - Serviços isolados

### Nginx
- ✅ `docker/nginx/includes/app-winebrain.conf` - Rotas proxy
- ✅ `docker/nginx/conf.d/winebrain-upstreams.conf` - Upstreams

### Scripts
- ✅ `deploy-ueg.sh` - Deploy automático
- ✅ `check-ueg.sh` - Verificação de status

### Documentação
- ✅ `GUIA_DEPLOY_SERVIDOR_UEG.md` - Guia completo
- ✅ `DEPLOY_RAPIDO_UEG.md` - Este arquivo

---

## 🔧 Comandos Úteis

### Ver Status
```bash
./check-ueg.sh
```

### Ver Logs
```bash
docker logs -f winebrain-backend
docker logs -f winebrain-frontend
```

### Atualizar Aplicação
```bash
cd ~/winebrain-sad
git pull
cd ~/docker-ueg-projects
docker-compose restart winebrain-backend winebrain-frontend
```

### Rebuild Completo
```bash
cd ~/docker-ueg-projects
docker-compose build --no-cache winebrain-backend winebrain-frontend
docker-compose up -d winebrain-backend winebrain-frontend
```

### Parar/Iniciar
```bash
docker-compose stop winebrain-backend winebrain-frontend
docker-compose start winebrain-backend winebrain-frontend
```

---

## 🌐 URLs

| Recurso | URL |
|---------|-----|
| **Aplicação** | https://patrimonioueg.duckdns.org/winebrain/ |
| **API Docs** | https://patrimonioueg.duckdns.org/winebrain/api/docs |
| **Health Check** | https://patrimonioueg.duckdns.org/winebrain/api/health |
| **Dashboard** | https://patrimonioueg.duckdns.org/winebrain/api/dashboard/stats |
| **Clientes** | https://patrimonioueg.duckdns.org/winebrain/api/clientes |

---

## 📊 Arquitetura

```
Internet (HTTPS)
    ↓
Nginx Gateway (porta 80/443)
    ↓
[/winebrain/api/*] → winebrain-backend:8000 (Python FastAPI)
[/winebrain/*]     → winebrain-frontend:80 (React SPA)
    ↓
Redes Docker Isoladas
    - winebrain_network (interno)
    - proxy_network (gateway)
```

---

## ✅ Checklist de Deploy

- [ ] Processar dados localmente (`process_data.bat`)
- [ ] Fazer commit no GitHub
- [ ] Enviar dados via SCP para servidor
- [ ] SSH no servidor
- [ ] Clonar projeto (primeira vez)
- [ ] Executar `deploy-ueg.sh`
- [ ] Verificar com `check-ueg.sh`
- [ ] Testar no navegador

---

## 🆘 Problemas Comuns

### Container não inicia
```bash
docker logs winebrain-backend
# Verificar se dados existem em ~/winebrain-sad/data/
```

### API retorna 502
```bash
# Testar container diretamente
docker exec -it winebrain-backend curl http://localhost:8000/api/health

# Reiniciar nginx
docker-compose restart nginx
```

### Frontend não carrega
```bash
# Verificar build
docker logs winebrain-frontend

# Rebuild com variável correta
docker-compose build --build-arg VITE_API_BASE_URL=https://patrimonioueg.duckdns.org/winebrain/api winebrain-frontend
```

---

## 📖 Documentação Completa

Para instruções detalhadas, troubleshooting avançado e explicações técnicas, consulte:

👉 **[GUIA_DEPLOY_SERVIDOR_UEG.md](GUIA_DEPLOY_SERVIDOR_UEG.md)**

---

**Criado em:** 20/11/2025  
**Servidor:** 200.137.241.42:8740  
**Ambiente:** Docker + Nginx + Let's Encrypt
