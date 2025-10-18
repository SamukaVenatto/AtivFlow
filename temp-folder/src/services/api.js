/**
 * Configuração do Axios para comunicação com o backend
 * Inclui interceptors para renovação de sessão e tratamento de erros globais
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true, // Importante para enviar cookies de sessão
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor de resposta para tratamento de erros
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Erro de resposta do servidor
      const { status, data } = error.response;
      
      if (status === 401) {
        // Não autenticado - redirecionar para login
        window.location.href = '/login';
      } else if (status === 403) {
        // Sem permissão
        console.error('Acesso negado:', data.error);
      } else if (status === 500) {
        // Erro interno do servidor
        console.error('Erro no servidor:', data.error);
      }
    } else if (error.request) {
      // Requisição feita mas sem resposta
      console.error('Erro de rede:', error.message);
    } else {
      // Erro na configuração da requisição
      console.error('Erro:', error.message);
    }
    
    return Promise.reject(error);
  }
);

export default api;

