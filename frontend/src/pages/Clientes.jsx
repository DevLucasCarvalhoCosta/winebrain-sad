import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Users, Search, Eye, AlertCircle, Star, ArrowUpDown, ArrowUp, ArrowDown } from 'lucide-react';
import { getClientes } from '../services/api';

function Clientes() {
  const [clientes, setClientes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState(null); // 'clube', 'risco', 'cancelados'
  const [sortConfig, setSortConfig] = useState({ key: null, direction: 'asc' });

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

  // Filtrar por busca e status
  const filteredClientes = clientes.filter(cliente => {
    const matchesSearch = (cliente.nome?.toLowerCase() || '').includes(searchTerm.toLowerCase()) ||
      (cliente.cidade?.toLowerCase() || '').includes(searchTerm.toLowerCase());
    
    if (!matchesSearch) return false;
    
    // Filtrar por status
    if (filterStatus === 'clube') return cliente.assinante_clube;
    if (filterStatus === 'risco') return cliente.pontuacao_engajamento < 4;
    if (filterStatus === 'cancelados') return cliente.cancelou_assinatura;
    
    return true;
  });

  // Ordenar clientes
  const sortedClientes = React.useMemo(() => {
    let sortableClientes = [...filteredClientes];
    
    if (sortConfig.key) {
      sortableClientes.sort((a, b) => {
        let aVal = a[sortConfig.key];
        let bVal = b[sortConfig.key];
        
        // Tratamento especial para nome (pode ser null)
        if (sortConfig.key === 'nome') {
          aVal = aVal || `Cliente ${a.cliente_id}`;
          bVal = bVal || `Cliente ${b.cliente_id}`;
        }
        
        if (aVal < bVal) {
          return sortConfig.direction === 'asc' ? -1 : 1;
        }
        if (aVal > bVal) {
          return sortConfig.direction === 'asc' ? 1 : -1;
        }
        return 0;
      });
    }
    
    return sortableClientes;
  }, [filteredClientes, sortConfig]);

  const handleSort = (key) => {
    let direction = 'asc';
    if (sortConfig.key === key && sortConfig.direction === 'asc') {
      direction = 'desc';
    }
    setSortConfig({ key, direction });
  };

  const handleFilterClick = (filter) => {
    setFilterStatus(filterStatus === filter ? null : filter);
  };

  const getEngajamentoBadge = (score) => {
    if (score >= 8) return { color: 'bg-green-500', text: 'Alto' };
    if (score >= 4) return { color: 'bg-yellow-500', text: 'Médio' };
    return { color: 'bg-red-500', text: 'Baixo' };
  };

  const getSortIcon = (columnKey) => {
    if (sortConfig.key !== columnKey) {
      return <ArrowUpDown className="h-4 w-4 text-slate-500" />;
    }
    return sortConfig.direction === 'asc' 
      ? <ArrowUp className="h-4 w-4 text-wine-500" />
      : <ArrowDown className="h-4 w-4 text-wine-500" />;
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

      {/* Stats Cards - Clicáveis com filtro */}
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

        <button
          onClick={() => handleFilterClick('clube')}
          className={`bg-slate-800 rounded-lg p-4 border-2 transition-all duration-200 hover:scale-105 text-left ${
            filterStatus === 'clube' 
              ? 'border-yellow-500 shadow-lg shadow-yellow-500/50 ring-2 ring-yellow-500/20' 
              : 'border-slate-700 hover:border-yellow-500/50'
          }`}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Clube</p>
              <p className="text-2xl font-bold text-white">
                {clientes.filter(c => c.assinante_clube).length}
              </p>
              {filterStatus === 'clube' && (
                <p className="text-xs text-yellow-400 mt-1">✓ Filtro ativo</p>
              )}
            </div>
            <Star className={`h-8 w-8 ${filterStatus === 'clube' ? 'text-yellow-400' : 'text-yellow-500'}`} />
          </div>
        </button>

        <button
          onClick={() => handleFilterClick('risco')}
          className={`bg-slate-800 rounded-lg p-4 border-2 transition-all duration-200 hover:scale-105 text-left ${
            filterStatus === 'risco' 
              ? 'border-red-500 shadow-lg shadow-red-500/50 ring-2 ring-red-500/20' 
              : 'border-slate-700 hover:border-red-500/50'
          }`}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Em Risco</p>
              <p className="text-2xl font-bold text-white">
                {clientes.filter(c => c.pontuacao_engajamento < 4).length}
              </p>
              {filterStatus === 'risco' && (
                <p className="text-xs text-red-400 mt-1">✓ Filtro ativo</p>
              )}
            </div>
            <AlertCircle className={`h-8 w-8 ${filterStatus === 'risco' ? 'text-red-400' : 'text-red-500'}`} />
          </div>
        </button>

        <button
          onClick={() => handleFilterClick('cancelados')}
          className={`bg-slate-800 rounded-lg p-4 border-2 transition-all duration-200 hover:scale-105 text-left ${
            filterStatus === 'cancelados' 
              ? 'border-orange-500 shadow-lg shadow-orange-500/50 ring-2 ring-orange-500/20' 
              : 'border-slate-700 hover:border-orange-500/50'
          }`}
        >
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm">Cancelados</p>
              <p className="text-2xl font-bold text-white">
                {clientes.filter(c => c.cancelou_assinatura).length}
              </p>
              {filterStatus === 'cancelados' && (
                <p className="text-xs text-orange-400 mt-1">✓ Filtro ativo</p>
              )}
            </div>
            <AlertCircle className={`h-8 w-8 ${filterStatus === 'cancelados' ? 'text-orange-400' : 'text-orange-500'}`} />
          </div>
        </button>
      </div>

      {/* Filtro ativo indicator */}
      {filterStatus && (
        <div className="mb-4 flex items-center justify-between bg-slate-800 rounded-lg p-3 border border-slate-700">
          <p className="text-sm text-slate-300">
            Mostrando: <span className="font-semibold text-white">
              {filterStatus === 'clube' && 'Clientes do Clube'}
              {filterStatus === 'risco' && 'Clientes em Risco'}
              {filterStatus === 'cancelados' && 'Clientes Cancelados'}
            </span> ({sortedClientes.length} resultado{sortedClientes.length !== 1 ? 's' : ''})
          </p>
          <button
            onClick={() => setFilterStatus(null)}
            className="text-xs bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded-md transition"
          >
            Limpar Filtro
          </button>
        </div>
      )}

      {/* Table */}
      <div className="bg-slate-800 rounded-lg border border-slate-700 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-700">
            <thead className="bg-slate-900">
              <tr>
                <th 
                  onClick={() => handleSort('cliente_id')}
                  className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:bg-slate-800 transition"
                >
                  <div className="flex items-center space-x-1">
                    <span>Código</span>
                    {getSortIcon('cliente_id')}
                  </div>
                </th>
                <th 
                  onClick={() => handleSort('nome')}
                  className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:bg-slate-800 transition"
                >
                  <div className="flex items-center space-x-1">
                    <span>Cliente</span>
                    {getSortIcon('nome')}
                  </div>
                </th>
                <th 
                  onClick={() => handleSort('cidade')}
                  className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:bg-slate-800 transition"
                >
                  <div className="flex items-center space-x-1">
                    <span>Cidade</span>
                    {getSortIcon('cidade')}
                  </div>
                </th>
                <th 
                  onClick={() => handleSort('pontuacao_engajamento')}
                  className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:bg-slate-800 transition"
                >
                  <div className="flex items-center space-x-1">
                    <span>Engajamento</span>
                    {getSortIcon('pontuacao_engajamento')}
                  </div>
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Status
                </th>
                <th 
                  onClick={() => handleSort('total_gasto')}
                  className="px-6 py-3 text-right text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:bg-slate-800 transition"
                >
                  <div className="flex items-center justify-end space-x-1">
                    <span>Total Gasto</span>
                    {getSortIcon('total_gasto')}
                  </div>
                </th>
                <th 
                  onClick={() => handleSort('n_compras')}
                  className="px-6 py-3 text-center text-xs font-medium text-slate-400 uppercase tracking-wider cursor-pointer hover:bg-slate-800 transition"
                >
                  <div className="flex items-center justify-center space-x-1">
                    <span>Compras</span>
                    {getSortIcon('n_compras')}
                  </div>
                </th>
                <th className="px-6 py-3 text-center text-xs font-medium text-slate-400 uppercase tracking-wider">
                  Ações
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-700">
              {sortedClientes.map((cliente) => {
                const engajamento = getEngajamentoBadge(cliente.pontuacao_engajamento);
                return (
                  <tr key={cliente.cliente_id} className="hover:bg-slate-700 transition">
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-400 font-mono">
                      #{cliente.cliente_id}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-white">
                        {cliente.nome || `Cliente ${cliente.cliente_id}`}
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

      {sortedClientes.length === 0 && (
        <div className="text-center py-12 text-slate-400">
          Nenhum cliente encontrado com os critérios de busca.
        </div>
      )}
    </div>
  );
}

export default Clientes;
