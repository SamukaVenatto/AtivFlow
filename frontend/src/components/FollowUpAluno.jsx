import React, { useState, useEffect } from 'react';
import { Plus, Calendar, User, CheckCircle, XCircle, Send } from 'lucide-react';

const FollowUpAluno = () => {
  const [followUps, setFollowUps] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    atividade_texto: '',
    data_realizacao: new Date().toISOString().split('T')[0],
    funcao: '',
    realizado: true,
    justificativa: ''
  });

  useEffect(() => {
    carregarFollowUps();
  }, []);

  const carregarFollowUps = async () => {
    try {
      const response = await fetch('/api/followups/me');
      if (response.ok) {
        const data = await response.json();
        setFollowUps(data.followups || []);
      }
    } catch (error) {
      console.error('Erro ao carregar follow-ups:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!formData.atividade_texto.trim()) {
      alert('Por favor, descreva a atividade realizada');
      return;
    }

    try {
      const response = await fetch('/api/followups', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        alert('Follow-up enviado com sucesso!');
        setFormData({
          atividade_texto: '',
          data_realizacao: new Date().toISOString().split('T')[0],
          funcao: '',
          realizado: true,
          justificativa: ''
        });
        setShowForm(false);
        carregarFollowUps();
      } else {
        const error = await response.json();
        alert('Erro: ' + (error.error || 'Erro ao enviar follow-up'));
      }
    } catch (error) {
      console.error('Erro ao enviar follow-up:', error);
      alert('Erro ao enviar follow-up');
    }
  };

  const formatarData = (data) => {
    return new Date(data).toLocaleDateString('pt-BR');
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      {/* Cabeçalho */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6 rounded-lg mb-6">
        <h1 className="text-2xl font-bold text-center">
          FOLLOW UP - PREENCHIMENTO INDIVIDUAL
        </h1>
      </div>

      {/* Botão Adicionar */}
      <div className="mb-6 flex justify-end">
        <button
          onClick={() => setShowForm(!showForm)}
          className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors"
        >
          <Plus size={20} />
          Nova Atividade
        </button>
      </div>

      {/* Formulário */}
      {showForm && (
        <div className="bg-white border border-gray-200 rounded-lg p-6 mb-6 shadow-sm">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">
            Registrar Nova Atividade
          </h3>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Data de Realização
                </label>
                <input
                  type="date"
                  value={formData.data_realizacao}
                  onChange={(e) => setFormData({...formData, data_realizacao: e.target.value})}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Função/Responsabilidade
                </label>
                <input
                  type="text"
                  value={formData.funcao}
                  onChange={(e) => setFormData({...formData, funcao: e.target.value})}
                  placeholder="Ex: Estudos, Desenvolvimento, Pesquisa..."
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Atividade Realizada
              </label>
              <textarea
                value={formData.atividade_texto}
                onChange={(e) => setFormData({...formData, atividade_texto: e.target.value})}
                placeholder="Descreva detalhadamente a atividade que você realizou..."
                rows={4}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Status
              </label>
              <select
                value={formData.realizado}
                onChange={(e) => setFormData({...formData, realizado: e.target.value === 'true'})}
                className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="true">Realizado</option>
                <option value="false">Não Realizado</option>
              </select>
            </div>

            {!formData.realizado && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Justificativa (obrigatória para atividades não realizadas)
                </label>
                <textarea
                  value={formData.justificativa}
                  onChange={(e) => setFormData({...formData, justificativa: e.target.value})}
                  placeholder="Explique por que a atividade não foi realizada..."
                  rows={3}
                  className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  required={!formData.realizado}
                />
              </div>
            )}

            <div className="flex gap-3 pt-4">
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors"
              >
                <Send size={18} />
                ENVIAR ATIVIDADE
              </button>
              
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="bg-gray-500 hover:bg-gray-600 text-white px-6 py-3 rounded-lg transition-colors"
              >
                Cancelar
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Tabela de Follow-ups */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="bg-gray-50 px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-800">
            Histórico de Atividades
          </h2>
        </div>

        {followUps.length === 0 ? (
          <div className="p-8 text-center text-gray-500">
            <User size={48} className="mx-auto mb-4 text-gray-300" />
            <p className="text-lg">Nenhuma atividade registrada ainda</p>
            <p className="text-sm">Clique em "Nova Atividade" para começar</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-blue-600 text-white">
                <tr>
                  <th className="px-4 py-3 text-left font-medium">NOME</th>
                  <th className="px-4 py-3 text-left font-medium">ATIVIDADE REALIZADA</th>
                  <th className="px-4 py-3 text-left font-medium">DATA DE REALIZAÇÃO</th>
                  <th className="px-4 py-3 text-left font-medium">FUNÇÃO/RESPONSABILIDADE</th>
                  <th className="px-4 py-3 text-center font-medium">REALIZADO</th>
                  <th className="px-4 py-3 text-left font-medium">JUSTIFICATIVA</th>
                  <th className="px-4 py-3 text-center font-medium">STATUS</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {followUps.map((followUp, index) => (
                  <tr key={followUp.id} className={index % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {followUp.aluno?.nome || 'Você'}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {followUp.atividade_texto}
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
                        <XCircle className="w-5 h-5 text-red-500 mx-auto" />
                      )}
                    </td>
                    <td className="px-4 py-3 text-sm text-gray-900">
                      {followUp.justificativa || '-'}
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
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Estatísticas */}
      {followUps.length > 0 && (
        <div className="mt-6 grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
            <div className="text-2xl font-bold text-blue-600">
              {followUps.length}
            </div>
            <div className="text-sm text-blue-700">Total de Atividades</div>
          </div>
          
          <div className="bg-green-50 p-4 rounded-lg border border-green-200">
            <div className="text-2xl font-bold text-green-600">
              {followUps.filter(f => f.realizado).length}
            </div>
            <div className="text-sm text-green-700">Realizadas</div>
          </div>
          
          <div className="bg-yellow-50 p-4 rounded-lg border border-yellow-200">
            <div className="text-2xl font-bold text-yellow-600">
              {followUps.filter(f => !f.revisado).length}
            </div>
            <div className="text-sm text-yellow-700">Pendentes de Revisão</div>
          </div>
          
          <div className="bg-purple-50 p-4 rounded-lg border border-purple-200">
            <div className="text-2xl font-bold text-purple-600">
              {followUps.filter(f => f.revisado).length}
            </div>
            <div className="text-sm text-purple-700">Revisadas</div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FollowUpAluno;
