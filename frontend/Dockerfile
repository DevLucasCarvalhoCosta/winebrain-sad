# ============================================
# WineBrain Frontend - React + Vite
# Build em multi-stage para otimização
# ============================================

# Stage 1: Build da aplicação
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar package.json e package-lock.json
COPY package*.json ./

# Instalar dependências (incluindo devDependencies para o build)
RUN npm ci --silent

# Copiar código fonte
COPY . .

# Variável de ambiente para API (será sobrescrita no runtime)
ARG VITE_API_BASE_URL=http://localhost:8000/api
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Build da aplicação
RUN npm run build

# Stage 2: Servir com Nginx
FROM nginx:1.27-alpine

# Copiar build do stage anterior
COPY --from=builder /app/dist /usr/share/nginx/html

# Copiar configuração customizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

# Comando padrão do Nginx
CMD ["nginx", "-g", "daemon off;"]
