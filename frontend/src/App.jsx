/**
 * Componente principal da aplicação
 * Define rotas e estrutura geral
 */
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/common/ProtectedRoute';

// Páginas
import Login from './pages/auth/Login';
import AlunoDashboard from './pages/aluno/Dashboard';
import ProfessorDashboard from './pages/professor/Dashboard';

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          {/* Rota pública */}
          <Route path="/login" element={<Login />} />
          
          {/* Rotas do aluno */}
          <Route
            path="/aluno/dashboard"
            element={
              <ProtectedRoute requiredType="aluno">
                <AlunoDashboard />
              </ProtectedRoute>
            }
          />
          
          {/* Rotas do professor */}
          <Route
            path="/professor/dashboard"
            element={
              <ProtectedRoute requiredType="professor">
                <ProfessorDashboard />
              </ProtectedRoute>
            }
          />
          
          {/* Rota padrão */}
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;

