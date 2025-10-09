import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import {
  ArrowLeft,
  CheckCircle,
  Clock,
  AlertTriangle,
  User,
  Calendar,
  FileText,
  MessageSquare
} from 'lucide-react';

const EntregasAtividade = ({ atividadeId, onBack }) => {
  const id = atividadeId;
  const [atividade, setAtividade] = useState(null);
  const [entregas, setEntregas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isAvaliarDialogOpen, setIsAvaliarDialogOpen] = useState(false);
  const [entregaSelecionada, setEntregaSelecionada] = useState(null);
  const [avaliacaoData, setAvaliacaoData] = useState({
    status: 'revisado',
    feedback: ''
  });

  useEffect(() => {
    fetchEntregas();
  }, [id]);

  const fetchEntregas = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/professor/atividades/${id}/entregas`, {
        credentials: 'include'
      });
      
      if (response.ok) {
        const data = await response.json();
        setAtividade(data.atividade);
        setEntregas(data.entregas || []);
      } else {
        setError('Erro ao carregar entregas');
      }
    } catch (error) {
      console.error('Erro:', error);
      setError('Erro ao conectar com o servidor');
    } finally {
      setLoading(false);
    }
  };

  const handleAvaliar = async () => {
    if (!entregaSelecionada) return;

    try {
      const response = await fetch(`/api/professor/entregas/${entregaSelecionada.id}/avaliar`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify(avaliacaoData)
      });

      if (response.ok) {
        setSuccess('Entrega avaliada com sucesso!');
        setIsAvaliarDialogOpen(false);
        setEntregaSelecionada(null);
        setAvaliacaoData({ status: 'revisado', feedback: '' });
        fetchEntregas();
      } else {
        const data = await response.json();
        setError(data.error || 'Erro ao avaliar entrega');
      }
    } catch (error) {
      console.error('Erro:', error);
      setError('Erro ao conectar com o servidor');
    }
  };

  const openAvaliarDialog = (entrega) => {
    setEntregaSelecionada(entrega);
    setAvaliacaoData({
      status: entrega.status || 'revisado',
      feedback: entrega.justificativa || ''
    });
    setIsAvaliarDialogOpen(true);
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Não entregue';
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status, entregue) => {
    if (!entregue) {
      return <Badge variant="secondary" className="bg-gray-500">Pendente</Badge>;
    }

    const statusConfig = {
      'entregue': { variant: 'success', className: 'bg-green-500', label: 'Entregue' },
      'atrasado': { variant: 'destructive', className: 'bg-red-500', label: 'Atrasado' },
      'revisado': { variant: 'default', className: 'bg-blue-500', label: 'Revisado' },
      'aprovado': { variant: 'success', className: 'bg-green-600', label: 'Aprovado' },
      'reprovado': { variant: 'destructive', className: 'bg-red-600', label: 'Reprovado' }
    };

    const config = statusConfig[status] || statusConfig['entregue'];
    return <Badge className={config.className}>{config.label}</Badge>;
  };

  const getStatusIcon = (status, entregue) => {
    if (!entregue) {
      return <Clock className="h-5 w-5 text-gray-500" />;
    }
    if (status === 'atrasado') {
      return <AlertTriangle className="h-5 w-5 text-red-500" />;
    }
    return <CheckCircle className="h-5 w-5 text-green-500" />;
  };

  const calcularEstatisticas = () => {
    const total = entregas.length;
    const entregues = entregas.filter(e => e.entregue).length;
    const pendentes = entregas.filter(e => !e.entregue).length;
    const atrasadas = entregas.filter(e => e.status === 'atrasado').length;
    const taxa = total > 0 ? ((entregues / total) * 100).toFixed(1) : 0;

    return { total, entregues, pendentes, atrasadas, taxa };
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-64 bg-gray-200 rounded"></div>
        </div>
      </div>
    );
  }

  const stats = calcularEstatisticas();

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center space-x-4">
        <Button
          variant="outline"
          size="sm"
          onClick={onBack}
        >
          <ArrowLeft className="h-4 w-4 mr-2" />
          Voltar
        </Button>
        <div>
          <h1 className="text-3xl font-bold text-gray-900">
            {atividade?.titulo || 'Atividade'}
          </h1>
          <p className="text-gray-600 mt-1">
            Prazo: {atividade ? formatDate(atividade.prazo_entrega) : ''}
          </p>
        </div>
      </div>

      {/* Alerts */}
      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {success && (
        <Alert className="bg-green-50 border-green-200">
          <CheckCircle className="h-4 w-4 text-green-600" />
          <AlertDescription className="text-green-800">{success}</AlertDescription>
        </Alert>
      )}

      {/* Estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Total</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.total}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Entregues</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">{stats.entregues}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Pendentes</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">{stats.pendentes}</div>
          </CardContent>
        </Card>
        <Card>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-gray-600">Taxa de Entrega</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{stats.taxa}%</div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de Entregas */}
      <Card>
        <CardHeader>
          <CardTitle>Entregas dos Alunos</CardTitle>
          <CardDescription>
            Visualize e avalie as entregas dos alunos
          </CardDescription>
        </CardHeader>
        <CardContent>
          {entregas.length === 0 ? (
            <div className="text-center py-12">
              <FileText className="h-16 w-16 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">Nenhuma entrega encontrada</p>
            </div>
          ) : (
            <div className="space-y-4">
              {entregas.map((entrega) => (
                <div
                  key={entrega.id}
                  className="flex items-center justify-between p-4 border rounded-lg hover:bg-gray-50 transition-colors"
                >
                  <div className="flex items-center space-x-4 flex-1">
                    {getStatusIcon(entrega.status, entrega.entregue)}
                    <div className="flex-1">
                      <div className="flex items-center space-x-3">
                        <h4 className="font-medium text-gray-900">
                          {entrega.aluno?.nome || 'Aluno Desconhecido'}
                        </h4>
                        {getStatusBadge(entrega.status, entrega.entregue)}
                      </div>
                      <div className="flex items-center space-x-4 mt-1 text-sm text-gray-500">
                        <span className="flex items-center">
                          <Calendar className="h-3 w-3 mr-1" />
                          {formatDate(entrega.data_entrega)}
                        </span>
                        {entrega.justificativa && (
                          <span className="flex items-center">
                            <MessageSquare className="h-3 w-3 mr-1" />
                            Tem justificativa
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => openAvaliarDialog(entrega)}
                    disabled={!entrega.entregue}
                  >
                    {entrega.status === 'revisado' || entrega.status === 'aprovado' || entrega.status === 'reprovado'
                      ? 'Ver Avaliação'
                      : 'Avaliar'}
                  </Button>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Dialog de Avaliação */}
      <Dialog open={isAvaliarDialogOpen} onOpenChange={setIsAvaliarDialogOpen}>
        <DialogContent className="max-w-2xl">
          <DialogHeader>
            <DialogTitle>Avaliar Entrega</DialogTitle>
            <DialogDescription>
              Aluno: {entregaSelecionada?.aluno?.nome}
            </DialogDescription>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Informações da Entrega */}
            <div className="bg-gray-50 p-4 rounded-lg space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Data de Entrega:</span>
                <span className="font-medium">{formatDate(entregaSelecionada?.data_entrega)}</span>
              </div>
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Status Atual:</span>
                <span>{getStatusBadge(entregaSelecionada?.status, entregaSelecionada?.entregue)}</span>
              </div>
              {entregaSelecionada?.justificativa && (
                <div className="pt-2 border-t">
                  <span className="text-sm text-gray-600">Justificativa do Aluno:</span>
                  <p className="text-sm mt-1">{entregaSelecionada.justificativa}</p>
                </div>
              )}
            </div>

            {/* Formulário de Avaliação */}
            <div>
              <Label htmlFor="status">Status da Avaliação</Label>
              <Select
                value={avaliacaoData.status}
                onValueChange={(value) => setAvaliacaoData(prev => ({ ...prev, status: value }))}
              >
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="revisado">Revisado</SelectItem>
                  <SelectItem value="aprovado">Aprovado</SelectItem>
                  <SelectItem value="reprovado">Reprovado</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="feedback">Feedback para o Aluno</Label>
              <Textarea
                id="feedback"
                value={avaliacaoData.feedback}
                onChange={(e) => setAvaliacaoData(prev => ({ ...prev, feedback: e.target.value }))}
                rows={5}
                placeholder="Escreva seu feedback aqui..."
              />
            </div>
          </div>

          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => {
                setIsAvaliarDialogOpen(false);
                setEntregaSelecionada(null);
              }}
            >
              Cancelar
            </Button>
            <Button onClick={handleAvaliar}>
              Salvar Avaliação
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default EntregasAtividade;
