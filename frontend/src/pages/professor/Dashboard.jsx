/**
 * Dashboard do Professor
 * Visão geral com estatísticas, atividades e gestão
 */
import { useState, useEffect } from 'react';
import { useAuth } from '../../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import api from '../../services/api';

const Dashboard = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [atividades, setAtividades] = useState([]);
  const [alunos, setAlunos] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    carregarDados();
  }, []);

  const carregarDados = async () => {
    try {
      const [atividadesRes, alunosRes] = await Promise.all([
        api.get('/atividades'),
        api.get('/alunos?turma=' + user.turma)
      ]);
      
      setAtividades(atividadesRes.data.atividades || []);
      setAlunos(alunosRes.data.alunos || []);
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
            <h1 className="text-2xl font-bold">AtivFlow - Professor</h1>
            <p className="text-sm text-gray-200">Bem-vindo, Prof. {user?.nome_completo}</p>
          </div>
          <div className="flex gap-4">
            <button
              onClick={() => navigate('/professor/atividades/nova')}
              className="bg-white text-senac-blue px-4 py-2 rounded hover:bg-gray-100 transition-colors"
            >
              + Nova Atividade
            </button>
            <button
              onClick={handleLogout}
              className="bg-senac-blue-dark text-white px-4 py-2 rounded hover:bg-senac-blue transition-colors"
            >
              Sair
            </button>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Cards de Resumo */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Total de Alunos</h3>
            <p className="text-4xl font-bold text-senac-blue">{alunos.length}</p>
          </div>
          
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Atividades Ativas</h3>
            <p className="text-4xl font-bold text-green-600">{atividades.filter(a => a.ativo).length}</p>
          </div>
          
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Turma</h3>
            <p className="text-2xl font-bold text-gray-800">{user?.turma}</p>
          </div>
          
          <div className="card">
            <h3 className="text-lg font-semibold text-gray-700 mb-2">Curso</h3>
            <p className="text-xl font-bold text-gray-800">{user?.curso}</p>
          </div>
        </div>

        {/* Ações Rápidas */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <button
            onClick={() => navigate('/professor/atividades')}
            className="card hover:bg-senac-blue hover:text-white transition-all text-left"
          >
            <h3 className="text-xl font-semibold mb-2">📚 Gerenciar Atividades</h3>
            <p className="text-sm opacity-80">Criar, editar e visualizar atividades</p>
          </button>
          
          <button
            onClick={() => navigate('/professor/alunos')}
            className="card hover:bg-senac-blue hover:text-white transition-all text-left"
          >
            <h3 className="text-xl font-semibold mb-2">👥 Gerenciar Alunos</h3>
            <p className="text-sm opacity-80">Adicionar e gerenciar alunos da turma</p>
          </button>
          
          <button
            onClick={() => navigate('/professor/relatorios')}
            className="card hover:bg-senac-blue hover:text-white transition-all text-left"
          >
            <h3 className="text-xl font-semibold mb-2">📊 Relatórios</h3>
            <p className="text-sm opacity-80">Visualizar desempenho e estatísticas</p>
          </button>
        </div>

        {/* Lista de Atividades */}
        <div className="card">
          <h2 className="text-2xl font-bold text-gray-800 mb-6">Atividades Recentes</h2>
          
          {atividades.length === 0 ? (
            <div className="text-center py-8">
              <p className="text-gray-600 mb-4">Nenhuma atividade criada ainda</p>
              <button
                onClick={() => navigate('/professor/atividades/nova')}
                className="btn-primary"
              >
                Criar primeira atividade
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              {atividades.slice(0, 5).map((atividade) => (
                <div
                  key={atividade.id}
                  className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
                >
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <h3 className="font-semibold text-lg text-gray-800">{atividade.titulo}</h3>
                      <p className="text-gray-600 text-sm mt-1">{atividade.descricao}</p>
                      <div className="flex gap-4 mt-2">
                        <span className="text-xs bg-senac-blue text-white px-2 py-1 rounded">
                          {atividade.tipo}
                        </span>
                        <span className="text-xs text-gray-600">
                          Prazo: {new Date(atividade.prazo).toLocaleDateString('pt-BR')}
                        </span>
                        <span className={`text-xs px-2 py-1 rounded ${atividade.ativo ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'}`}>
                          {atividade.ativo ? 'Ativa' : 'Inativa'}
                        </span>
                      </div>
                    </div>
                    <button
                      onClick={() => navigate(`/professor/atividades/${atividade.id}`)}
                      className="btn-secondary text-sm ml-4"
                    >
                      Gerenciar
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;

