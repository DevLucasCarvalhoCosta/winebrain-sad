import React, { useState, useEffect } from 'react';
import { 
  Users, ShoppingCart, Wine, TrendingUp, AlertTriangle, 
  DollarSign, Activity 
} from 'lucide-react';
import { 
  BarChart, Bar, LineChart, Line, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer 
} from 'recharts';
import { 
  getDashboardStats, getTopClientes, getTopProdutos, getRankingProdutosDetalhado,
  getVendasTipoUva, getVendasPais, getSegmentacao, getVendasTemporal 
} from '../services/api';

// Paleta expandida para suportar todos os países
const COLORS = [
  '#ef4444', // Vermelho
  '#f59e0b', // Laranja
  '#10b981', // Verde
  '#3b82f6', // Azul
  '#8b5cf6', // Roxo
  '#ec4899', // Rosa
  '#06b6d4', // Ciano
  '#f43f5e', // Vermelho Rose
  '#84cc16', // Lima
  '#6366f1', // Índigo
  '#14b8a6', // Teal
  '#f97316'  // Laranja escuro
];

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [topClientes, setTopClientes] = useState([]);
  const [topProdutos, setTopProdutos] = useState([]);
  const [vendasUva, setVendasUva] = useState([]);
  const [vendasPais, setVendasPais] = useState([]);
  const [vendasTemporal, setVendasTemporal] = useState([]);
  const [segmentacao, setSegmentacao] = useState([]);
  const [rankingProdutos, setRankingProdutos] = useState([]);
  const [loading, setLoading] = useState(true);
  
  // Filtros para análise temporal
  const [filtrosPeriodo, setFiltrosPeriodo] = useState({
    periodo: 'mensal',
    metrica: 'valor'
  });
  
  // Filtros para ranking de produtos
  const [filtrosProdutos, setFiltrosProdutos] = useState({
    ordenar_por: 'valor',
    limit: 10
  });

  useEffect(() => {
    loadDashboardData();
  }, []);

  useEffect(() => {
    loadVendasTemporais();
  }, [filtrosPeriodo]);

  useEffect(() => {
    loadRankingProdutos();
  }, [filtrosProdutos]);

  const loadVendasTemporais = async () => {
    try {
      const response = await getVendasTemporal(filtrosPeriodo);
      setVendasTemporal(response.data);
    } catch (error) {
      console.error('Erro ao carregar vendas temporais:', error);
    }
  };

  const loadRankingProdutos = async () => {
    try {
      const response = await getRankingProdutosDetalhado(filtrosProdutos);
      setRankingProdutos(response.data);
    } catch (error) {
      console.error('Erro ao carregar ranking de produtos:', error);
    }
  };

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      const [
        statsRes, 
        clientesRes, 
        produtosRes, 
        uvaRes, 
        paisRes,
        temporalRes,
        segmentacaoRes
      ] = await Promise.all([
        getDashboardStats(),
        getTopClientes(5),
        getTopProdutos(5),
        getVendasTipoUva(),
        getVendasPais(),
        getVendasTemporal(),
        getSegmentacao()
      ]);

      setStats(statsRes.data);
      setTopClientes(clientesRes.data);
      setVendasTemporal(temporalRes.data);
      setTopProdutos(produtosRes.data);
      
      // Transformar dados para gráficos
      setVendasUva(
        Object.entries(uvaRes.data)
          .map(([name, value]) => ({ name, value }))
          .slice(0, 5)
      );
      
      // Exibir TODOS os países com vendas (não limitar a 5)
      setVendasPais(
        Object.entries(paisRes.data)
          .map(([name, value]) => ({ name, value }))
          .sort((a, b) => b.value - a.value) // Ordenar do maior para o menor
      );

      setSegmentacao(segmentacaoRes.data);
      
    } catch (error) {
      console.error('Erro ao carregar dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-white text-xl">Carregando dashboard...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Dashboard Executivo</h1>
        <p className="text-slate-400">Visão geral do negócio e indicadores principais</p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <Users className="h-8 w-8 text-blue-500" />
            <span className="text-green-500 text-sm font-medium">
              {((1 - stats.taxa_cancelamento) * 100).toFixed(1)}% ativos
            </span>
          </div>
          <h3 className="text-2xl font-bold text-white">{stats.total_clientes}</h3>
          <p className="text-slate-400 text-sm">Total de Clientes</p>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <ShoppingCart className="h-8 w-8 text-purple-500" />
          </div>
          <h3 className="text-2xl font-bold text-white">{stats.total_compras}</h3>
          <p className="text-slate-400 text-sm">Total de Compras</p>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <DollarSign className="h-8 w-8 text-green-500" />
          </div>
          <h3 className="text-2xl font-bold text-white">
            R$ {stats.receita_total.toFixed(2)}
          </h3>
          <p className="text-slate-400 text-sm">Receita Total</p>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <TrendingUp className="h-8 w-8 text-wine-500" />
          </div>
          <h3 className="text-2xl font-bold text-white">
            R$ {stats.ticket_medio.toFixed(2)}
          </h3>
          <p className="text-slate-400 text-sm">Ticket Médio</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
        {/* Vendas por Tipo de Uva */}
        <div className="bg-slate-800 rounded-lg p-3 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center px-3 pt-3">
            <Wine className="h-5 w-5 mr-2 text-red-500" />
            Vendas por Tipo de Uva
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart 
              data={vendasUva} 
              layout="vertical"
              margin={{ top: 5, right: 50, left: 40, bottom: 5 }}
            >
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis type="number" stroke="#9ca3af" />
              <YAxis 
                type="category" 
                dataKey="name" 
                stroke="#9ca3af"
              />
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                labelStyle={{ color: '#fff' }}
                formatter={(value) => [`R$ ${value.toFixed(2)}`, 'Vendas']}
              />
              <Bar 
                dataKey="value" 
                fill="#dc2626"
                radius={[0, 8, 8, 0]}
                barSize={25}
                label={{ 
                  position: 'right',
                  fill: '#fff',
                  fontSize: 12,
                  fontWeight: 600,
                  formatter: (value) => `R$ ${value.toFixed(0)}`
                }}
              />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Vendas por País */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">
            Vendas por País
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={vendasPais}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                outerRadius={100}
                fill="#8884d8"
                dataKey="value"
              >
                {vendasPais.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Gráfico de Vendas Temporais */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
          <h3 className="text-lg font-semibold text-white flex items-center mb-4 md:mb-0">
            <TrendingUp className="h-5 w-5 mr-2 text-green-500" />
            Análise Temporal de Vendas
          </h3>
          
          {/* Filtros */}
          <div className="flex gap-3 flex-wrap">
            <div className="flex items-center gap-2">
              <label className="text-sm text-slate-400">Período:</label>
              <select 
                value={filtrosPeriodo.periodo}
                onChange={(e) => setFiltrosPeriodo({...filtrosPeriodo, periodo: e.target.value})}
                className="bg-slate-700 text-white text-sm rounded px-3 py-1.5 border border-slate-600 focus:outline-none focus:border-green-500"
              >
                <option value="diario">Diário</option>
                <option value="semanal">Semanal</option>
                <option value="mensal">Mensal</option>
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <label className="text-sm text-slate-400">Métrica:</label>
              <select 
                value={filtrosPeriodo.metrica}
                onChange={(e) => setFiltrosPeriodo({...filtrosPeriodo, metrica: e.target.value})}
                className="bg-slate-700 text-white text-sm rounded px-3 py-1.5 border border-slate-600 focus:outline-none focus:border-green-500"
              >
                <option value="valor">Valor (R$)</option>
                <option value="quantidade">Quantidade</option>
                <option value="ticket_medio">Ticket Médio</option>
              </select>
            </div>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <div style={{ 
            minWidth: filtrosPeriodo.periodo === 'diario' ? `${Math.max(vendasTemporal.length * 80, 2000)}px` : '100%' 
          }}>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={vendasTemporal}>
                <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                <XAxis 
                  dataKey="periodo" 
                  stroke="#9ca3af"
                  angle={-45}
                  textAnchor="end"
                  height={80}
                  interval={0}
                  tick={{ fontSize: 9 }}
                />
                <YAxis stroke="#9ca3af" />
                <Tooltip 
                  contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
                  labelStyle={{ color: '#fff' }}
                  formatter={(value) => {
                    const metricaAtual = filtrosPeriodo.metrica;
                    if (metricaAtual === 'valor' || metricaAtual === 'ticket_medio') {
                      return [`R$ ${value.toFixed(2)}`, metricaAtual === 'valor' ? 'Vendas' : 'Ticket Médio'];
                    } else if (metricaAtual === 'quantidade') {
                      return [`${value} itens`, 'Quantidade'];
                    } else {
                      return [`${value} compras`, 'Nº de Compras'];
                    }
                  }}
                />
                <Line 
                  type="monotone" 
                  dataKey={filtrosPeriodo.metrica}
                  stroke="#10b981" 
                  strokeWidth={3}
                  dot={{ fill: '#10b981', r: 5 }}
                  activeDot={{ r: 7 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>

      {/* Segmentação de Clientes */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-8">
        <h3 className="text-lg font-semibold text-white mb-4">
          Segmentação de Clientes por Engajamento
        </h3>
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={segmentacao}>
            <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
            <XAxis dataKey="nivel_engajamento" stroke="#9ca3af" />
            <YAxis yAxisId="left" orientation="left" stroke="#9ca3af" />
            <YAxis yAxisId="right" orientation="right" stroke="#9ca3af" />
            <Tooltip 
              contentStyle={{ backgroundColor: '#1e293b', border: '1px solid #334155' }}
              labelStyle={{ color: '#fff' }}
            />
            <Legend />
            <Bar yAxisId="left" dataKey="quantidade" fill="#3b82f6" name="Quantidade" />
            <Bar yAxisId="right" dataKey="gasto_medio" fill="#10b981" name="Gasto Médio" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Ranking Detalhado de Produtos */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between mb-6">
          <h3 className="text-lg font-semibold text-white flex items-center mb-4 md:mb-0">
            <Wine className="h-5 w-5 mr-2 text-red-500" />
            Ranking Detalhado de Produtos
          </h3>
          
          {/* Filtros */}
          <div className="flex gap-3 flex-wrap">
            <div className="flex items-center gap-2">
              <label className="text-sm text-slate-400">Ordenar por:</label>
              <select 
                value={filtrosProdutos.ordenar_por}
                onChange={(e) => setFiltrosProdutos({...filtrosProdutos, ordenar_por: e.target.value})}
                className="bg-slate-700 text-white text-sm rounded px-3 py-1.5 border border-slate-600 focus:outline-none focus:border-red-500"
              >
                <option value="valor">Receita (R$)</option>
                <option value="quantidade">Quantidade Vendida</option>
                <option value="ticket_medio">Ticket Médio</option>
              </select>
            </div>
            
            <div className="flex items-center gap-2">
              <label className="text-sm text-slate-400">Exibir:</label>
              <select 
                value={filtrosProdutos.limit}
                onChange={(e) => setFiltrosProdutos({...filtrosProdutos, limit: parseInt(e.target.value)})}
                className="bg-slate-700 text-white text-sm rounded px-3 py-1.5 border border-slate-600 focus:outline-none focus:border-red-500"
              >
                <option value="5">Top 5</option>
                <option value="10">Top 10</option>
                <option value="20">Top 20</option>
              </select>
            </div>
          </div>
        </div>
        
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-700">
            <thead>
              <tr className="bg-slate-900">
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Produto</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">País</th>
                <th className="px-4 py-3 text-center text-xs font-semibold text-slate-300 uppercase">Safra</th>
                <th className="px-4 py-3 text-left text-xs font-semibold text-slate-300 uppercase">Tipo de Uva</th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-300 uppercase">Receita</th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-300 uppercase">Qtd</th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-300 uppercase">Ticket Médio</th>
                <th className="px-4 py-3 text-right text-xs font-semibold text-slate-300 uppercase">Vendas</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {rankingProdutos.map((produto, idx) => (
                <tr key={produto.produto_id} className="hover:bg-slate-750 transition-colors">
                  <td className="px-4 py-3 text-sm text-white font-medium">{produto.nome}</td>
                  <td className="px-4 py-3 text-sm text-slate-300">{produto.pais}</td>
                  <td className="px-4 py-3 text-sm text-slate-300 text-center">{produto.safra}</td>
                  <td className="px-4 py-3 text-sm text-slate-300">{produto.tipo_uva}</td>
                  <td className="px-4 py-3 text-sm text-green-400 text-right font-semibold">
                    R$ {produto.valor.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-sm text-blue-400 text-right font-medium">
                    {produto.quantidade}
                  </td>
                  <td className="px-4 py-3 text-sm text-purple-400 text-right font-medium">
                    R$ {produto.ticket_medio.toFixed(2)}
                  </td>
                  <td className="px-4 py-3 text-sm text-slate-400 text-right">
                    {produto.num_vendas}x
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Tables Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Clientes */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">
            Top 5 Clientes por Faturamento
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-700">
              <thead>
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase">
                    Cliente
                  </th>
                  <th className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase">
                    Cidade
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-medium text-slate-400 uppercase">
                    Total Gasto
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700">
                {topClientes.map((cliente, idx) => (
                  <tr key={idx}>
                    <td className="px-4 py-3 text-sm text-white">
                      {cliente.nome || `Cliente ${cliente.cliente_id}`}
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-300">
                      {cliente.cidade}
                    </td>
                    <td className="px-4 py-3 text-sm text-green-500 text-right font-medium">
                      R$ {cliente.total_gasto.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Top Produtos */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4">
            Top 5 Produtos por Faturamento
          </h3>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-slate-700">
              <thead>
                <tr>
                  <th className="px-4 py-2 text-left text-xs font-medium text-slate-400 uppercase">
                    Produto
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-medium text-slate-400 uppercase">
                    Qtd
                  </th>
                  <th className="px-4 py-2 text-right text-xs font-medium text-slate-400 uppercase">
                    Valor
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-700">
                {topProdutos.map((produto, idx) => (
                  <tr key={idx}>
                    <td className="px-4 py-3 text-sm text-white">
                      {produto.nome}
                    </td>
                    <td className="px-4 py-3 text-sm text-slate-300 text-right">
                      {produto.quantidade}
                    </td>
                    <td className="px-4 py-3 text-sm text-green-500 text-right font-medium">
                      R$ {produto.valor.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Alert Section */}
      <div className="mt-8 bg-wine-900 border border-wine-700 rounded-lg p-6">
        <div className="flex items-start">
          <AlertTriangle className="h-6 w-6 text-wine-500 mr-3 flex-shrink-0 mt-1" />
          <div>
            <h3 className="text-lg font-semibold text-white mb-2">
              Insights do Sistema
            </h3>
            <ul className="space-y-2 text-slate-300">
              <li>• Taxa de cancelamento: {(stats.taxa_cancelamento * 100).toFixed(1)}%</li>
              <li>• Clientes do clube: {stats.clientes_clube} ({((stats.clientes_clube / stats.total_clientes) * 100).toFixed(1)}%)</li>
              <li>• Ticket médio geral: R$ {stats.ticket_medio.toFixed(2)}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
