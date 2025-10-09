import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { 
  BookOpen, 
  Users, 
  BarChart3, 
  Settings, 
  LogOut,
  User,
  Home
} from 'lucide-react';

const Layout = ({ children, currentPage, onNavigate }) => {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
  };

  const menuItems = user?.tipo === 'professor' ? [
    { id: 'dashboard', label: 'Dashboard', icon: Home },
    { id: 'alunos', label: 'Alunos', icon: Users },
    { id: 'atividades', label: 'Atividades', icon: BookOpen },
    { id: 'grupos', label: 'Grupos', icon: Users },
    { id: 'relatorios', label: 'Relatórios', icon: BarChart3 },
  ] : [
    { id: 'dashboard', label: 'Meu Painel', icon: Home },
    { id: 'atividades', label: 'Atividades', icon: BookOpen },
    { id: 'grupos', label: 'Meus Grupos', icon: Users },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <h1 className="text-2xl font-bold text-blue-600">AtivFlow</h1>
              </div>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-gray-500" />
                <span className="text-sm font-medium text-gray-700">
                  Olá, {user?.nome}! 👋
                </span>
              </div>
              <Button
                variant="outline"
                size="sm"
                onClick={handleLogout}
                className="flex items-center space-x-2"
              >
                <LogOut className="h-4 w-4" />
                <span>Sair</span>
              </Button>
            </div>
          </div>
        </div>
      </header>

      <div className="flex">
        {/* Sidebar */}
        <nav className="w-64 bg-white shadow-sm min-h-screen">
          <div className="p-4">
            <div className="space-y-2">
              {menuItems.map((item) => {
                const Icon = item.icon;
                return (
                  <button
                    key={item.id}
                    onClick={() => onNavigate(item.id)}
                    className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors ${
                      currentPage === item.id
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
          </div>
        </nav>

        {/* Main Content */}
        <main className="flex-1 p-6">
          {children}
        </main>
      </div>

      {/* Footer */}
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
