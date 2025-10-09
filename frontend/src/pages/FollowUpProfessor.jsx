import React, { useState, useEffect } from 'react';
import { Eye, CheckCircle, Download, Filter, Search, Calendar, User } from 'lucide-react';

const FollowUpProfessor = () => {
  const [followUps, setFollowUps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filtros, setFiltros] = useState({
    aluno_id: '',
    realizado: '',
    revisado: '',
    date_from: '',
    date_to: '',
    search: ''
  });
  const [alunos, setAlunos] = useState([]);
  const [estatisticas, setEstatisticas] = useState({
    total: 0,
    realizadas: 0,
    nao_realizadas: 0,
    revisadas: 0,
    pendentes: 0
  });

  useEffect(() => {
    carregarDados();
    carregarAlunos();
  }, []);

  useEffect(() => {
    carregarFollowUps();
  }, [filtros]);

  const carregarDados = async () => {
    await Promise.all([
      carregarFollowUps(),
      carregarAlunos()
    ]);
  };

  const carregarFollowUps = async () => {
    try {
      setLoading(true);
      
      // Construir query string com filtros
      const params = new URLSearchParams();
      Object.entries(filtros).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });

      const response = await fetch(`/api/admin/followups?${params}`);
      if (response.ok) {
        const data = await response.json();
        setFollowUps(data.followups || []);
        
        // Calcular estatísticas
        const total = data.followups?.length || 0;
        const realizadas = data.followups?.filter(f => f.realizado).length || 0;
        const nao_realizadas = total - realizadas;
        const revisadas = data.followups?.filter(f => f.revisado).length || 0;
        const pendentes = total - revisadas;
        
        setEstatisticas({
          total,
          realizadas,
          nao_realizadas,
          revisadas,
          pendentes
        });
      }
    } catch (error) {
      console.error('Erro ao carregar follow-ups:', error);
    } finally {
      setLoading(false);
    }
  };

  const carregarAlunos = async () => {
    try {
      const response = await fetch('/api/alunos/');
      if (response.ok) {
        const data = await response.json();
        setAlunos(data.alunos || []);
      }
    } catch (error) {
      console.error('Erro ao carregar alunos:', error);
    }
  };

  const marcarComoRevisado = async (followUpId) => {
    try {
      const response = await fetch(`/api/admin/followups/${followUpId}/revisar`, {
        method: 'PUT'
      });

      if (response.ok) {
        alert('Follow-up marcado como revisado!');
        carregarFollowUps();
      } else {
        const error = await response.json();
        alert('Erro: ' + (error.error || 'Erro ao marcar como revisado'));
      }
    } catch (error) {
      console.error('Erro ao marcar como revisado:', error);
      alert('Erro ao marcar como revisado');
    }
  };

  const exportarCSV = async () => {
    try {
      const params = new URLSearchParams();
      Object.entries(filtros).forEach(([key, value]) => {
        if (value) params.append(key, value);
      });

      const response = await fetch(`/api/admin/followups/export?${params}`);
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `followups_${new Date().toISOString().split('T')[0]}.csv`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Erro ao exportar CSV:', error);
      alert('Erro ao exportar CSV');
    }
  };

  const limparFiltros = () => {
    setFiltros({
      aluno_id: '',
      realizado: '',
      revisado: '',
      date_from: '',
      date_to: '',
      search: ''
    });
  };

  const formatarData = (data) => {
    return new Date(data).toLocaleDateString('pt-BR');
  };

  const formatarDataHora = (data) => {
    return new Date(data).toLocaleString('pt-BR');
  };

  return (
    <div className="p-6">
      {/* Cabeçalho */}
      <div className="bg-gradient-to-r from-green-600 to-green-800 text-white p-6 rounded-lg mb-6">
        <h1 className="text-2xl font-bold text-center">
          FOLLOW UP - ACOMPANHAMENTO PROFESSOR
        </h1>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-6">
        <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
          <div className="text-2xl font-bold text-blue-600">{estatisticas.total}</div>
          <div className="text-sm text-blue-700">Total</div>
        </div>
        
        <div className="bg-green-50 p-4 rounded-lg border border-green-200">
          <div className="text-2xl font-bold text-green-600">{estatisticas.realizadas}</div>
          <div className="text-sm text-green-700">Realizadas</div>
        </div>
        
        <div className="bg-red-50 p-4 rounded-lg border border-red-200">
          <div className="text-2xl font-bold text-red-600">{estatisticas.nao_realizadas}</div>
          <div className="text-sm text-red-700">Não Realizadas</div>
        </div>
        
        <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
          <div className="text-2xl font-bold text-purple-600">{estatisticas.revisadas}</div>
          <div className="text-sm text-purple-700">Revisadas</div>
        </div>
        
        <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
          <div className="text-2xl font-bold text-yellow-600">{estatisticas.pendentes}</div>
          <div className="text-sm text-yellow-700">Pendentes</div>
        </div>
      </div>

      {/* Filtros */}
      <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200 mb-6">
        <div className="flex items-center gap-2 mb-4">
          <Filter size={20} className="text-gray-600" />
          <h3 className="text-lg font-semibold text-gray-800">Filtros</h3>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Aluno
            </label>
            <select
              value={filtros.aluno_id}
              onChange={(e) => setFiltros({...filtros, aluno_id: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="">Todos os alunos</option>
              {alunos.map(aluno => (
                <option key={aluno.id} value={aluno.id}>
                  {aluno.nome}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Status
            </label>
            <select
              value={filtros.realizado}
              onChange={(e) => setFiltros({...filtros, realizado: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="">Todos</option>
              <option value="true">Realizadas</option>
              <option value="false">Não Realizadas</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Revisão
            </label>
            <select
              value={filtros.revisado}
              onChange={(e) => setFiltros({...filtros, revisado: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            >
              <option value="">Todos</option>
              <option value="true">Revisadas</option>
              <option value="false">Pendentes</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Data Início
            </label>
            <input
              type="date"
              value={filtros.date_from}
              onChange={(e) => setFiltros({...filtros, date_from: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Data Fim
            </label>
            <input
              type="date"
              value={filtros.date_to}
              onChange={(e) => setFiltros({...filtros, date_to: e.target.value})}
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Buscar
            </label>
            <input
              type="text"
              value={filtros.search}
              onChange={(e) => setFiltros({...filtros, search: e.target.value})}
              placeholder="Buscar atividade..."
              className="w-full p-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent"
            />
          </div>
        </div>

        <div className="flex gap-3 mt-4">
          <button
            onClick={limparFiltros}
            className="bg-gray-500 hover:bg-gray-600 text-white px-4 py-2 rounded-lg transition-colors"
          >
            Limpar Filtros
          </button>
          
          <button
            onClick={exportarCSV}
            className="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
          >
            <Download size={18} />
            Exportar CSV
          </button>
        </div>
      </div>

      {/* Tabela */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800">
            Follow-ups dos Alunos ({followUps.length})
          </h2>
        </div>

        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-600"></div>
          </div>
        ) : followUps.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <User size={48} className="mx-auto mb-4 text-gray-300" />
            <p className="text-lg">Nenhum follow-up encontrado</p>
            <p className="text-sm">Ajuste os filtros ou aguarde os alunos registrarem atividades</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-green-600 text-white">
                <tr>
                  <th className="px-4 py-3 text-left font-medium">ALUNO</th>
                  <th className="px-4 py-3 text-left font-medium">ATIVIDADE</th>
                  <th className="px-4 py-3 text-left font-medium">DATA</th>
                  <th className="px-4 py-3 text-left font-medium">FUNÇÃO</th>
                  <th className="px-4 py-3 text-center font-medium">REALIZADO</th>
                  <th className="px-4 py-3 text-left font-medium">JUSTIFICATIVA</th>
                  <th className="px-4 py-3 text-center font-medium">STATUS</th>
                  <th className="px-4 py-3 text-center font-medium">AÇÕES</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {followUps.map((followUp, index) => (
                  <tr key={followUp.id} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-4 py-3 text-sm font-medium text-gray-900">
                      {followUp.aluno?.nome || 'N/A'}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 max-w-xs">
                      <div className="truncate" title={followUp.atividade_texto}>
                        {followUp.atividade_texto}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {formatarData(followUp.data_realizacao)}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {followUp.funcao || '-'}
                    </td>
                    <td className="px-4 py-3 text-center">
                      {followUp.realizado ? (
                        <CheckCircle className="w-5 h-5 text-green-500 mx-auto" />
                      ) : (
                        <div className="w-5 h-5 rounded-full border-2 border-red-500 mx-auto"></div>
                      )}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900 max-w-xs">
                      <div className="truncate" title={followUp.justificativa}>
                        {followUp.justificativa || '-'}
                      </div>
                    </td>
                    <td className="px-4 py-3 text-center">
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        followUp.revisado 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-yellow-100 text-yellow-800'
                      }`}>
                        {followUp.revisado ? 'Revisado' : 'Pendente'}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-center">
                      {!followUp.revisado && (
                        <button
                          onClick={() => marcarComoRevisado(followUp.id)}
                          className="bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded text-xs transition-colors"
                          title="Marcar como revisado"
                        >
                          <CheckCircle size={14} />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default FollowUpProfessor;
