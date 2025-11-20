#!/bin/bash
# ============================================
# WineBrain - Script de Deploy Remoto
# Para uso via GitHub Actions ou SSH
# ============================================

set -e  # Exit on error

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo ""
echo -e "${BLUE}============================================${NC}"
echo -e "${BLUE}🍷 WineBrain - Deploy Remoto${NC}"
echo -e "${BLUE}============================================${NC}"
echo ""

# Variáveis (podem ser sobrescritas via env vars)
PROJECT_NAME="${PROJECT_NAME:-winebrain-sad}"
COMPOSE_DIR="${COMPOSE_DIR:-$HOME/docker-ueg-projects}"
PROJECT_DIR="${PROJECT_DIR:-$HOME/$PROJECT_NAME}"
GITHUB_REPO="${GITHUB_REPO:-DevLucasCarvalhoCosta/winebrain-sad}"
DEPLOY_MODE="${DEPLOY_MODE:-auto}"  # auto, manual, ci

# Funções de log
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    exit 1
}

log_step() {
    echo ""
    echo -e "${BLUE}▶ $1${NC}"
    echo -e "${BLUE}──────────────────────────────────────────${NC}"
}

# Verificar se está no servidor
check_environment() {
    log_step "Verificando ambiente..."
    
    if [ ! -d "$COMPOSE_DIR" ]; then
        log_error "Diretório $COMPOSE_DIR não encontrado!"
    fi
    
    if ! command -v docker &> /dev/null; then
        log_error "Docker não está instalado!"
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        log_error "Docker Compose não está instalado!"
    fi
    
    log_info "✅ Ambiente OK"
}

# Atualizar código do GitHub
update_code() {
    log_step "Atualizando código do GitHub..."
    
    if [ ! -d "$PROJECT_DIR" ]; then
        log_info "Primeira vez - clonando repositório..."
        cd ~
        git clone "https://github.com/$GITHUB_REPO.git" "$PROJECT_NAME" || log_error "Falha ao clonar repositório!"
        cd "$PROJECT_DIR"
    else
        log_info "Atualizando código existente..."
        cd "$PROJECT_DIR"
        
        # Salvar mudanças locais se houver
        if [ -n "$(git status --porcelain)" ]; then
            log_warn "Há mudanças locais. Fazendo stash..."
            git stash
        fi
        
        git fetch origin
        git reset --hard origin/main
        git pull origin main || log_error "Falha ao atualizar código!"
    fi
    
    CURRENT_COMMIT=$(git rev-parse --short HEAD)
    log_info "✅ Código atualizado para commit: $CURRENT_COMMIT"
}

# Verificar dados
check_data() {
    log_step "Verificando dados..."
    
    local missing_data=0
    
    if [ ! -f "$PROJECT_DIR/data/processed/clientes_agregado.csv" ]; then
        log_warn "⚠️  Arquivo não encontrado: data/processed/clientes_agregado.csv"
        missing_data=1
    else
        log_info "✅ Dados processados OK"
    fi
    
    if [ ! -f "$PROJECT_DIR/data/models/churn_model.pkl" ]; then
        log_warn "⚠️  Arquivo não encontrado: data/models/churn_model.pkl"
        missing_data=1
    else
        log_info "✅ Modelo ML OK"
    fi
    
    if [ $missing_data -eq 1 ]; then
        log_warn ""
        log_warn "Alguns arquivos de dados estão faltando!"
        log_warn "Para enviar do seu PC, use:"
        log_warn "  scp -P 8740 data/processed/* usuario@200.137.241.42:~/winebrain-sad/data/processed/"
        log_warn "  scp -P 8740 data/models/* usuario@200.137.241.42:~/winebrain-sad/data/models/"
        log_warn ""
        log_warn "Os containers vão iniciar, mas a aplicação pode não funcionar corretamente."
        
        # Não falhar, apenas avisar
        sleep 3
    fi
}

