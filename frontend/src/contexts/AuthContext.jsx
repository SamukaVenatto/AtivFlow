// ... trecho relevante para garantir o tipo de usuário seja setado
const login = async (credentials) => {
  setLoading(true);
  setError(null);
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(credentials)
    });
    const data = await response.json();
    if (response.ok) {
      setUser({ ...data.user, tipo_usuario: data.user.tipo_usuario });
    } else {
      setError(data.error || 'Erro ao fazer login');
    }
  } catch (error) {
    setError('Erro de conexão');
  } finally {
    setLoading(false);
  }
};