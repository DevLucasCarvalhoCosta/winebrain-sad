import axios from 'axios';

// Usar variável de ambiente VITE_API_BASE_URL ou fallback para localhost
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Dashboard
export const getDashboardStats = () => api.get('/dashboard/stats');
export const getTopClientes = (limit = 5) => api.get(`/dashboard/top-clientes?limit=${limit}`);
export const getTopProdutos = (limit = 5) => api.get(`/dashboard/produtos/top?limit=${limit}`);
export const getVendasTipoUva = () => api.get('/dashboard/vendas/tipo-uva');
export const getVendasPais = () => api.get('/dashboard/vendas/pais');

// Clientes
export const getClientes = (limit = 10, offset = 0) => 
  api.get(`/clientes?limit=${limit}&offset=${offset}`);
export const getCliente = (clienteId) => api.get(`/clientes/${clienteId}`);
export const getRecomendacao = (clienteId) => api.get(`/clientes/${clienteId}/recomendacao`);

// Analytics
export const getSegmentacao = () => api.get('/analytics/segmentacao');

export default api;
