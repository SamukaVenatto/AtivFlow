import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { 
  Home, 
  Users, 
  BookOpen, 
  FileText, 
  UserCheck, 
  BarChart3, 
  Settings,
  ClipboardList,
  MessageSquare,
  Bell
} from 'lucide-react';

const Navigation = ({ userType }) => {
  const location = useLocation();

  const isActive = (path) => {
    return location.pathname === path;
  };

  const menuItems = {
    aluno: [
      { path: '/dashboard', icon: Home, label: 'Dashboard' },
      { path: '/atividades', icon: BookOpen, label: 'Atividades' },
      { path: '/entregas', icon: FileText, label: 'Entregas' },
      { path: '/followup', icon: ClipboardList, label: 'Follow-up' },
      { path: '/notificacoes', icon: Bell, label: 'Notificações' },
      { path: '/configuracoes', icon: Settings, label: 'Configurações' }
    ],
    professor: [
      { path: '/dashboard', icon: Home, label: 'Dashboard' },
      { path: '/alunos', icon: Users, label: 'Alunos' },
      { path: '/atividades', icon: BookOpen, label: 'Atividades' },
      { path: '/entregas', icon: FileText, label: 'Entregas' },
      { path: '/followup-professor', icon: UserCheck, label: 'Follow-up' },
      { path: '/relatorios', icon: BarChart3, label: 'Relatórios' },
      { path: '/notificacoes', icon: Bell, label: 'Notificações' },
      { path: '/configuracoes', icon: Settings, label: 'Configurações' }
    ]
  };

  const items = menuItems[userType] || [];

  return (
    <nav className="bg-white shadow-sm border-r border-gray-200 w-64 min-h-screen">
      <div className="p-6">
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
            <BookOpen className="text-white" size={24} />
          </div>
          <div>
            <h1 className="text-xl font-bold text-gray-800">AtivFlow</h1>
            <p className="text-sm text-gray-500 capitalize">{userType}</p>
          </div>
        </div>

        <ul className="space-y-2">
          {items.map((item) => {
            const Icon = item.icon;
            return (
              <li key={item.path}>
                <Link
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive(item.path)
                      ? 'bg-blue-50 text-blue-600 border-r-2 border-blue-600'
                      : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
                  }`}
                >
                  <Icon size={20} />
                  <span className="font-medium">{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </div>
    </nav>
  );
};

export default Navigation;