# Copiar configurações Nginx
setup_nginx() {
    log_step "Configurando Nginx..."
    
    local nginx_includes="$COMPOSE_DIR/docker/nginx/includes"
    local nginx_conf="$COMPOSE_DIR/docker/nginx/conf.d"
    
    # Criar diretórios se não existirem
    mkdir -p "$nginx_includes" "$nginx_conf"
    
    # Copiar configuração do app
    if [ -f "$PROJECT_DIR/docker/nginx/includes/app-winebrain.conf" ]; then
        cp "$PROJECT_DIR/docker/nginx/includes/app-winebrain.conf" "$nginx_includes/" || log_warn "Falha ao copiar app-winebrain.conf"
        log_info "✅ app-winebrain.conf copiado"
    else
        log_warn "⚠️  app-winebrain.conf não encontrado"
    fi
    
    # Copiar upstreams
    if [ -f "$PROJECT_DIR/docker/nginx/conf.d/winebrain-upstreams.conf" ]; then
        cp "$PROJECT_DIR/docker/nginx/conf.d/winebrain-upstreams.conf" "$nginx_conf/" || log_warn "Falha ao copiar winebrain-upstreams.conf"
        log_info "✅ winebrain-upstreams.conf copiado"
    else
        log_warn "⚠️  winebrain-upstreams.conf não encontrado"
    fi
}

# Build das imagens Docker
build_images() {
    log_step "Building Docker images..."
    
    cd "$COMPOSE_DIR"
    
    log_info "Building winebrain-backend..."
    docker-compose build \
        --no-cache \
        winebrain-backend || log_error "Build do backend falhou!"
    
    log_info "Building winebrain-frontend..."
    docker-compose build \
        --build-arg VITE_API_BASE_URL=https://patrimonioueg.duckdns.org/winebrain/api \
        --no-cache \
        winebrain-frontend || log_error "Build do frontend falhou!"
    
    log_info "✅ Build concluído"
}

# Parar containers antigos
stop_containers() {
    log_step "Parando containers antigos..."
    
    cd "$COMPOSE_DIR"
    
    if docker ps | grep -q winebrain; then
        docker-compose stop winebrain-backend winebrain-frontend 2>/dev/null || true
        log_info "✅ Containers parados"
    else
        log_info "ℹ️  Nenhum container rodando"
    fi
}

# Iniciar containers
start_containers() {
    log_step "Iniciando containers..."
    
    cd "$COMPOSE_DIR"
    
    docker-compose up -d winebrain-backend winebrain-frontend || log_error "Falha ao iniciar containers!"
    
    log_info "✅ Containers iniciados"
}

# Reiniciar Nginx
restart_nginx() {
    log_step "Reiniciando Nginx Gateway..."
    
    cd "$COMPOSE_DIR"
    
    docker-compose restart nginx || log_warn "Falha ao reiniciar Nginx"
    
    log_info "✅ Nginx reiniciado"
}

# Aguardar serviços iniciarem
wait_for_services() {
    log_step "Aguardando serviços iniciarem..."
    
    local max_wait=60
    local waited=0
    local interval=5
    
    while [ $waited -lt $max_wait ]; do
        if docker ps | grep -q winebrain-backend && docker ps | grep -q winebrain-frontend; then
            log_info "✅ Containers rodando"
            sleep 10  # Aguardar mais um pouco para app iniciar
            return 0
        fi
        
        sleep $interval
        waited=$((waited + interval))
        echo -n "."
    done
    
    echo ""
    log_error "Timeout aguardando containers iniciarem!"
}

# Verificar status dos containers
check_containers() {
    log_step "Verificando status dos containers..."
    
    echo ""
    docker ps | grep winebrain || log_warn "Nenhum container winebrain rodando!"
    echo ""
    
    # Verificar se estão rodando
    if docker ps | grep -q winebrain-backend; then
        log_info "✅ Backend: RODANDO"
    else
        log_error "❌ Backend: NÃO ESTÁ RODANDO"
    fi
    
    if docker ps | grep -q winebrain-frontend; then
        log_info "✅ Frontend: RODANDO"
    else
        log_error "❌ Frontend: NÃO ESTÁ RODANDO"
    fi
}

