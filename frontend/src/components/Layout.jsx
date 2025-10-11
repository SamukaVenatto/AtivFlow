import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate, useLocation } from 'react-router-dom';
import { BookOpen, Users, BarChart3, Settings, LogOut, User, Home, ClipboardCheck } from 'lucide-react';

const Layout = ({ children }) => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  // Menu lateral por perfil
  const menuItems = user?.tipo_usuario === 'professor'
    ? [
        { id: 'dashboard', label: 'Painel', icon: Home, path: '/dashboard' },
        { id: 'alunos', label: 'Alunos', icon: Users, path: '/alunos' },
        { id: 'atividades', label: 'Atividades', icon: BookOpen, path: '/atividades-professor' },
        { id: 'grupos', label: 'Grupos', icon: User, path: '/grupos' },
        { id: 'followup-professor', label: 'Acompanhamento', icon: ClipboardCheck, path: '/followup-professor' },
        { id: 'relatorios', label: 'Relatórios', icon: BarChart3, path: '/relatorios' },
        { id: 'configuracoes', label: 'Configurações', icon: Settings, path: '/configuracoes' }
      ]
    : [
        { id: 'dashboard', label: 'Meu Painel', icon: Home, path: '/dashboard' },
        { id: 'atividades', label: 'Atividades', icon: BookOpen, path: '/atividades' },
        { id: 'grupos', label: 'Meus Grupos', icon: User, path: '/grupos' },
        { id: 'followup', label: 'Acompanhamento', icon: ClipboardCheck, path: '/followup' },
        { id: 'configuracoes', label: 'Configurações', icon: Settings, path: '/configuracoes' }
      ];

  return (
    <div className="flex h-screen">
      <aside className="w-64 bg-white border-r flex flex-col">
        <div className="flex items-center h-16 px-6 font-bold text-xl border-b">AtivFlow</div>
        <nav className="flex-1 px-4 py-6 space-y-1">
          {menuItems.map(item => (
            <button
              key={item.id}
              onClick={() => navigate(item.path)}
              className={`w-full flex items-center px-4 py-2 rounded-lg text-left transition ${
                location.pathname === item.path
                  ? 'bg-blue-100 text-blue-700 font-semibold'
                  : 'hover:bg-gray-100 text-gray-700'
              }`}
              data-testid={`menu-${item.id}`}
            >
              <item.icon size={20} className="mr-3" />
              {item.label}
            </button>
          ))}
        </nav>
        <button
          onClick={logout}
          className="m-4 px-4 py-2 rounded-lg bg-red-100 text-red-600 flex items-center justify-center gap-2"
        >
          <LogOut size={18} /> Sair
        </button>
      </aside>
      <main className="flex-1 bg-gray-50 overflow-y-auto">{children}</main>
    </div>
  );
};

export default Layout;