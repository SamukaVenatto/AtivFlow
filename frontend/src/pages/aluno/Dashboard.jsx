/**
 * Dashboard do Aluno
 * Visão geral com cards de resumo, atividades e notificações
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [atividades, setAtividades] = useState([]);
  const [notificacoes, setNotificacoes] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      const [atividadesRes, notificacoesRes] = await Promise.all([
        api.get('/atividades'),
        api.get('/notificacoes?lida=false')
      ]);
      
      setAtividades(atividadesRes.data.atividades || []);
      setNotificacoes(notificacoesRes.data.notificacoes || []);
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-senac-blue"></div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-senac-blue text-white shadow-lg">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">AtivFlow</h1>
            <p className="text-sm text-gray-200">Bem-vindo, {user?.nome_completo}</p>
          </div>
          <button
            onClick={handleLogout}
            className="bg-white text-senac-blue px-4 py-2 rounded hover:bg-gray-100 transition-colors"
          >
            Sair
          </button>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Cards de Resumo */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Atividades Pendentes</h3>
            <p className="text-4xl font-bold text-senac-blue">{atividades.length}</p>
          </div>
          
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Notificações</h3>
            <p className="text-4xl font-bold text-orange-500">{notificacoes.length}</p>
          </div>
          
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Turma</h3>
            <p className="text-2xl font-bold text-gray-800">{user?.turma}</p>
          </div>
        </div>

        {/* Lista de Atividades */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Atividades Recentes</h2>
          
          {atividades.length === 0 ? (
            <p className="text-gray-600 text-center py-8">Nenhuma atividade disponível</p>
          ) : (
            <div className="space-y-4">
              {atividades.slice(0, 5).map((atividade) => (
                <div
                  key={atividade.id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
                  onClick={() => navigate(`/aluno/atividades/${atividade.id}`)}
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="font-semibold text-lg text-gray-800">{atividade.titulo}</h3>
                      <p className="text-gray-600 text-sm mt-1">{atividade.descricao}</p>
                      <div className="flex gap-4 mt-2">
                        <span className="text-xs bg-senac-blue text-white px-2 py-1 rounded">
                          {atividade.tipo}
                        </span>
                        <span className="text-xs text-gray-600">
                          Prazo: {new Date(atividade.prazo).toLocaleDateString('pt-BR')}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Notificações */}
        {notificacoes.length > 0 && (
          <div className="card mt-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-6">Notificações</h2>
            <div className="space-y-3">
              {notificacoes.slice(0, 5).map((notif) => (
                <div key={notif.id} className="border-l-4 border-senac-blue bg-blue-50 p-4 rounded">
                  <h4 className="font-semibold text-gray-800">{notif.titulo}</h4>
                  <p className="text-sm text-gray-600 mt-1">{notif.mensagem}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Dashboard;

