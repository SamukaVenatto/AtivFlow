import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle, DialogTrigger } from '@/components/ui/dialog';
import { 
  BookOpen, 
  Plus, 
  Edit, 
  Clock, 
  CheckCircle, 
  AlertTriangle,
  Calendar,
  User,
  Users,
  Send
} from 'lucide-react';

const AtividadesAluno = () => {
  const { user } = useAuth();
  const [atividades, setAtividades] = useState([]);
  const [entregas, setEntregas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [selectedAtividade, setSelectedAtividade] = useState(null);
  const [isDialogOpen, setIsDialogOpen] = useState(false);

  // Estados do formulário de entrega
  const [formData, setFormData] = useState({
    entregue: false,
    justificativa: '',
    funcao_responsabilidade: ''
  });

  useEffect(() => {
    if (user) {
      fetchData();
    }
  }, [user]);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Buscar atividades ativas
      const atividadesResponse = await fetch('/api/atividades/ativas');
      if (atividadesResponse.ok) {
        const atividadesData = await atividadesResponse.json();
        setAtividades(atividadesData);
      }

      // Buscar entregas do aluno
      const entregasResponse = await fetch(`/api/entregas/aluno/${user.id}`);
      if (entregasResponse.ok) {
        const entregasData = await entregasResponse.json();
        setEntregas(entregasData);
      }

    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      setError('Erro ao carregar atividades');
    } finally {
      setLoading(false);
    }
  };

  const getEntregaForAtividade = (atividadeId) => {
    return entregas.find(entrega => entrega.atividade_id === atividadeId);
  };

  const getStatusBadge = (atividade) => {
    const entrega = getEntregaForAtividade(atividade.id);
    const prazoVencido = new Date() > new Date(atividade.prazo_entrega);
    
    if (!entrega) {
      return prazoVencido 
        ? <Badge className="bg-red-100 text-red-800">Não Entregue</Badge>
        : <Badge className="bg-gray-100 text-gray-800">Pendente</Badge>;
    }
    
    if (entrega.entregue) {
      return entrega.status === 'atrasado'
        ? <Badge className="bg-orange-100 text-orange-800">Entregue (Atrasado)</Badge>
        : <Badge className="bg-green-100 text-green-800">Entregue</Badge>;
    }
    
    return prazoVencido
      ? <Badge className="bg-red-100 text-red-800">Atrasado</Badge>
      : <Badge className="bg-yellow-100 text-yellow-800">Pendente</Badge>;
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleOpenDialog = (atividade) => {
    setSelectedAtividade(atividade);
    const entrega = getEntregaForAtividade(atividade.id);
    
    if (entrega) {
      setFormData({
        entregue: entrega.entregue,
        justificativa: entrega.justificativa || '',
        funcao_responsabilidade: entrega.funcao_responsabilidade || ''
      });
    } else {
      setFormData({
        entregue: false,
        justificativa: '',
        funcao_responsabilidade: ''
      });
    }
    
    setIsDialogOpen(true);
    setError('');
    setSuccess('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!selectedAtividade) return;
    
    try {
      const entrega = getEntregaForAtividade(selectedAtividade.id);
      const url = entrega 
        ? `/api/entregas/${entrega.id}`
        : '/api/entregas/';
      
      const method = entrega ? 'PUT' : 'POST';
      
      const payload = {
        ...formData,
        aluno_id: user.id,
        atividade_id: selectedAtividade.id
      };

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
        await fetchData(); // Recarregar dados
        setTimeout(() => {
          setIsDialogOpen(false);
          setSuccess('');
        }, 2000);
      } else {
        setError(data.error);
      }
    } catch (error) {
      setError('Erro ao salvar entrega');
    }
  };

  const canEdit = (atividade) => {
    const entrega = getEntregaForAtividade(atividade.id);
    const prazoVencido = new Date() > new Date(atividade.prazo_entrega);
    
    // Pode editar se não passou do prazo ou se já entregou mas ainda está no prazo
    return !prazoVencido || (entrega && entrega.entregue);
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <div className="grid gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="bg-gray-200 rounded-lg h-40"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Minhas Atividades</h1>
        <p className="text-gray-600">
          Gerencie suas entregas e acompanhe o progresso das atividades
        </p>
      </div>

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

      {/* Lista de atividades */}
      {atividades.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <BookOpen className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Nenhuma atividade disponível
            </h3>
            <p className="text-gray-500">
              Quando o professor criar atividades, elas aparecerão aqui.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6">
          {atividades.map((atividade) => {
            const entrega = getEntregaForAtividade(atividade.id);
            const prazoVencido = new Date() > new Date(atividade.prazo_entrega);
            const diasRestantes = Math.ceil((new Date(atividade.prazo_entrega) - new Date()) / (1000 * 60 * 60 * 24));
            
            return (
              <Card key={atividade.id} className={`hover:shadow-lg transition-shadow ${prazoVencido && !entrega?.entregue ? 'border-red-200' : ''}`}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="flex items-center space-x-2">
                        <BookOpen className="h-5 w-5" />
                        <span>{atividade.descricao}</span>
                      </CardTitle>
                      <CardDescription className="mt-2">
                        <div className="flex items-center space-x-4 text-sm">
                          <div className="flex items-center space-x-1">
                            {atividade.tipo === 'individual' ? (
                              <User className="h-4 w-4" />
                            ) : (
                              <Users className="h-4 w-4" />
                            )}
                            <span className="capitalize">{atividade.tipo}</span>
                          </div>
                          <div className="flex items-center space-x-1">
                            <Calendar className="h-4 w-4" />
                            <span>Prazo: {formatDate(atividade.prazo_entrega)}</span>
                          </div>
                          {!prazoVencido && diasRestantes >= 0 && (
                            <div className="flex items-center space-x-1">
                              <Clock className="h-4 w-4" />
                              <span className={diasRestantes <= 2 ? 'text-red-600 font-medium' : ''}>
                                {diasRestantes === 0 ? 'Vence hoje!' : `${diasRestantes} dias restantes`}
                              </span>
                            </div>
                          )}
                        </div>
                      </CardDescription>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusBadge(atividade)}
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent>
                  {entrega && (
                    <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                      <h4 className="font-medium text-sm mb-2">Sua Entrega:</h4>
                      {entrega.funcao_responsabilidade && (
                        <p className="text-sm text-gray-600 mb-1">
                          <strong>Função/Responsabilidade:</strong> {entrega.funcao_responsabilidade}
                        </p>
                      )}
                      {entrega.justificativa && (
                        <p className="text-sm text-gray-600 mb-1">
                          <strong>Justificativa:</strong> {entrega.justificativa}
                        </p>
                      )}
                      <p className="text-xs text-gray-500">
                        Última atualização: {formatDate(entrega.updated_at)}
                      </p>
                    </div>
                  )}
                  
                  <div className="flex justify-between items-center">
                    <div>
                      {prazoVencido && !entrega?.entregue && (
                        <p className="text-sm text-red-600 font-medium">
                          ⚠️ Prazo vencido
                        </p>
                      )}
                      {!prazoVencido && diasRestantes <= 2 && (
                        <p className="text-sm text-orange-600 font-medium">
                          ⏰ Prazo próximo!
                        </p>
                      )}
                    </div>
                    
                    <Dialog open={isDialogOpen && selectedAtividade?.id === atividade.id} onOpenChange={setIsDialogOpen}>
                      <DialogTrigger asChild>
                        <Button
                          onClick={() => handleOpenDialog(atividade)}
                          disabled={!canEdit(atividade)}
                          className="flex items-center space-x-2"
                        >
                          {entrega ? (
                            <>
                              <Edit className="h-4 w-4" />
                              <span>Editar Entrega</span>
                            </>
                          ) : (
                            <>
                              <Plus className="h-4 w-4" />
                              <span>Fazer Entrega</span>
                            </>
                          )}
                        </Button>
                      </DialogTrigger>
                      
                      <DialogContent className="sm:max-w-md">
                        <DialogHeader>
                          <DialogTitle>
                            {entrega ? 'Editar Entrega' : 'Nova Entrega'}
                          </DialogTitle>
                          <DialogDescription>
                            {atividade.descricao}
                          </DialogDescription>
                        </DialogHeader>
                        
                        <form onSubmit={handleSubmit} className="space-y-4">
                          <div className="space-y-2">
                            <label className="text-sm font-medium">Status da Entrega</label>
                            <div className="flex space-x-4">
                              <label className="flex items-center space-x-2">
                                <input
                                  type="radio"
                                  name="entregue"
                                  checked={!formData.entregue}
                                  onChange={() => setFormData({ ...formData, entregue: false })}
                                />
                                <span>Não Entregue</span>
                              </label>
                              <label className="flex items-center space-x-2">
                                <input
                                  type="radio"
                                  name="entregue"
                                  checked={formData.entregue}
                                  onChange={() => setFormData({ ...formData, entregue: true })}
                                />
                                <span>Entregue</span>
                              </label>
                            </div>
                          </div>

                          <div className="space-y-2">
                            <label className="text-sm font-medium">
                              Função ou Responsabilidade
                            </label>
                            <Input
                              placeholder="Descreva sua função na atividade"
                              value={formData.funcao_responsabilidade}
                              onChange={(e) => setFormData({ 
                                ...formData, 
                                funcao_responsabilidade: e.target.value 
                              })}
                            />
                          </div>

                          <div className="space-y-2">
                            <label className="text-sm font-medium">
                              Justificativa
                            </label>
                            <Textarea
                              placeholder="Adicione observações, dificuldades ou comentários sobre a atividade"
                              value={formData.justificativa}
                              onChange={(e) => setFormData({ 
                                ...formData, 
                                justificativa: e.target.value 
                              })}
                              rows={3}
                            />
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
                            <Button type="submit" className="flex items-center space-x-2">
                              <Send className="h-4 w-4" />
                              <span>Salvar</span>
                            </Button>
                          </div>
                        </form>
                      </DialogContent>
                    </Dialog>
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default AtividadesAluno;
