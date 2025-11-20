#!/bin/bash
# ============================================
# WineBrain - Script de Verificação
# Testa se tudo está funcionando no servidor
# ============================================

echo "============================================"
echo "🔍 WineBrain - Verificação de Status"
echo "============================================"
echo ""

# Cores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 1. Containers rodando
echo "📦 Containers:"
if docker ps | grep -q winebrain-backend; then
    echo -e "  Backend: ${GREEN}✓ Rodando${NC}"
else
    echo -e "  Backend: ${RED}✗ Parado${NC}"
fi

if docker ps | grep -q winebrain-frontend; then
    echo -e "  Frontend: ${GREEN}✓ Rodando${NC}"
else
    echo -e "  Frontend: ${RED}✗ Parado${NC}"
fi

echo ""

# 2. Health Checks
echo "🏥 Health Checks:"

# Backend direto
BACKEND_HEALTH=$(curl -s http://localhost:8000/api/health 2>/dev/null)
if echo "$BACKEND_HEALTH" | grep -q "healthy"; then
    echo -e "  Backend (direto): ${GREEN}✓ Healthy${NC}"
else
    echo -e "  Backend (direto): ${RED}✗ Falhou${NC}"
fi

# API via Nginx
API_HEALTH=$(curl -s http://localhost/winebrain/api/health 2>/dev/null)
if echo "$API_HEALTH" | grep -q "healthy"; then
    echo -e "  API (nginx): ${GREEN}✓ Healthy${NC}"
else
    echo -e "  API (nginx): ${RED}✗ Falhou${NC}"
fi

echo ""

# 3. Dados carregados
echo "📊 Dados:"
if echo "$BACKEND_HEALTH" | grep -q '"data_loaded":true'; then
    echo -e "  Dados: ${GREEN}✓ Carregados${NC}"
else
    echo -e "  Dados: ${RED}✗ Não carregados${NC}"
fi

if echo "$BACKEND_HEALTH" | grep -q '"model_loaded":true'; then
    echo -e "  Modelo ML: ${GREEN}✓ Carregado${NC}"
else
    echo -e "  Modelo ML: ${RED}✗ Não carregado${NC}"
fi

echo ""

# 4. Endpoints
echo "🔗 Endpoints:"

# Dashboard Stats
if curl -s http://localhost/winebrain/api/dashboard/stats | grep -q "total_clientes"; then
    echo -e "  /dashboard/stats: ${GREEN}✓ OK${NC}"
else
    echo -e "  /dashboard/stats: ${RED}✗ Falhou${NC}"
fi

# Clientes
if curl -s http://localhost/winebrain/api/clientes | grep -q "id_cliente"; then
    echo -e "  /clientes: ${GREEN}✓ OK${NC}"
else
    echo -e "  /clientes: ${RED}✗ Falhou${NC}"
fi

echo ""

# 5. Logs recentes
echo "📝 Logs Recentes (últimas 5 linhas):"
echo ""
echo "=== Backend ==="
docker logs --tail=5 winebrain-backend 2>/dev/null || echo "Container não encontrado"
echo ""
echo "=== Frontend ==="
docker logs --tail=5 winebrain-frontend 2>/dev/null || echo "Container não encontrado"

echo ""

# 6. Uso de recursos
echo "💻 Uso de Recursos:"
docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" | grep winebrain

echo ""
echo "============================================"
echo "✅ Verificação concluída"
echo "============================================"
echo ""
echo "🌐 URL: https://patrimonioueg.duckdns.org/winebrain/"
echo ""
