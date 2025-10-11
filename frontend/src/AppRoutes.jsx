import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Layout from './components/Layout';
import ProtectedRoute from './components/ProtectedRoute';

// Importação das páginas
import Login from './pages/Login';
import Register from './pages/Register';
import DashboardAluno from './pages/DashboardAluno';
import DashboardProfessor from './pages/DashboardProfessor';
import AtividadesAluno from './pages/AtividadesAluno';
import AtividadesProfessor from './pages/AtividadesProfessor';
import GruposAluno from './pages/GruposAluno';
import GruposProfessor from './pages/GruposProfessor';
import FollowUpAluno from './pages/FollowUpAluno';
import FollowUpProfessor from './pages/FollowUpProfessor';
import Relatorios from './pages/Relatorios';
import Configuracoes from './pages/Configuracoes';
import NotFound from './pages/NotFound';

// Layout principal protegendo rotas autenticadas
const MainLayout = ({ children }) => (
  <Layout>{children}</Layout>
);

function AppRoutes() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />

          {/* Rotas protegidas para aluno */}
          <Route element={<ProtectedRoute allowedRoles={['aluno']} />}>
            <Route path="/dashboard" element={<MainLayout><DashboardAluno /></MainLayout>} />
            <Route path="/atividades" element={<MainLayout><AtividadesAluno /></MainLayout>} />
            <Route path="/grupos" element={<MainLayout><GruposAluno /></MainLayout>} />
            <Route path="/followup" element={<MainLayout><FollowUpAluno /></MainLayout>} />
            <Route path="/configuracoes" element={<MainLayout><Configuracoes /></MainLayout>} />
          </Route>

          {/* Rotas protegidas para professor */}
          <Route element={<ProtectedRoute allowedRoles={['professor']} />}>
            <Route path="/dashboard" element={<MainLayout><DashboardProfessor /></MainLayout>} />
            <Route path="/alunos" element={<MainLayout><GruposProfessor /></MainLayout>} />
            <Route path="/atividades-professor" element={<MainLayout><AtividadesProfessor /></MainLayout>} />
            <Route path="/grupos" element={<MainLayout><GruposProfessor /></MainLayout>} />
            <Route path="/followup-professor" element={<MainLayout><FollowUpProfessor /></MainLayout>} />
            <Route path="/relatorios" element={<MainLayout><Relatorios /></MainLayout>} />
            <Route path="/configuracoes" element={<MainLayout><Configuracoes /></MainLayout>} />
          </Route>

          {/* Rota fallback */}
          <Route path="*" element={<NotFound />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default AppRoutes;