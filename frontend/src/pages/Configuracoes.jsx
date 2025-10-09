import React, { useState, useEffect } from 'react';
import { Settings, Lock, User, Save, Eye, EyeOff } from 'lucide-react';

const Configuracoes = () => {
  const [activeTab, setActiveTab] = useState('perfil');
  const [perfil, setPerfil] = useState({});
  const [loading, setLoading] = useState(true);
  const [showPassword, setShowPassword] = useState({
    atual: false,
    nova: false,
    confirmar: false
  });
  
  const [senhaForm, setSenhaForm] = useState({
    senha_atual: '',
    nova_senha: '',
    confirmar_senha: ''
  });

  const [perfilForm, setPerfilForm] = useState({
    nome: ''
  });

  useEffect(() => {
    carregarPerfil();
  }, []);

  const carregarPerfil = async () => {
    try {
      const response = await fetch('/api/configuracoes/perfil');
      if (response.ok) {
        const data = await response.json();
        setPerfil(data.perfil);
        setPerfilForm({
          nome: data.perfil.nome || ''
        });
      }
    } catch (error) {
      console.error('Erro ao carregar perfil:', error);
    } finally {
      setLoading(false);
    }
  };

  const alterarSenha = async (e) => {
    e.preventDefault();
    
    if (senhaForm.nova_senha !== senhaForm.confirmar_senha) {
      alert('Nova senha e confirmação não coincidem');
      return;
    }

    if (senhaForm.nova_senha.length < 6) {
      alert('Nova senha deve ter pelo menos 6 caracteres');
      return;
    }

    try {
      const response = await fetch('/api/configuracoes/alterar-senha', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(senhaForm)
      });

      const data = await response.json();

      if (response.ok) {
        alert('Senha alterada com sucesso!');
        setSenhaForm({
          senha_atual: '',
          nova_senha: '',
          confirmar_senha: ''
        });
      } else {
        alert('Erro: ' + (data.error || 'Erro ao alterar senha'));
      }
    } catch (error) {
      console.error('Erro ao alterar senha:', error);
      alert('Erro ao alterar senha');
    }
  };

  const atualizarPerfil = async (e) => {
    e.preventDefault();
    
    try {
      const response = await fetch('/api/configuracoes/atualizar-perfil', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(perfilForm)
      });

      const data = await response.json();

      if (response.ok) {
        alert('Perfil atualizado com sucesso!');
        carregarPerfil();
      } else {
        alert('Erro: ' + (data.error || 'Erro ao atualizar perfil'));
      }
    } catch (error) {
      console.error('Erro ao atualizar perfil:', error);
      alert('Erro ao atualizar perfil');
    }
  };

  const togglePasswordVisibility = (field) => {
    setShowPassword(prev => ({
      ...prev,
      [field]: !prev[field]
    }));
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
      <div className="bg-gradient-to-r from-purple-600 to-purple-800 text-white p-6 rounded-lg mb-6">
        <div className="flex items-center gap-3">
          <Settings size={32} />
          <h1 className="text-2xl font-bold">Configurações</h1>
        </div>
      </div>

      {/* Tabs */}
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden">
        <div className="border-b border-gray-200">
          <nav className="flex">
            <button
              onClick={() => setActiveTab('perfil')}
              className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'perfil'
                  ? 'border-purple-500 text-purple-600 bg-purple-50'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center gap-2">
                <User size={18} />
                Perfil
              </div>
            </button>
            
            <button
              onClick={() => setActiveTab('senha')}
              className={`px-6 py-4 text-sm font-medium border-b-2 transition-colors ${
                activeTab === 'senha'
                  ? 'border-purple-500 text-purple-600 bg-purple-50'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              <div className="flex items-center gap-2">
                <Lock size={18} />
                Alterar Senha
              </div>
            </button>
          </nav>
        </div>

        <div className="p-6">
          {/* Tab Perfil */}
          {activeTab === 'perfil' && (
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Informações do Perfil
              </h2>

              {/* Informações Atuais */}
              <div className="bg-gray-50 p-4 rounded-lg mb-6">
                <h3 className="text-lg font-medium text-gray-800 mb-4">
                  Dados Atuais
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Nome
                    </label>
                    <div className="text-gray-900 font-medium">
                      {perfil.nome}
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Email
                    </label>
                    <div className="text-gray-900">
                      {perfil.email}
                    </div>
                  </div>

                  {perfil.turma && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Turma
                      </label>
                      <div className="text-gray-900">
                        {perfil.turma}
                      </div>
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Tipo de Usuário
                    </label>
                    <div className="text-gray-900 capitalize">
                      {perfil.tipo_usuario}
                    </div>
                  </div>

                  {perfil.status && (
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Status
                      </label>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                        perfil.status === 'ativo' 
                          ? 'bg-green-100 text-green-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {perfil.status}
                      </span>
                    </div>
                  )}

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Membro desde
                    </label>
                    <div className="text-gray-900">
                      {perfil.created_at ? new Date(perfil.created_at).toLocaleDateString('pt-BR') : 'N/A'}
                    </div>
                  </div>
                </div>
              </div>

              {/* Formulário de Edição */}
              <form onSubmit={atualizarPerfil}>
                <h3 className="text-lg font-medium text-gray-800 mb-4">
                  Editar Informações
                </h3>
                
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nome
                    </label>
                    <input
                      type="text"
                      value={perfilForm.nome}
                      onChange={(e) => setPerfilForm({...perfilForm, nome: e.target.value})}
                      className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                      required
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Email (não editável)
                    </label>
                    <input
                      type="email"
                      value={perfil.email}
                      disabled
                      className="w-full p-3 border border-gray-300 rounded-lg bg-gray-100 text-gray-500"
                    />
                  </div>
                </div>

                <button
                  type="submit"
                  className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors"
                >
                  <Save size={18} />
                  Salvar Alterações
                </button>
              </form>
            </div>
          )}

          {/* Tab Senha */}
          {activeTab === 'senha' && (
            <div>
              <h2 className="text-xl font-semibold text-gray-800 mb-6">
                Alterar Senha
              </h2>

              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4 mb-6">
                <div className="flex items-start gap-3">
                  <Lock className="text-yellow-600 mt-0.5" size={20} />
                  <div>
                    <h3 className="text-sm font-medium text-yellow-800">
                      Dicas de Segurança
                    </h3>
                    <ul className="text-sm text-yellow-700 mt-2 space-y-1">
                      <li>• Use pelo menos 6 caracteres</li>
                      <li>• Combine letras, números e símbolos</li>
                      <li>• Não use informações pessoais</li>
                      <li>• Não compartilhe sua senha</li>
                    </ul>
                  </div>
                </div>
              </div>

              <form onSubmit={alterarSenha} className="max-w-md">
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Senha Atual
                    </label>
                    <div className="relative">
                      <input
                        type={showPassword.atual ? 'text' : 'password'}
                        value={senhaForm.senha_atual}
                        onChange={(e) => setSenhaForm({...senhaForm, senha_atual: e.target.value})}
                        className="w-full p-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        required
                      />
                      <button
                        type="button"
                        onClick={() => togglePasswordVisibility('atual')}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      >
                        {showPassword.atual ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Nova Senha
                    </label>
                    <div className="relative">
                      <input
                        type={showPassword.nova ? 'text' : 'password'}
                        value={senhaForm.nova_senha}
                        onChange={(e) => setSenhaForm({...senhaForm, nova_senha: e.target.value})}
                        className="w-full p-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        required
                        minLength={6}
                      />
                      <button
                        type="button"
                        onClick={() => togglePasswordVisibility('nova')}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      >
                        {showPassword.nova ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Confirmar Nova Senha
                    </label>
                    <div className="relative">
                      <input
                        type={showPassword.confirmar ? 'text' : 'password'}
                        value={senhaForm.confirmar_senha}
                        onChange={(e) => setSenhaForm({...senhaForm, confirmar_senha: e.target.value})}
                        className="w-full p-3 pr-12 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                        required
                        minLength={6}
                      />
                      <button
                        type="button"
                        onClick={() => togglePasswordVisibility('confirmar')}
                        className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700"
                      >
                        {showPassword.confirmar ? <EyeOff size={18} /> : <Eye size={18} />}
                      </button>
                    </div>
                  </div>

                  {/* Indicador de força da senha */}
                  {senhaForm.nova_senha && (
                    <div>
                      <div className="text-sm text-gray-700 mb-2">Força da senha:</div>
                      <div className="flex gap-1">
                        {[1, 2, 3, 4].map((level) => {
                          let strength = 0;
                          if (senhaForm.nova_senha.length >= 6) strength++;
                          if (senhaForm.nova_senha.length >= 8) strength++;
                          if (/[A-Z]/.test(senhaForm.nova_senha)) strength++;
                          if (/[0-9]/.test(senhaForm.nova_senha)) strength++;
                          if (/[^A-Za-z0-9]/.test(senhaForm.nova_senha)) strength++;

                          return (
                            <div
                              key={level}
                              className={`h-2 w-full rounded ${
                                level <= strength
                                  ? strength <= 2
                                    ? 'bg-red-400'
                                    : strength <= 3
                                    ? 'bg-yellow-400'
                                    : 'bg-green-400'
                                  : 'bg-gray-200'
                              }`}
                            />
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>

                <button
                  type="submit"
                  className="mt-6 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-lg flex items-center gap-2 transition-colors"
                >
                  <Lock size={18} />
                  Alterar Senha
                </button>
              </form>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Configuracoes;
