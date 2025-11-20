#!/bin/bash
# ============================================
# WineBrain - Script de Deploy Automático
# Servidor UEG
# ============================================

set -e  # Exit on error

echo "============================================"
echo "🍷 WineBrain - Deploy Automático"
echo "============================================"
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Variáveis
PROJECT_DIR="$HOME/winebrain-sad"
COMPOSE_DIR="$HOME/docker-ueg-projects"
NGINX_INCLUDES="$COMPOSE_DIR/docker/nginx/includes"
NGINX_CONF="$COMPOSE_DIR/docker/nginx/conf.d"

# Função para log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar se está no servidor
if [ ! -d "$COMPOSE_DIR" ]; then
    log_error "Diretório docker-ueg-projects não encontrado!"
    log_error "Este script deve ser executado no servidor UEG."
    exit 1
fi

# 1. Atualizar código do GitHub
log_info "Atualizando código do GitHub..."
cd "$PROJECT_DIR"
git fetch origin
git pull origin main

# 2. Verificar dados
log_info "Verificando dados..."
if [ ! -f "$PROJECT_DIR/data/processed/clientes_agregado.csv" ]; then
    log_warn "Dados processados não encontrados!"
    log_warn "Execute: scp -P 8740 data/processed/* usuario@200.137.241.42:~/winebrain-sad/data/processed/"
fi

if [ ! -f "$PROJECT_DIR/data/models/churn_model.pkl" ]; then
    log_warn "Modelo ML não encontrado!"
    log_warn "Execute: scp -P 8740 data/models/* usuario@200.137.241.42:~/winebrain-sad/data/models/"
fi

# 3. Copiar configurações Nginx (se necessário)
log_info "Verificando configurações Nginx..."

if [ ! -f "$NGINX_INCLUDES/app-winebrain.conf" ]; then
    log_info "Copiando configuração Nginx..."
    cp "$PROJECT_DIR/docker/nginx/includes/app-winebrain.conf" "$NGINX_INCLUDES/"
fi

if [ ! -f "$NGINX_CONF/winebrain-upstreams.conf" ]; then
    log_info "Copiando upstreams Nginx..."
    cp "$PROJECT_DIR/docker/nginx/conf.d/winebrain-upstreams.conf" "$NGINX_CONF/"
fi

# 4. Build das imagens
log_info "Fazendo build das imagens Docker..."
cd "$COMPOSE_DIR"

docker-compose build \
    --build-arg VITE_API_BASE_URL=https://patrimonioueg.duckdns.org/winebrain/api \
    winebrain-backend winebrain-frontend

# 5. Parar containers antigos
log_info "Parando containers antigos..."
docker-compose stop winebrain-backend winebrain-frontend 2>/dev/null || true

# 6. Iniciar novos containers
log_info "Iniciando containers..."
docker-compose up -d winebrain-backend winebrain-frontend

# 7. Reiniciar nginx
log_info "Reiniciando Nginx Gateway..."
docker-compose restart nginx

# 8. Aguardar serviços ficarem prontos
log_info "Aguardando serviços iniciarem..."
sleep 10

# 9. Verificar status
log_info "Verificando status dos containers..."
docker ps | grep winebrain

# 10. Testar health checks
log_info "Testando health checks..."

echo ""
echo -n "Backend health check: "
if curl -s http://localhost:8000/api/health | grep -q "healthy"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FALHOU${NC}"
    log_error "Backend não está respondendo corretamente!"
fi

echo -n "Frontend health check: "
if curl -s http://localhost/winebrain/ | grep -q "WineBrain"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${YELLOW}WARN${NC} - Verifique manualmente"
fi

echo -n "API via Nginx: "
if curl -s http://localhost/winebrain/api/health | grep -q "healthy"; then
    echo -e "${GREEN}OK${NC}"
else
    echo -e "${RED}FALHOU${NC}"
    log_error "Nginx não está roteando corretamente!"
fi

# 11. Mostrar logs recentes
echo ""
log_info "Últimas linhas dos logs:"
echo ""
echo "=== Backend ==="
docker logs --tail=10 winebrain-backend
echo ""
echo "=== Frontend ==="
docker logs --tail=10 winebrain-frontend

# 12. Conclusão
echo ""
echo "============================================"
echo -e "${GREEN}✅ Deploy concluído!${NC}"
echo "============================================"
echo ""
echo "🌐 Acesse: https://patrimonioueg.duckdns.org/winebrain/"
echo "📚 API Docs: https://patrimonioueg.duckdns.org/winebrain/api/docs"
echo ""
echo "📊 Para ver logs:"
echo "  docker logs -f winebrain-backend"
echo "  docker logs -f winebrain-frontend"
echo ""
