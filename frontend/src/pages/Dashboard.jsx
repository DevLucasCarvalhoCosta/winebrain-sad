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
  getDashboardStats, getTopClientes, getTopProdutos, 
  getVendasTipoUva, getVendasPais, getSegmentacao 
} from '../services/api';

const COLORS = ['#ef4444', '#f59e0b', '#10b981', '#3b82f6', '#8b5cf6', '#ec4899'];

function Dashboard() {
  const [stats, setStats] = useState(null);
  const [topClientes, setTopClientes] = useState([]);
  const [topProdutos, setTopProdutos] = useState([]);
  const [vendasUva, setVendasUva] = useState([]);
  const [vendasPais, setVendasPais] = useState([]);
  const [segmentacao, setSegmentacao] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      
      const [
        statsRes, 
        clientesRes, 
        produtosRes, 
        uvaRes, 
        paisRes,
        segmentacaoRes
      ] = await Promise.all([
        getDashboardStats(),
        getTopClientes(5),
        getTopProdutos(5),
        getVendasTipoUva(),
        getVendasPais(),
        getSegmentacao()
      ]);

      setStats(statsRes.data);
      setTopClientes(clientesRes.data);
      setTopProdutos(produtosRes.data);
      
      // Transformar dados para gráficos
      setVendasUva(
        Object.entries(uvaRes.data)
          .map(([name, value]) => ({ name, value }))
          .slice(0, 5)
      );
      
      setVendasPais(
        Object.entries(paisRes.data)
          .map(([name, value]) => ({ name, value }))
          .slice(0, 5)
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
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
            <Wine className="h-5 w-5 mr-2 text-red-500" />
            Vendas por Tipo de Uva
          </h3>
          <ResponsiveContainer width="100%" height={350}>
            <BarChart 
              data={vendasUva} 
              layout="vertical"
              margin={{ top: 10, right: 80, left: 100, bottom: 10 }}
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
                barSize={30}
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
