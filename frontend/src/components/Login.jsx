import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { BookOpen, User, Mail, Lock, GraduationCap } from 'lucide-react';

const Login = () => {
  const { login, register } = useAuth();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Estados para login
  const [loginData, setLoginData] = useState({
    email: '',
    senha: '',
    tipoUsuario: 'aluno'
  });

  // Estados para registro
  const [registerData, setRegisterData] = useState({
    nome: '',
    email: '',
    turma: '',
    senha: ''
  });

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    const result = await login(loginData.email, loginData.senha, loginData.tipoUsuario);
    
    if (!result.success) {
      setError(result.error);
    }
    
    setLoading(false);
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');

    const result = await register(
      registerData.nome,
      registerData.email,
      registerData.turma,
      registerData.senha
    );
    
    if (result.success) {
      setSuccess('Cadastro realizado com sucesso! Faça login para continuar.');
      setRegisterData({ nome: '', email: '', turma: '', senha: '' });
    } else {
      setError(result.error);
    }
    
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center mb-4">
            <BookOpen className="h-12 w-12 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900">AtivFlow</h1>
          <p className="text-gray-600 mt-2">Sistema de Gestão de Entregas de Atividades</p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Bem-vindo ao AtivFlow</CardTitle>
            <CardDescription>
              Faça login ou cadastre-se para acessar o sistema
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="login">Login</TabsTrigger>
                <TabsTrigger value="register">Cadastro</TabsTrigger>
              </TabsList>

              {/* Tab de Login */}
              <TabsContent value="login">
                <form onSubmit={handleLogin} className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Tipo de Usuário</label>
                    <div className="flex space-x-2">
                      <Button
                        type="button"
                        variant={loginData.tipoUsuario === 'aluno' ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setLoginData({ ...loginData, tipoUsuario: 'aluno' })}
                        className="flex-1"
                      >
                        <User className="h-4 w-4 mr-2" />
                        Aluno
                      </Button>
                      <Button
                        type="button"
                        variant={loginData.tipoUsuario === 'professor' ? 'default' : 'outline'}
                        size="sm"
                        onClick={() => setLoginData({ ...loginData, tipoUsuario: 'professor' })}
                        className="flex-1"
                      >
                        <GraduationCap className="h-4 w-4 mr-2" />
                        Professor
                      </Button>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium">Email</label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        type="email"
                        placeholder="seu@email.com"
                        value={loginData.email}
                        onChange={(e) => setLoginData({ ...loginData, email: e.target.value })}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium">Senha</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        type="password"
                        placeholder="Sua senha"
                        value={loginData.senha}
                        onChange={(e) => setLoginData({ ...loginData, senha: e.target.value })}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>

                  {error && (
                    <Alert variant="destructive">
                      <AlertDescription>{error}</AlertDescription>
                    </Alert>
                  )}

                  <Button type="submit" className="w-full" disabled={loading}>
                    {loading ? 'Entrando...' : 'Entrar'}
                  </Button>
                </form>

                {/* Credenciais de teste */}
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-xs text-blue-700 font-medium mb-2">Credenciais de teste:</p>
                  <p className="text-xs text-blue-600">
                    <strong>Professor:</strong> professor@senac.com / 123456
                  </p>
                </div>
              </TabsContent>

              {/* Tab de Cadastro */}
              <TabsContent value="register">
                <form onSubmit={handleRegister} className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">Nome Completo</label>
                    <div className="relative">
                      <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        type="text"
                        placeholder="Seu nome completo"
                        value={registerData.nome}
                        onChange={(e) => setRegisterData({ ...registerData, nome: e.target.value })}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium">Email</label>
                    <div className="relative">
                      <Mail className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        type="email"
                        placeholder="seu@email.com"
                        value={registerData.email}
                        onChange={(e) => setRegisterData({ ...registerData, email: e.target.value })}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium">Turma</label>
                    <Input
                      type="text"
                      placeholder="Ex: 321530"
                      value={registerData.turma}
                      onChange={(e) => setRegisterData({ ...registerData, turma: e.target.value })}
                      required
                    />
                  </div>

                  <div className="space-y-2">
                    <label className="text-sm font-medium">Senha</label>
                    <div className="relative">
                      <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                      <Input
                        type="password"
                        placeholder="Crie uma senha"
                        value={registerData.senha}
                        onChange={(e) => setRegisterData({ ...registerData, senha: e.target.value })}
                        className="pl-10"
                        required
                      />
                    </div>
                  </div>

                  {error && (
                    <Alert variant="destructive">
                      <AlertDescription>{error}</AlertDescription>
                    </Alert>
                  )}

                  {success && (
                    <Alert>
                      <AlertDescription className="text-green-700">{success}</AlertDescription>
                    </Alert>
                  )}

                  <Button type="submit" className="w-full" disabled={loading}>
                    {loading ? 'Cadastrando...' : 'Cadastrar'}
                  </Button>
                </form>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card>

        {/* Footer */}
        <div className="text-center mt-8">
          <p className="text-sm text-gray-500 font-semibold">
            321530 – A melhor Turma de ADM do SENAC 📚
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;
