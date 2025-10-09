import React, { useState } from 'react';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/Layout';
import Login from './components/Login';
import Loading from './components/Loading';

// Importar páginas (serão criadas nas próximas fases)
import DashboardAluno from './pages/DashboardAluno';
import DashboardProfessor from './pages/DashboardProfessor';
import AtividadesAluno from './pages/AtividadesAluno';
import AtividadesProfessor from './pages/AtividadesProfessor';
import GruposAluno from './pages/GruposAluno';
import GruposProfessor from './pages/GruposProfessor';
import AlunosProfessor from './pages/AlunosProfessor';
import RelatoriosProfessor from './pages/RelatoriosProfessor';

import './App.css';

const AppContent = () => {
  const { user, loading } = useAuth();
  const [currentPage, setCurrentPage] = useState('dashboard');

  if (loading) {
    return <Loading />;
  }

  if (!user) {
    return <Login />;
  }

  const renderPage = () => {
    if (user.tipo === 'professor') {
      switch (currentPage) {
        case 'dashboard':
          return <DashboardProfessor />;
        case 'alunos':
          return <AlunosProfessor />;
        case 'atividades':
          return <AtividadesProfessor />;
        case 'grupos':
          return <GruposProfessor />;
        case 'relatorios':
          return <RelatoriosProfessor />;
        default:
          return <DashboardProfessor />;
      }
    } else {
      switch (currentPage) {
        case 'dashboard':
          return <DashboardAluno />;
        case 'atividades':
          return <AtividadesAluno />;
        case 'grupos':
          return <GruposAluno />;
        default:
          return <DashboardAluno />;
      }
    }
  };

  return (
    <Layout currentPage={currentPage} onNavigate={setCurrentPage}>
      {renderPage()}
    </Layout>
  );
};

function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}

export default App;