# Testar health checks
test_health() {
    log_step "Testando health checks..."
    
    local retries=5
    local wait=3
    
    # Testar backend direto
    echo -n "Backend (direto): "
    for i in $(seq 1 $retries); do
        if curl -sf http://localhost:8000/api/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ OK${NC}"
            break
        fi
        
        if [ $i -eq $retries ]; then
            echo -e "${RED}❌ FALHOU${NC}"
            log_warn "Backend não está respondendo no localhost:8000"
        else
            sleep $wait
        fi
    done
    
    # Testar API via Nginx
    echo -n "API (via Nginx): "
    for i in $(seq 1 $retries); do
        if curl -sf http://localhost/winebrain/api/health > /dev/null 2>&1; then
            echo -e "${GREEN}✅ OK${NC}"
            break
        fi
        
        if [ $i -eq $retries ]; then
            echo -e "${RED}❌ FALHOU${NC}"
            log_warn "Nginx não está roteando corretamente"
        else
            sleep $wait
        fi
    done
    
    # Testar frontend via Nginx
    echo -n "Frontend (via Nginx): "
    if curl -sf http://localhost/winebrain/ > /dev/null 2>&1; then
        echo -e "${GREEN}✅ OK${NC}"
    else
        echo -e "${YELLOW}⚠️  WARN${NC} (verifique manualmente)"
    fi
}

# Mostrar logs
show_logs() {
    log_step "Logs recentes..."
    
    echo ""
    echo -e "${BLUE}=== Backend (últimas 10 linhas) ===${NC}"
    docker logs --tail=10 winebrain-backend 2>&1 || log_warn "Não foi possível obter logs do backend"
    
    echo ""
    echo -e "${BLUE}=== Frontend (últimas 10 linhas) ===${NC}"
    docker logs --tail=10 winebrain-frontend 2>&1 || log_warn "Não foi possível obter logs do frontend"
    echo ""
}

# Resumo final
show_summary() {
    log_step "Deploy concluído!"
    
    echo ""
    echo -e "${GREEN}✅ Deploy realizado com sucesso!${NC}"
    echo ""
    echo -e "${BLUE}📊 Informações:${NC}"
    echo "  Commit: $CURRENT_COMMIT"
    echo "  Data: $(date '+%Y-%m-%d %H:%M:%S')"
    echo ""
    echo -e "${BLUE}🌐 URLs:${NC}"
    echo "  Aplicação:    https://patrimonioueg.duckdns.org/winebrain/"
    echo "  API Docs:     https://patrimonioueg.duckdns.org/winebrain/api/docs"
    echo "  Health Check: https://patrimonioueg.duckdns.org/winebrain/api/health"
    echo ""
    echo -e "${BLUE}📊 Comandos úteis:${NC}"
    echo "  Ver logs:     docker logs -f winebrain-backend"
    echo "  Status:       docker ps | grep winebrain"
    echo "  Restart:      cd ~/docker-ueg-projects && docker-compose restart winebrain-backend winebrain-frontend"
    echo ""
}

# Função principal
main() {
    local start_time=$(date +%s)
    
    # Executar passos
    check_environment
    update_code
    check_data
    setup_nginx
    build_images
    stop_containers
    start_containers
    restart_nginx
    wait_for_services
    check_containers
    test_health
    show_logs
    
    local end_time=$(date +%s)
    local duration=$((end_time - start_time))
    
    echo ""
    echo -e "${BLUE}============================================${NC}"
    show_summary
    echo -e "${BLUE}============================================${NC}"
    echo ""
    echo "⏱️  Tempo total: ${duration}s"
    echo ""
}

# Executar
main "$@"
