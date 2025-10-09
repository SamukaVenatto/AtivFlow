import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { 
  Users, 
  Plus, 
  Edit, 
  Trash2, 
  Search,
  Mail,
  GraduationCap,
  CheckCircle,
  AlertTriangle,
  Eye,
  UserCheck,
  UserX
} from 'lucide-react';

const AlunosProfessor = () => {
  const [alunos, setAlunos] = useState([]);
  const [filteredAlunos, setFilteredAlunos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedAluno, setSelectedAluno] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isViewDialogOpen, setIsViewDialogOpen] = useState(false);
  const [alunoStats, setAlunoStats] = useState(null);

  // Estados do formulário
  const [formData, setFormData] = useState({
    nome: '',
    email: '',
    turma: '',
    senha: '123456',
    status: 'ativo'
  });

  useEffect(() => {
    fetchAlunos();
  }, []);

  useEffect(() => {
    // Filtrar alunos baseado no termo de busca
    const filtered = alunos.filter(aluno =>
      aluno.nome.toLowerCase().includes(searchTerm.toLowerCase()) ||
      aluno.email.toLowerCase().includes(searchTerm.toLowerCase()) ||
      aluno.turma.toLowerCase().includes(searchTerm.toLowerCase())
    );
    setFilteredAlunos(filtered);
  }, [alunos, searchTerm]);

  const fetchAlunos = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/alunos/');
      if (response.ok) {
        const data = await response.json();
        setAlunos(data);
      } else {
        setError('Erro ao carregar alunos');
      }
    } catch (error) {
      console.error('Erro ao carregar alunos:', error);
      setError('Erro ao carregar alunos');
    } finally {
      setLoading(false);
    }
  };

  const fetchAlunoStats = async (alunoId) => {
    try {
      const response = await fetch(`/api/dashboard/aluno/${alunoId}/stats`);
      if (response.ok) {
        const data = await response.json();
        setAlunoStats(data);
      }
    } catch (error) {
      console.error('Erro ao carregar estatísticas do aluno:', error);
    }
  };

  const handleOpenDialog = (aluno = null) => {
    if (aluno) {
      setSelectedAluno(aluno);
      setFormData({
        nome: aluno.nome,
        email: aluno.email,
        turma: aluno.turma,
        senha: '',
        status: aluno.status
      });
    } else {
      setSelectedAluno(null);
      setFormData({
        nome: '',
        email: '',
        turma: '',
        senha: '123456',
        status: 'ativo'
      });
    }
    setIsDialogOpen(true);
    setError('');
    setSuccess('');
  };

  const handleViewAluno = async (aluno) => {
    setSelectedAluno(aluno);
    await fetchAlunoStats(aluno.id);
    setIsViewDialogOpen(true);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const url = selectedAluno 
        ? `/api/alunos/${selectedAluno.id}`
        : '/api/alunos/';
      
      const method = selectedAluno ? 'PUT' : 'POST';
      
      // Se estiver editando e senha estiver vazia, não enviar senha
      const payload = { ...formData };
      if (selectedAluno && !payload.senha) {
        delete payload.senha;
      }

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(data.message);
        await fetchAlunos();
        setTimeout(() => {
          setIsDialogOpen(false);
          setSuccess('');
        }, 2000);
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError('Erro ao salvar aluno');
    }
  };

  const handleDelete = async (alunoId) => {
    if (!confirm('Tem certeza que deseja excluir este aluno?')) {
      return;
    }

    try {
      const response = await fetch(`/api/alunos/${alunoId}`, {
        method: 'DELETE',
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(data.message);
        await fetchAlunos();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError('Erro ao excluir aluno');
    }
  };

  const toggleStatus = async (aluno) => {
    try {
      const novoStatus = aluno.status === 'ativo' ? 'inativo' : 'ativo';
      
      const response = await fetch(`/api/alunos/${aluno.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ status: novoStatus }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(`Aluno ${novoStatus === 'ativo' ? 'ativado' : 'desativado'} com sucesso`);
        await fetchAlunos();
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError('Erro ao alterar status do aluno');
    }
  };

  const getStatusBadge = (status) => {
    return status === 'ativo' 
      ? <Badge className="bg-green-100 text-green-800">Ativo</Badge>
      : <Badge className="bg-red-100 text-red-800">Inativo</Badge>;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <div className="grid gap-4">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="bg-gray-200 rounded-lg h-20"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Gerenciar Alunos</h1>
          <p className="text-gray-600">
            Cadastre e gerencie os alunos da turma
          </p>
        </div>
        
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => handleOpenDialog()} className="flex items-center space-x-2">
              <Plus className="h-4 w-4" />
              <span>Novo Aluno</span>
            </Button>
          </DialogTrigger>
          
          <DialogContent className="sm:max-w-md">
            <DialogHeader>
              <DialogTitle>
                {selectedAluno ? 'Editar Aluno' : 'Novo Aluno'}
              </DialogTitle>
              <DialogDescription>
                {selectedAluno ? 'Edite as informações do aluno' : 'Cadastre um novo aluno na turma'}
              </DialogDescription>
            </DialogHeader>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="space-y-2">
                <label className="text-sm font-medium">Nome Completo</label>
                <Input
                  placeholder="Nome do aluno"
                  value={formData.nome}
                  onChange={(e) => setFormData({ ...formData, nome: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Email</label>
                <Input
                  type="email"
                  placeholder="email@exemplo.com"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Turma</label>
                <Input
                  placeholder="Ex: 321530"
                  value={formData.turma}
                  onChange={(e) => setFormData({ ...formData, turma: e.target.value })}
                  required
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">
                  Senha {selectedAluno && '(deixe vazio para manter a atual)'}
                </label>
                <Input
                  type="password"
                  placeholder={selectedAluno ? 'Nova senha (opcional)' : 'Senha do aluno'}
                  value={formData.senha}
                  onChange={(e) => setFormData({ ...formData, senha: e.target.value })}
                  required={!selectedAluno}
                />
              </div>

              <div className="space-y-2">
                <label className="text-sm font-medium">Status</label>
                <div className="flex space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      name="status"
                      checked={formData.status === 'ativo'}
                      onChange={() => setFormData({ ...formData, status: 'ativo' })}
                    />
                    <span>Ativo</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      name="status"
                      checked={formData.status === 'inativo'}
                      onChange={() => setFormData({ ...formData, status: 'inativo' })}
                    />
                    <span>Inativo</span>
                  </label>
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

              <div className="flex justify-end space-x-2">
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsDialogOpen(false)}
                >
                  Cancelar
                </Button>
                <Button type="submit">
                  {selectedAluno ? 'Salvar' : 'Cadastrar'}
                </Button>
              </div>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Alertas */}
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert>
          <CheckCircle className="h-4 w-4" />
          <AlertDescription className="text-green-700">{success}</AlertDescription>
        </Alert>
      )}

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Alunos</CardTitle>
            <Users className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{alunos.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Alunos Ativos</CardTitle>
            <UserCheck className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {alunos.filter(a => a.status === 'ativo').length}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Alunos Inativos</CardTitle>
            <UserX className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {alunos.filter(a => a.status === 'inativo').length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Barra de busca */}
      <Card>
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Buscar por nome, email ou turma..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Lista de alunos */}
      {filteredAlunos.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <Users className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {searchTerm ? 'Nenhum aluno encontrado' : 'Nenhum aluno cadastrado'}
            </h3>
            <p className="text-gray-500">
              {searchTerm 
                ? 'Tente ajustar os termos de busca'
                : 'Comece cadastrando o primeiro aluno da turma'
              }
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-4">
          {filteredAlunos.map((aluno) => (
            <Card key={aluno.id} className="hover:shadow-lg transition-shadow">
              <CardContent className="pt-6">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-4">
                    <div className="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center">
                      <GraduationCap className="h-6 w-6 text-blue-600" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">{aluno.nome}</h3>
                      <div className="flex items-center space-x-4 text-sm text-gray-500">
                        <div className="flex items-center space-x-1">
                          <Mail className="h-4 w-4" />
                          <span>{aluno.email}</span>
                        </div>
                        <span>Turma: {aluno.turma}</span>
                        <span>Cadastrado em: {formatDate(aluno.created_at)}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center space-x-2">
                    {getStatusBadge(aluno.status)}
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleViewAluno(aluno)}
                      className="flex items-center space-x-1"
                    >
                      <Eye className="h-4 w-4" />
                      <span>Ver</span>
                    </Button>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleOpenDialog(aluno)}
                      className="flex items-center space-x-1"
                    >
                      <Edit className="h-4 w-4" />
                      <span>Editar</span>
                    </Button>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => toggleStatus(aluno)}
                      className={`flex items-center space-x-1 ${
                        aluno.status === 'ativo' ? 'text-red-600 hover:text-red-700' : 'text-green-600 hover:text-green-700'
                      }`}
                    >
                      {aluno.status === 'ativo' ? (
                        <>
                          <UserX className="h-4 w-4" />
                          <span>Desativar</span>
                        </>
                      ) : (
                        <>
                          <UserCheck className="h-4 w-4" />
                          <span>Ativar</span>
                        </>
                      )}
                    </Button>
                    
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(aluno.id)}
                      className="flex items-center space-x-1 text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                      <span>Excluir</span>
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      )}

      {/* Dialog de visualização do aluno */}
      <Dialog open={isViewDialogOpen} onOpenChange={setIsViewDialogOpen}>
        <DialogContent className="sm:max-w-lg">
          <DialogHeader>
            <DialogTitle>Detalhes do Aluno</DialogTitle>
            <DialogDescription>
              Informações e estatísticas de {selectedAluno?.nome}
            </DialogDescription>
          </DialogHeader>
          
          {selectedAluno && (
            <div className="space-y-4">
              {/* Informações básicas */}
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-500">Nome</label>
                  <p className="font-medium">{selectedAluno.nome}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Email</label>
                  <p className="font-medium">{selectedAluno.email}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Turma</label>
                  <p className="font-medium">{selectedAluno.turma}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-500">Status</label>
                  <div className="mt-1">{getStatusBadge(selectedAluno.status)}</div>
                </div>
              </div>

              {/* Estatísticas */}
              {alunoStats && (
                <div className="border-t pt-4">
                  <h4 className="font-medium mb-3">Estatísticas de Desempenho</h4>
                  <div className="grid grid-cols-2 gap-4">
                    <div className="text-center p-3 bg-green-50 rounded-lg">
                      <div className="text-2xl font-bold text-green-600">
                        {alunoStats.entregas_entregues}
                      </div>
                      <div className="text-sm text-green-700">Entregues</div>
                    </div>
                    <div className="text-center p-3 bg-yellow-50 rounded-lg">
                      <div className="text-2xl font-bold text-yellow-600">
                        {alunoStats.entregas_pendentes}
                      </div>
                      <div className="text-sm text-yellow-700">Pendentes</div>
                    </div>
                    <div className="text-center p-3 bg-red-50 rounded-lg">
                      <div className="text-2xl font-bold text-red-600">
                        {alunoStats.entregas_atrasadas}
                      </div>
                      <div className="text-sm text-red-700">Atrasadas</div>
                    </div>
                    <div className="text-center p-3 bg-purple-50 rounded-lg">
                      <div className="text-2xl font-bold text-purple-600">
                        {alunoStats.grupos_como_integrante + alunoStats.grupos_como_lider}
                      </div>
                      <div className="text-sm text-purple-700">Grupos</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default AlunosProfessor;
