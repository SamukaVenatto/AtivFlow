import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/Layout';

// Páginas de autenticação
import Login from './pages/Login';

// Páginas do aluno
import DashboardAluno from './pages/DashboardAluno';
import AtividadesAluno from './pages/AtividadesAluno';
import EntregasAluno from './pages/EntregasAluno';
import FollowUpAluno from './pages/FollowUpAluno';

// Páginas do professor
import DashboardProfessor from './pages/DashboardProfessor';
import AlunosProfessor from './pages/AlunosProfessor';
import AtividadesProfessor from './pages/AtividadesProfessor';
import EntregasProfessor from './pages/EntregasProfessor';
import FollowUpProfessor from './pages/FollowUpProfessor';
import RelatoriosProfessor from './pages/RelatoriosProfessor';

// Páginas compartilhadas
import Notificacoes from './pages/Notificacoes';
import Configuracoes from './pages/Configuracoes';

// Componente de rota protegida
const ProtectedRoute = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.tipo_usuario)) {
    return <Navigate to="/dashboard" replace />;
  }

  return children;
};

// Layout principal usando Layout.jsx
const MainLayout = ({ children }) => {
  return (
    <Layout>
      {children}
    </Layout>
  );
};

// Componente principal da aplicação
const AppContent = () => {
  const { user } = useAuth();

  return (
    <Routes>
      {/* Rota de login */}
      <Route 
        path="/login" 
        element={
          user ? <Navigate to="/dashboard" replace /> : <Login />
        } 
      />

      {/* Rotas protegidas */}
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute>
            <MainLayout>
              {user?.tipo_usuario === 'aluno' ? <DashboardAluno /> : <DashboardProfessor />}
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* Rotas do aluno */}
      <Route
        path="/atividades"
        element={
          <ProtectedRoute allowedRoles={['aluno']}>
            <MainLayout>
              <AtividadesAluno />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/entregas"
        element={
          <ProtectedRoute allowedRoles={['aluno']}>
            <MainLayout>
              <EntregasAluno />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/followup"
        element={
          <ProtectedRoute allowedRoles={['aluno']}>
            <MainLayout>
              <FollowUpAluno />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* Rotas do professor */}
      <Route
        path="/alunos"
        element={
          <ProtectedRoute allowedRoles={['professor']}>
            <MainLayout>
              <AlunosProfessor />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/atividades-professor"
        element={
          <ProtectedRoute allowedRoles={['professor']}>
            <MainLayout>
              <AtividadesProfessor />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/entregas-professor"
        element={
          <ProtectedRoute allowedRoles={['professor']}>
            <MainLayout>
              <EntregasProfessor />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/followup-professor"
        element={
          <ProtectedRoute allowedRoles={['professor']}>
            <MainLayout>
              <FollowUpProfessor />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/relatorios"
        element={
          <ProtectedRoute allowedRoles={['professor']}>
            <MainLayout>
              <RelatoriosProfessor />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* Rotas compartilhadas */}
      <Route
        path="/notificacoes"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Notificacoes />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      <Route
        path="/configuracoes"
        element={
          <ProtectedRoute>
            <MainLayout>
              <Configuracoes />
            </MainLayout>
          </ProtectedRoute>
        }
      />

      {/* Rota padrão */}
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      
      {/* Rota 404 */}
      <Route 
        path="*" 
        element={
          <ProtectedRoute>
            <MainLayout>
              <div className="flex flex-col items-center justify-center h-full">
                <h1 className="text-4xl font-bold text-gray-800 mb-4">404</h1>
                <p className="text-gray-600 mb-8">Página não encontrada</p>
                <button
                  onClick={() => window.history.back()}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg transition-colors"
                >
                  Voltar
                </button>
              </div>
            </MainLayout>
          </ProtectedRoute>
        } 
      />
    </Routes>
  );
};

// Componente raiz
const AppRoutes = () => {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
};

export default AppRoutes;