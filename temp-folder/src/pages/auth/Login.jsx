/**
 * Página de Login
 * Seleção de tipo (Aluno/Professor) e autenticação
 */
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';

const Login = () => {
  const [tipoSelecionado, setTipoSelecionado] = useState(null);
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErro('');
    setLoading(true);

    // Validação client-side
    if (!email || !senha) {
      setErro('Por favor, preencha todos os campos');
      setLoading(false);
      return;
    }

    const result = await login(email, senha);
    
    if (result.success) {
      // Redirecionar baseado no tipo de usuário
      if (result.user.tipo === 'aluno') {
        navigate('/aluno/dashboard');
      } else if (result.user.tipo === 'professor' || result.user.tipo === 'admin') {
        navigate('/professor/dashboard');
      }
    } else {
      setErro(result.error);
    }
    
    setLoading(false);
  };

  if (!tipoSelecionado) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-senac-blue to-senac-blue-light flex items-center justify-center p-4">
        <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-senac-blue mb-2">AtivFlow</h1>
            <p className="text-gray-600">Sistema de Gerenciamento de Atividades</p>
          </div>
          
          <h2 className="text-2xl font-semibold text-center mb-6 text-gray-800">
            Selecione seu perfil
          </h2>
          
          <div className="space-y-4">
            <button
              onClick={() => setTipoSelecionado('aluno')}
              className="w-full py-4 px-6 bg-senac-blue hover:bg-senac-blue-dark text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-md"
            >
              Sou Aluno
            </button>
            
            <button
              onClick={() => setTipoSelecionado('professor')}
              className="w-full py-4 px-6 bg-senac-blue-light hover:bg-senac-blue text-white font-semibold rounded-lg transition-all duration-200 transform hover:scale-105 shadow-md"
            >
              Sou Professor
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-senac-blue to-senac-blue-light flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-2xl p-8 max-w-md w-full">
        <button
          onClick={() => setTipoSelecionado(null)}
          className="text-senac-blue hover:text-senac-blue-dark mb-4 flex items-center"
        >
          ← Voltar
        </button>
        
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-senac-blue mb-2">AtivFlow</h1>
          <p className="text-gray-600">
            Login como {tipoSelecionado === 'aluno' ? 'Aluno' : 'Professor'}
          </p>
        </div>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          {erro && (
            <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
              {erro}
            </div>
          )}
          
          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
              E-mail
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="input-field"
              placeholder={tipoSelecionado === 'aluno' ? 'nome.sobrenome@adm321530.com' : 'professor@senac.edu.br'}
              required
            />
          </div>
          
          <div>
            <label htmlFor="senha" className="block text-sm font-medium text-gray-700 mb-2">
              Senha
            </label>
            <input
              type="password"
              id="senha"
              value={senha}
              onChange={(e) => setSenha(e.target.value)}
              className="input-field"
              placeholder="••••••••"
              required
            />
          </div>
          
          <button
            type="submit"
            disabled={loading}
            className="w-full btn-primary py-3 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>
        
        <div className="mt-6 text-center text-sm text-gray-600">
          <p>Credenciais de teste:</p>
          <p className="mt-2">
            <strong>Professor:</strong> maria.santos@senac.edu.br / Prof@123
          </p>
          <p>
            <strong>Aluno:</strong> samuel.ribeiro@adm321530.com / Aluno@123
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;

