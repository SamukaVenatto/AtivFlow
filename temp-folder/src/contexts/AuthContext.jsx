/**
 * Contexto de Autenticação
 * Gerencia estado de autenticação e informações do usuário
 */
import { createContext, useContext, useState, useEffect } from 'react';
import api from '../services/api';

const AuthContext = createContext(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [authenticated, setAuthenticated] = useState(false);

  // Verificar autenticação ao carregar
  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    try {
      const response = await api.get('/auth/check');
      if (response.data.authenticated) {
        setUser(response.data.user);
        setAuthenticated(true);
      }
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error);
    } finally {
      setLoading(false);
    }
  };

  const login = async (email, senha) => {
    try {
      const response = await api.post('/auth/login', { email, senha });
      if (response.data.ok) {
        setUser(response.data.user);
        setAuthenticated(true);
        return { success: true, user: response.data.user };
      }
    } catch (error) {
      return {
        success: false,
        error: error.response?.data?.error || 'Erro ao fazer login'
      };
    }
  };

  const logout = async () => {
    try {
      await api.post('/auth/logout');
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    } finally {
      setUser(null);
      setAuthenticated(false);
    }
  };

  const value = {
    user,
    authenticated,
    loading,
    login,
    logout,
    checkAuth
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

