import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { 
  ArrowLeft, User, MapPin, Mail, Phone, Calendar, 
  TrendingUp, ShoppingBag, DollarSign, AlertTriangle,
  CheckCircle, XCircle, Star, Lightbulb
} from 'lucide-react';
import { getCliente, getRecomendacao } from '../services/api';

function ClienteDetalhes() {
  const { id } = useParams();
  const [cliente, setCliente] = useState(null);
  const [recomendacao, setRecomendacao] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadClienteData();
  }, [id]);

  const loadClienteData = async () => {
    try {
      setLoading(true);
      const [clienteRes, recomendacaoRes] = await Promise.all([
        getCliente(id),
        getRecomendacao(id)
      ]);
      setCliente(clienteRes.data);
      setRecomendacao(recomendacaoRes.data);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const getPrioridadeColor = (prioridade) => {
    const colors = {
      'critica': 'bg-red-500',
      'alta': 'bg-orange-500',
      'media': 'bg-yellow-500',
      'baixa': 'bg-green-500'
    };
    return colors[prioridade] || 'bg-gray-500';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-white text-xl">Carregando dados do cliente...</div>
      </div>
    );
  }

  if (!cliente || !recomendacao) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-white text-xl">Cliente não encontrado</div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Back Button */}
      <Link
        to="/clientes"
        className="inline-flex items-center text-slate-400 hover:text-white mb-6 transition"
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Voltar para Clientes
      </Link>

      {/* Header */}
      <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-6">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-wine-600 rounded-full p-4">
              <User className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white mb-1">
                {cliente.nome || `Cliente ${cliente.cliente_id}`}
              </h1>
              <div className="flex items-center space-x-4 text-slate-400">
                <span className="flex items-center">
                  <MapPin className="h-4 w-4 mr-1" />
                  {cliente.cidade}
                </span>
                {cliente.idade && (
                  <span>{cliente.idade} anos</span>
                )}
              </div>
            </div>
          </div>
          
          <div className="flex flex-col items-end space-y-2">
            {cliente.assinante_clube && (
              <span className="px-3 py-1 bg-yellow-500 text-white text-sm font-medium rounded-full flex items-center">
                <Star className="h-4 w-4 mr-1" />
                Assinante Clube
              </span>
            )}
            {cliente.cancelou_assinatura && (
              <span className="px-3 py-1 bg-red-500 text-white text-sm font-medium rounded-full">
                Cancelou Assinatura
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        {/* Métricas */}
        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Total Gasto</h3>
            <DollarSign className="h-6 w-6 text-green-500" />
          </div>
          <p className="text-3xl font-bold text-green-500">
            R$ {cliente.total_gasto.toFixed(2)}
          </p>
          <p className="text-sm text-slate-400 mt-2">
            Ticket médio: R$ {cliente.ticket_medio.toFixed(2)}
          </p>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Compras</h3>
            <ShoppingBag className="h-6 w-6 text-blue-500" />
          </div>
          <p className="text-3xl font-bold text-blue-500">
            {cliente.n_compras}
          </p>
          <p className="text-sm text-slate-400 mt-2">
            Total de compras realizadas
          </p>
        </div>

        <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-white">Engajamento</h3>
            <TrendingUp className="h-6 w-6 text-purple-500" />
          </div>
          <p className="text-3xl font-bold text-purple-500">
            {cliente.pontuacao_engajamento.toFixed(1)}
          </p>
          <p className="text-sm text-slate-400 mt-2">
            Nível: {recomendacao.nivel_engajamento}
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Análise de Risco */}
        <div className="lg:col-span-1">
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700 mb-6">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <AlertTriangle className="h-5 w-5 mr-2 text-orange-500" />
              Análise de Risco
            </h3>
            
            <div className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <span className="text-sm text-slate-400">Probabilidade de Churn</span>
                  <span className="text-sm font-medium text-white">
                    {(recomendacao.metricas.probabilidade_churn * 100).toFixed(1)}%
                  </span>
                </div>
                <div className="w-full bg-slate-700 rounded-full h-2">
                  <div
                    className={`h-2 rounded-full ${
                      recomendacao.metricas.probabilidade_churn > 0.7
                        ? 'bg-red-500'
                        : recomendacao.metricas.probabilidade_churn > 0.4
                        ? 'bg-yellow-500'
                        : 'bg-green-500'
                    }`}
                    style={{ width: `${recomendacao.metricas.probabilidade_churn * 100}%` }}
                  />
                </div>
              </div>

              <div className="pt-4 border-t border-slate-700">
                <p className="text-sm font-medium text-slate-400 mb-2">Segmento</p>
                <p className="text-lg font-bold text-white">{recomendacao.segmento}</p>
              </div>

              <div className="pt-4 border-t border-slate-700">
                <p className="text-sm font-medium text-slate-400 mb-2">Prioridade</p>
                <span className={`inline-block px-3 py-1 rounded-full text-white text-sm font-medium ${getPrioridadeColor(recomendacao.prioridade)}`}>
                  {recomendacao.prioridade.toUpperCase()}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Recomendações */}
        <div className="lg:col-span-2">
          <div className="bg-slate-800 rounded-lg p-6 border border-slate-700">
            <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
              <Lightbulb className="h-5 w-5 mr-2 text-yellow-500" />
              Recomendações Inteligentes
            </h3>

            {/* Mensagem Principal */}
            <div className="bg-wine-900 border border-wine-700 rounded-lg p-4 mb-6">
              <p className="text-white">{recomendacao.mensagem}</p>
            </div>

            {/* Ações Recomendadas */}
            <div className="space-y-4">
              {recomendacao.acoes_recomendadas.map((acao, idx) => (
                <div
                  key={idx}
                  className="bg-slate-900 border border-slate-700 rounded-lg p-4 hover:border-wine-500 transition"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex-1">
                      <h4 className="text-white font-medium mb-1">{acao.regra}</h4>
                      <p className="text-sm text-slate-400 mb-2">{acao.condicao}</p>
                    </div>
                    <span className={`px-2 py-1 rounded text-xs font-medium text-white ml-4 ${getPrioridadeColor(acao.prioridade)}`}>
                      {acao.prioridade}
                    </span>
                  </div>
                  
                  <div className="bg-slate-800 rounded p-3">
                    <p className="text-sm text-white mb-1">
                      <strong>Ação:</strong> {acao.acao}
                    </p>
                    <p className="text-sm text-slate-300">
                      {acao.descricao}
                    </p>
                  </div>
                </div>
              ))}
            </div>

            {recomendacao.acoes_recomendadas.length === 0 && (
              <div className="text-center py-8 text-slate-400">
                <CheckCircle className="h-12 w-12 mx-auto mb-2 text-green-500" />
                <p>Nenhuma ação crítica necessária no momento.</p>
                <p className="text-sm mt-1">Cliente com comportamento estável.</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Métricas Detalhadas */}
      <div className="mt-6 bg-slate-800 rounded-lg p-6 border border-slate-700">
        <h3 className="text-lg font-semibold text-white mb-4">Métricas Detalhadas</h3>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="text-center">
            <p className="text-slate-400 text-sm mb-1">Engajamento</p>
            <p className="text-2xl font-bold text-white">
              {recomendacao.metricas.engajamento.toFixed(2)}
            </p>
          </div>
          <div className="text-center">
            <p className="text-slate-400 text-sm mb-1">Total Gasto</p>
            <p className="text-2xl font-bold text-green-500">
              R$ {recomendacao.metricas.total_gasto.toFixed(2)}
            </p>
          </div>
          <div className="text-center">
            <p className="text-slate-400 text-sm mb-1">Nº Compras</p>
            <p className="text-2xl font-bold text-blue-500">
              {recomendacao.metricas.n_compras}
            </p>
          </div>
          <div className="text-center">
            <p className="text-slate-400 text-sm mb-1">Prob. Churn</p>
            <p className="text-2xl font-bold text-red-500">
              {(recomendacao.metricas.probabilidade_churn * 100).toFixed(1)}%
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ClienteDetalhes;
