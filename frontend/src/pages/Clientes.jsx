import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Users, Search, Eye, AlertCircle, Star } from 'lucide-react';
import { getClientes } from '../services/api';

function Clientes() {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadClientes();
  }, []);

  const loadClientes = async () => {
    try {
      setLoading(true);
      const response = await getClientes(100, 0); // Carregar todos
      setClientes(response.data);
    } catch (error) {
      console.error('Erro ao carregar clientes:', error);
    } finally {
      setLoading(false);
    }
  };

  const filteredClientes = clientes.filter(cliente =>
    (cliente.nome?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
    (cliente.cidade?.toLowerCase() || '').includes(searchTerm.toLowerCase())
  );

  const getEngajamentoBadge = (score) => {
    if (score >= 8) return { color: 'bg-green-500', text: 'Alto' };
    if (score >= 4) return { color: 'bg-yellow-500', text: 'Médio' };
    return { color: 'bg-red-500', text: 'Baixo' };
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-white text-xl">Carregando clientes...</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-white mb-2">Gestão de Clientes</h1>
        <p className="text-slate-400">
          Análise detalhada de {clientes.length} clientes cadastrados
        </p>
      </div>

      {/* Search Bar */}
      <div className="mb-6">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-slate-400" />
          <input
            type="text"
            placeholder="Buscar por nome ou cidade..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-10 pr-4 py-3 bg-slate-800 border border-slate-700 rounded-lg text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-wine-500"
          />
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Total</p>
              <p className="text-2xl font-bold text-white">{clientes.length}</p>
            </div>
            <Users className="h-8 w-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Clube</p>
              <p className="text-2xl font-bold text-white">
                {clientes.filter(c => c.assinante_clube).length}
              </p>
            </div>
            <Star className="h-8 w-8 text-yellow-500" />
          </div>
        </div>

        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Em Risco</p>
              <p className="text-2xl font-bold text-white">
                {clientes.filter(c => c.pontuacao_engajamento < 4).length}
              </p>
            </div>
            <AlertCircle className="h-8 w-8 text-red-500" />
          </div>
        </div>

        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Cancelados</p>
              <p className="text-2xl font-bold text-white">
                {clientes.filter(c => c.cancelou_assinatura).length}
              </p>
            </div>
            <AlertCircle className="h-8 w-8 text-orange-500" />
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-700">
            <thead className="bg-slate-900">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Cliente
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Cidade
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Engajamento
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Status
                </th>
                <th className="px-6 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Total Gasto
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Compras
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {filteredClientes.map((cliente) => {
                const engajamento = getEngajamentoBadge(cliente.pontuacao_engajamento);
                return (
                  <tr key={cliente.cliente_id} className="hover:bg-slate-700 transition">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <div>
                          <div className="text-sm font-medium text-white">
                            {cliente.nome || `Cliente ${cliente.cliente_id}`}
                          </div>
                          <div className="text-sm text-slate-400">
                            ID: {cliente.cliente_id}
                          </div>
                        </div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300">
                      {cliente.cidade}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <span className={`px-2 py-1 text-xs font-medium rounded-full ${engajamento.color} text-white`}>
                          {engajamento.text}
                        </span>
                        <span className="ml-2 text-sm text-slate-400">
                          {cliente.pontuacao_engajamento.toFixed(1)}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex flex-col space-y-1">
                        {cliente.assinante_clube && (
                          <span className="px-2 py-1 text-xs font-medium rounded-full bg-yellow-500 text-white inline-flex items-center w-fit">
                            <Star className="h-3 w-3 mr-1" />
                            Clube
                          </span>
                        )}
                        {cliente.cancelou_assinatura && (
                          <span className="px-2 py-1 text-xs font-medium rounded-full bg-red-500 text-white w-fit">
                            Cancelou
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-green-500 text-right font-medium">
                      R$ {cliente.total_gasto.toFixed(2)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-300 text-center">
                      {cliente.n_compras}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-center">
                      <Link
                        to={`/clientes/${cliente.cliente_id}`}
                        className="inline-flex items-center px-3 py-1 bg-wine-600 hover:bg-wine-700 text-white text-sm rounded-md transition"
                      >
                        <Eye className="h-4 w-4 mr-1" />
                        Ver Detalhes
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>

      {filteredClientes.length === 0 && (
        <div className="text-center py-12 text-slate-400">
          Nenhum cliente encontrado com os critérios de busca.
        </div>
      )}
    </div>
  );
}

export default Clientes;
