# 🔧 Modificações no Docker Compose Principal

Este arquivo documenta as modificações que devem ser feitas no `docker-compose.yml` principal do servidor UEG.

---

## 📝 Arquivo: `~/docker-ueg-projects/docker-compose.yml`

### 1. Adicionar rede WineBrain na seção `networks:`

```yaml
networks:
  patrimonio_network:
  estresse_network:
  ana_network:
  n8n_network:
  proxy_network:
  winebrain_network:  # ← ADICIONAR
```

---

### 2. Modificar serviço `nginx` para incluir WineBrain

**Localizar:**
```yaml
  nginx:
    image: nginx:1.27-alpine
    container_name: nginx-gateway
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:ro
      - ./docker/nginx/includes:/etc/nginx/includes:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - /var/www/html:/var/www/html:ro
    networks:
      - proxy_network
      - patrimonio_network
      - estresse_network
      - ana_network
      - n8n_network
    depends_on:
      - patrimonio-backend
      - ana-backend
      - estresse-app
```

**Modificar para:**
```yaml
  nginx:
    image: nginx:1.27-alpine
    container_name: nginx-gateway
    restart: unless-stopped
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./docker/nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./docker/nginx/conf.d:/etc/nginx/conf.d:ro
      - ./docker/nginx/includes:/etc/nginx/includes:ro
      - /etc/letsencrypt:/etc/letsencrypt:ro
      - /var/www/html:/var/www/html:ro
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

---

### 3. Adicionar serviços WineBrain no final

```yaml
  # ============================================
  # WineBrain - Sistema de Apoio à Decisão
  # ============================================
  
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

---

## 📝 Arquivo: `~/docker-ueg-projects/docker/nginx/conf.d/upstreams.conf`

### Adicionar no final do arquivo:

```nginx
# ============================================
# WineBrain Upstreams
# ============================================

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

---

## 📝 Arquivo: `~/docker-ueg-projects/docker/nginx/conf.d/default.conf`

### Localizar seção HTTPS e adicionar include:

**Localizar:**
```nginx
    # ✅ Incluir rotas dos projetos
    include /etc/nginx/includes/app-estresse.conf;
    include /etc/nginx/includes/app-patrimonio.conf;
    include /etc/nginx/includes/app-ana.conf;
```

**Modificar para:**
```nginx
    # ✅ Incluir rotas dos projetos
    include /etc/nginx/includes/app-estresse.conf;
    include /etc/nginx/includes/app-patrimonio.conf;
    include /etc/nginx/includes/app-ana.conf;
    include /etc/nginx/includes/app-winebrain.conf;  # ← ADICIONAR
```

---

## ✅ Comandos para Aplicar Modificações

```bash
# 1. Fazer backup do compose atual
cd ~/docker-ueg-projects
cp docker-compose.yml docker-compose.yml.backup-$(date +%Y%m%d)

# 2. Editar arquivo
nano docker-compose.yml
# Fazer as modificações acima

# 3. Editar upstreams
nano docker/nginx/conf.d/upstreams.conf
# Adicionar upstreams do WineBrain

# 4. Editar default.conf
nano docker/nginx/conf.d/default.conf
# Adicionar include do app-winebrain.conf

# 5. Copiar configs do WineBrain
cp ~/winebrain-sad/docker/nginx/includes/app-winebrain.conf \
   ~/docker-ueg-projects/docker/nginx/includes/

# 6. Validar configuração
docker-compose config

# 7. Aplicar mudanças
docker-compose up -d

# 8. Verificar
docker ps | grep winebrain
docker logs winebrain-backend
docker logs winebrain-frontend
```

---

## 🔍 Verificação

Após aplicar as modificações, verificar:

```bash
# 1. Containers rodando
docker ps | grep winebrain

# 2. Redes criadas
docker network ls | grep winebrain

# 3. Health checks
curl http://localhost:8000/api/health
curl http://localhost/winebrain/api/health

# 4. Frontend
curl -I http://localhost/winebrain/

# 5. Logs
docker logs --tail=50 winebrain-backend
docker logs --tail=50 winebrain-frontend
docker logs --tail=50 nginx-gateway | grep winebrain
```

---

## 📋 Resumo das Mudanças

| Arquivo | Modificação | Linha |
|---------|-------------|-------|
| `docker-compose.yml` | Adicionar `winebrain_network` | Seção networks |
| `docker-compose.yml` | Adicionar rede no nginx | nginx.networks |
| `docker-compose.yml` | Adicionar depends_on | nginx.depends_on |
| `docker-compose.yml` | Adicionar serviços | No final |
| `upstreams.conf` | Adicionar upstreams | No final |
| `default.conf` | Adicionar include | Seção HTTPS |
| Copiar arquivo | `app-winebrain.conf` | includes/ |

---

## 🎯 Resultado Final

Após todas as modificações:

- ✅ WineBrain isolado em rede própria
- ✅ Comunicação via proxy_network com nginx
- ✅ Rotas configuradas em /winebrain/
- ✅ Health checks configurados
- ✅ Restart automático
- ✅ SSL/HTTPS via gateway

**URL:** https://patrimonioueg.duckdns.org/winebrain/

---

**Última atualização:** 20/11/2025
