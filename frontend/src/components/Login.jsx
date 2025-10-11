import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';

const Login = () => {
  const { login, loading, error } = useAuth();
  const [tipoUsuario, setTipoUsuario] = useState('aluno');
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [aba, setAba] = useState('login');

  const handleSubmit = async (e) => {
    e.preventDefault();
    await login({ tipo_usuario: tipoUsuario, email, senha });
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-blue-50">
      <div className="mb-8 flex flex-col items-center">
        <div className="text-5xl text-blue-700 mb-2">
          <span role="img" aria-label="logo">📘</span>
        </div>
        <h1 className="text-3xl font-bold">AtivFlow</h1>
        <p className="text-lg text-gray-600 mt-1">Sistema de Gestão de Entregas de Atividades</p>
      </div>
      <div className="bg-white rounded-xl shadow-lg p-8 w-full max-w-md">
        <h2 className="text-xl font-semibold mb-4">Bem-vindo ao AtivFlow</h2>
        <p className="mb-6 text-gray-500">Faça login ou cadastre-se para acessar o sistema</p>
        <div className="flex mb-6">
          <button
            className={`flex-1 py-2 rounded-l-lg border ${aba === 'login' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600'}`}
            onClick={() => setAba('login')}
          >
            Conecte-se
          </button>
          <button
            className={`flex-1 py-2 rounded-r-lg border-l-0 border ${aba === 'cadastro' ? 'bg-blue-600 text-white' : 'bg-gray-100 text-gray-600'}`}
            onClick={() => setAba('cadastro')}
          >
            Cadastro
          </button>
        </div>
        <form onSubmit={handleSubmit}>
          <div className="mb-4 flex gap-2">
            <button
              type="button"
              className={`flex-1 py-2 rounded-l-lg border ${tipoUsuario === 'aluno' ? 'bg-black text-white' : 'bg-gray-100 text-gray-600'}`}
              onClick={() => setTipoUsuario('aluno')}
            >
              Aluno
            </button>
            <button
              type="button"
              className={`flex-1 py-2 rounded-r-lg border-l-0 border ${tipoUsuario === 'professor' ? 'bg-black text-white' : 'bg-gray-100 text-gray-600'}`}
              onClick={() => setTipoUsuario('professor')}
            >
              Professor
            </button>
          </div>
          <div className="mb-4">
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              placeholder="seu@email.com"
              className="w-full px-4 py-2 border rounded-lg"
              required
              autoComplete="username"
            />
          </div>
          <div className="mb-6">
            <input
              type="password"
              value={senha}
              onChange={e => setSenha(e.target.value)}
              placeholder="Sua senha"
              className="w-full px-4 py-2 border rounded-lg"
              required
              autoComplete="current-password"
            />
          </div>
          {error && <div className="mb-4 text-red-600 text-center">{error}</div>}
          <button
            type="submit"
            className="w-full py-2 rounded-lg bg-black text-white font-semibold flex items-center justify-center"
            disabled={loading}
          >
            {loading ? 'Entrando...' : 'Entrar'}
          </button>
        </form>

        {/* Removido o bloco das credenciais de teste */}
      </div>
      <div className="mt-8 text-gray-400 text-xs">
        321530 &ndash; A melhor Turma de ADM do SENAC <span role="img" aria-label="livro">📚</span>
      </div>
    </div>
  );
};

export default Login;
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
