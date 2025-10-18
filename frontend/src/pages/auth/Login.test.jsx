import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BrowserRouter } from 'react-router-dom';
import { AuthProvider } from '../../contexts/AuthContext';
import Login from './Login';
import api from '../../services/api';

// Mock do módulo api para controlar o comportamento das chamadas HTTP
jest.mock('../../services/api');

describe('Login Component', () => {
  beforeEach(() => {
    // Limpar mocks antes de cada teste
    api.post.mockClear();
  });

  test('renderiza a seleção de perfil inicialmente', () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    );
    expect(screen.getByText(/Selecione seu perfil/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sou Aluno/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Sou Professor/i })).toBeInTheDocument();
  });

  test('muda para o formulário de login ao selecionar perfil', () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    );
    fireEvent.click(screen.getByRole('button', { name: /Sou Aluno/i }));
    expect(screen.getByText(/Login como Aluno/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/E-mail/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Senha/i)).toBeInTheDocument();
  });

  test('exibe mensagem de erro para campos vazios', async () => {
    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    );
    fireEvent.click(screen.getByRole('button', { name: /Sou Aluno/i }));
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));

    await waitFor(() => {
      expect(screen.getByText(/Por favor, preencha todos os campos/i)).toBeInTheDocument();
    });
  });

  test('exibe mensagem de erro para credenciais inválidas', async () => {
    api.post.mockResolvedValueOnce({
      data: { ok: false, error: 'Credenciais inválidas' },
      status: 401,
    });

    render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    );
    fireEvent.click(screen.getByRole('button', { name: /Sou Aluno/i }));

    fireEvent.change(screen.getByLabelText(/E-mail/i), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByLabelText(/Senha/i), { target: { value: 'wrongpassword' } });
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));

    await waitFor(() => {
      expect(screen.getByText(/Credenciais inválidas/i)).toBeInTheDocument();
    });
  });

  test('redireciona para o dashboard do aluno em login bem-sucedido', async () => {
    api.post.mockResolvedValueOnce({
      data: { ok: true, user: { id: 1, nome_completo: 'Aluno Teste', tipo: 'aluno', turma: '321530' } },
      status: 200,
    });

    const { container } = render(
      <BrowserRouter>
        <AuthProvider>
          <Login />
        </AuthProvider>
      </BrowserRouter>
    );
    fireEvent.click(screen.getByRole('button', { name: /Sou Aluno/i }));

    fireEvent.change(screen.getByLabelText(/E-mail/i), { target: { value: 'aluno@test.com' } });
    fireEvent.change(screen.getByLabelText(/Senha/i), { target: { value: 'Aluno@123' } });
    fireEvent.click(screen.getByRole('button', { name: /Entrar/i }));

    await waitFor(() => {
      expect(container.innerHTML).not.toContain('Login como Aluno'); // Verifica que a página de login não está mais visível
    });
    // Em um ambiente de teste real, você verificaria a navegação usando `window.location.pathname` ou mocks do `useNavigate`
    // Para este exemplo, a ausência do formulário de login é um bom indicativo.
  });
});

