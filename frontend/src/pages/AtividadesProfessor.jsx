import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Badge } from '@/components/ui/badge';
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { Plus, Calendar, Users, User, Search, Edit, Trash2, Eye } from 'lucide-react';

const AtividadesProfessor = () => {
  const [atividades, setAtividades] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingAtividade, setEditingAtividade] = useState(null);
  const [formData, setFormData] = useState({
    descricao: '',
    prazo_entrega: '',
    tipo: 'individual'
  });

  // Carregar atividades
  useEffect(() => {
    fetchAtividades();
  }, []);

  const fetchAtividades = async () => {
    try {
      const response = await fetch('/api/atividades');
      if (response.ok) {
        const data = await response.json();
        setAtividades(data);
      }
    } catch (error) {
      console.error('Erro ao carregar atividades:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const url = editingAtividade 
        ? `/api/atividades/${editingAtividade.id}`
        : '/api/atividades';
      
      const method = editingAtividade ? 'PUT' : 'POST';
      
      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        fetchAtividades();
        setIsDialogOpen(false);
        setEditingAtividade(null);
        setFormData({
          descricao: '',
          prazo_entrega: '',
          tipo: 'individual'
        });
      }
    } catch (error) {
      console.error('Erro ao salvar atividade:', error);
    }
  };

  const handleEdit = (atividade) => {
    setEditingAtividade(atividade);
    setFormData({
      descricao: atividade.descricao,
      prazo_entrega: atividade.prazo_entrega ? atividade.prazo_entrega.split('T')[0] : '',
      tipo: atividade.tipo
    });
    setIsDialogOpen(true);
  };

  const handleDelete = async (id) => {
    if (window.confirm('Tem certeza que deseja excluir esta atividade?')) {
      try {
        const response = await fetch(`/api/atividades/${id}`, {
          method: 'DELETE',
        });

        if (response.ok) {
          fetchAtividades();
        }
      } catch (error) {
        console.error('Erro ao excluir atividade:', error);
      }
    }
  };

  const filteredAtividades = atividades.filter(atividade =>
    atividade.descricao.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const formatDate = (dateString) => {
    if (!dateString) return 'Não definido';
    return new Date(dateString).toLocaleDateString('pt-BR');
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      ativa: { color: 'bg-green-100 text-green-800', text: 'Ativa' },
      inativa: { color: 'bg-gray-100 text-gray-800', text: 'Inativa' },
      finalizada: { color: 'bg-blue-100 text-blue-800', text: 'Finalizada' }
    };
    
    const config = statusConfig[status] || statusConfig.ativa;
    return <Badge className={config.color}>{config.text}</Badge>;
  };

  const getTipoBadge = (tipo) => {
    return tipo === 'grupo' ? (
      <Badge variant="outline" className="text-purple-600 border-purple-200">
        <Users className="w-3 h-3 mr-1" />
        Grupo
      </Badge>
    ) : (
      <Badge variant="outline" className="text-blue-600 border-blue-200">
        <User className="w-3 h-3 mr-1" />
        Individual
      </Badge>
    );
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="text-lg text-gray-600">Carregando atividades...</div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Gerenciar Atividades</h1>
          <p className="text-gray-600">Crie e gerencie as atividades da turma</p>
        </div>
        
        <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
          <DialogTrigger asChild>
            <Button onClick={() => {
              setEditingAtividade(null);
              setFormData({
                descricao: '',
                prazo_entrega: '',
                tipo: 'individual'
              });
            }}>
              <Plus className="w-4 h-4 mr-2" />
              Nova Atividade
            </Button>
          </DialogTrigger>
          
          <DialogContent className="sm:max-w-[500px]">
            <DialogHeader>
              <DialogTitle>
                {editingAtividade ? 'Editar Atividade' : 'Nova Atividade'}
              </DialogTitle>
              <DialogDescription>
                {editingAtividade 
                  ? 'Edite as informações da atividade'
                  : 'Preencha os dados para criar uma nova atividade'
                }
              </DialogDescription>
            </DialogHeader>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <Label htmlFor="descricao">Descrição da Atividade</Label>
                <Textarea
                  id="descricao"
                  value={formData.descricao}
                  onChange={(e) => setFormData({...formData, descricao: e.target.value})}
                  placeholder="Descreva a atividade..."
                  required
                />
              </div>
              
              <div>
                <Label htmlFor="prazo">Prazo de Entrega</Label>
                <Input
                  id="prazo"
                  type="date"
                  value={formData.prazo_entrega}
                  onChange={(e) => setFormData({...formData, prazo_entrega: e.target.value})}
                  required
                />
              </div>
              
              <div>
                <Label htmlFor="tipo">Tipo de Atividade</Label>
                <Select value={formData.tipo} onValueChange={(value) => setFormData({...formData, tipo: value})}>
                  <SelectTrigger>
                    <SelectValue placeholder="Selecione o tipo" />
                  </SelectTrigger>
                  <SelectContent>
                    <SelectItem value="individual">Individual</SelectItem>
                    <SelectItem value="grupo">Em Grupo</SelectItem>
                  </SelectContent>
                </Select>
              </div>
              
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancelar
                </Button>
                <Button type="submit">
                  {editingAtividade ? 'Salvar Alterações' : 'Criar Atividade'}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Atividades</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{atividades.length}</div>
            <p className="text-xs text-muted-foreground">atividades criadas</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Atividades Ativas</CardTitle>
            <Calendar className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {atividades.filter(a => a.status === 'ativa').length}
            </div>
            <p className="text-xs text-muted-foreground">em andamento</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Individuais</CardTitle>
            <User className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">
              {atividades.filter(a => a.tipo === 'individual').length}
            </div>
            <p className="text-xs text-muted-foreground">atividades individuais</p>
          </CardContent>
        </Card>
        
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Em Grupo</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {atividades.filter(a => a.tipo === 'grupo').length}
            </div>
            <p className="text-xs text-muted-foreground">atividades em grupo</p>
          </CardContent>
        </Card>
      </div>

      {/* Busca */}
      <Card>
        <CardContent className="pt-6">
          <div className="relative">
            <Search className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
            <Input
              placeholder="Buscar atividades..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </CardContent>
      </Card>

      {/* Lista de Atividades */}
      <div className="space-y-4">
        {filteredAtividades.length === 0 ? (
          <Card>
            <CardContent className="pt-6">
              <div className="text-center py-8">
                <Calendar className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">Nenhuma atividade encontrada</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {searchTerm ? 'Tente buscar com outros termos.' : 'Comece criando uma nova atividade.'}
                </p>
              </div>
            </CardContent>
          </Card>
        ) : (
          filteredAtividades.map((atividade) => (
            <Card key={atividade.id} className="hover:shadow-md transition-shadow">
              <CardContent className="pt-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-semibold text-gray-900">
                        {atividade.descricao}
                      </h3>
                      {getTipoBadge(atividade.tipo)}
                      {getStatusBadge(atividade.status)}
                    </div>
                    
                    <div className="flex items-center gap-4 text-sm text-gray-600">
                      <div className="flex items-center gap-1">
                        <Calendar className="w-4 h-4" />
                        <span>Prazo: {formatDate(atividade.prazo_entrega)}</span>
                      </div>
                      <div className="flex items-center gap-1">
                        <span>Criado em: {formatDate(atividade.created_at)}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex items-center gap-2">
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleEdit(atividade)}
                    >
                      <Edit className="w-4 h-4" />
                    </Button>
                    <Button
                      variant="outline"
                      size="sm"
                      onClick={() => handleDelete(atividade.id)}
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

export default AtividadesProfessor;
