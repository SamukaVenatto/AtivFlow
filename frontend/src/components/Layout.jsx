import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';
import { BookOpen, Users, BarChart3, Settings, LogOut, User, Home, ClipboardCheck } from 'lucide-react';

const Layout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate("/login");
  };

  // Menus dinâmicos por tipo de usuário
  const menuItems = user?.tipo_usuario === 'professor' ? [
    { id: 'dashboard', label: 'Painel', icon: Home, path: '/dashboard' },
    { id: 'alunos', label: 'Alunos', icon: Users, path: '/alunos' },
    { id: 'atividades', label: 'Atividades', icon: BookOpen, path: '/atividades-professor' },
    { id: 'grupos', label: 'Grupos', icon: Users, path: '/grupos' },
    { id: 'followup-professor', label: 'Follow-up', icon: ClipboardCheck, path: '/followup-professor' },
    { id: 'relatorios', label: 'Relatórios', icon: BarChart3, path: '/relatorios' },
    { id: 'configuracoes', label: 'Configurações', icon: Settings, path: '/configuracoes' }
  ] : [
    { id: 'dashboard', label: 'Meu Painel', icon: Home, path: '/dashboard' },
    { id: 'atividades', label: 'Atividades', icon: BookOpen, path: '/atividades' },
    { id: 'grupos', label: 'Meus Grupos', icon: Users, path: '/grupos' },
    { id: 'followup', label: 'Follow-up', icon: ClipboardCheck, path: '/followup' },
    { id: 'configuracoes', label: 'Configurações', icon: Settings, path: '/configuracoes' }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-blue-600">AtivFlow</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-gray-500" />
                <span className="text-sm font-medium text-gray-700">Olá, {user?.nome}!</span>
              </div>
              <button
                onClick={handleLogout}
                className="flex items-center space-x-2 bg-gray-100 hover:bg-gray-200 px-3 py-2 rounded"
              >
                <LogOut className="h-4 w-4" />
                <span>Sair</span>
              </button>
            </div>
          </div>
        </div>
      </header>
      <div className="flex">
        <nav className="w-64 bg-white shadow-sm min-h-screen">
          <div className="p-4 space-y-2">
            {menuItems.map((item) => {
              const Icon = item.icon;
              const isActive = location.pathname === item.path;
              return (
                <button
                  key={item.id}
                  onClick={() => navigate(item.path)}
                  className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                    isActive
                      ? 'bg-blue-50 text-blue-700 border-r-2 border-blue-700'
                      : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <Icon className="h-5 w-5" />
                  <span className="font-medium">{item.label}</span>
                </button>
              );
            })}
          </div>
        </nav>
        <main className="flex-1 p-6">{children}</main>
      </div>
      <footer className="bg-white border-t mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="text-center text-sm text-gray-500">
            <p className="font-semibold text-blue-600">
              321530 – A melhor Turma de ADM do SENAC 📚
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;