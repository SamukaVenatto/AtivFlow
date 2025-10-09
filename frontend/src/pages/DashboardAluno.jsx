import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  CheckCircle, 
  Clock, 
  AlertTriangle, 
  BookOpen, 
  Users, 
  Calendar,
  TrendingUp
} from 'lucide-react';

const DashboardAluno = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [entregas, setEntregas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      fetchDashboardData();
    }
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Buscar estatísticas do aluno
      const statsResponse = await fetch(`/api/dashboard/aluno/${user.id}/stats`);
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }

      // Buscar entregas do aluno
      const entregasResponse = await fetch(`/api/entregas/aluno/${user.id}`);
      if (entregasResponse.ok) {
        const entregasData = await entregasResponse.json();
        setEntregas(entregasData);
      }

    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      setError('Erro ao carregar dados do dashboard');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'entregue': { color: 'bg-green-100 text-green-800', label: 'Entregue' },
      'pendente': { color: 'bg-yellow-100 text-yellow-800', label: 'Pendente' },
      'atrasado': { color: 'bg-red-100 text-red-800', label: 'Atrasado' },
      'em_analise': { color: 'bg-blue-100 text-blue-800', label: 'Em Análise' }
    };
    
    const config = statusConfig[status] || statusConfig['pendente'];
    return (
      <Badge className={config.color}>
        {config.label}
      </Badge>
    );
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

  const getMotivationalMessage = () => {
    if (!stats) return '';
    
    const { entregas_entregues, total_entregas, entregas_atrasadas } = stats;
    
    if (total_entregas === 0) {
      return "🎯 Pronto para começar! Suas atividades aparecerão aqui.";
    }
    
    if (entregas_entregues === total_entregas) {
      return "🎉 Parabéns! Você está em dia com todas as atividades!";
    }
    
    if (entregas_atrasadas === 0) {
      return "👏 Excelente! Você não tem atividades em atraso.";
    }
    
    return "💪 Continue assim! Você está fazendo um ótimo trabalho.";
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {[1, 2, 3].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="bg-gray-200 rounded-lg h-32"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header com saudação personalizada */}
      <div className="bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">
          Bem-vindo, {user?.nome}! 👋
        </h1>
        <p className="text-blue-100 mb-4">
          Aqui está um resumo das suas atividades e progresso
        </p>
        
        {/* Mensagem motivacional */}
        <div className="bg-white/10 rounded-lg p-4 backdrop-blur-sm">
          <p className="text-white font-medium">
            {getMotivationalMessage()}
          </p>
        </div>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Cards de estatísticas */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Atividades Entregues</CardTitle>
            <CheckCircle className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {stats?.entregas_entregues || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              de {stats?.total_entregas || 0} atividades
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Pendentes</CardTitle>
            <Clock className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">
              {stats?.entregas_pendentes || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              aguardando entrega
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Atrasadas</CardTitle>
            <AlertTriangle className="h-4 w-4 text-red-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-red-600">
              {stats?.entregas_atrasadas || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              precisam de atenção
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Grupos</CardTitle>
            <Users className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">
              {(stats?.grupos_como_integrante || 0) + (stats?.grupos_como_lider || 0)}
            </div>
            <p className="text-xs text-muted-foreground">
              {stats?.grupos_como_lider || 0} como líder
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Atividades próximas do prazo */}
      {stats?.atividades_proximas > 0 && (
        <Alert>
          <Calendar className="h-4 w-4" />
          <AlertDescription>
            Você tem <strong>{stats.atividades_proximas}</strong> atividade(s) com prazo próximo. 
            Não esqueça de entregá-las!
          </AlertDescription>
        </Alert>
      )}

      {/* Lista de atividades recentes */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BookOpen className="h-5 w-5" />
              <span>Atividades Recentes</span>
            </CardTitle>
            <CardDescription>
              Suas últimas entregas e atividades pendentes
            </CardDescription>
          </CardHeader>
          <CardContent>
            {entregas.length === 0 ? (
              <div className="text-center py-8">
                <BookOpen className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">Nenhuma atividade encontrada</p>
                <p className="text-sm text-gray-400">
                  Suas atividades aparecerão aqui quando forem criadas
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                {entregas.slice(0, 5).map((entrega) => (
                  <div key={entrega.id} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                    <div className="flex-1">
                      <h4 className="font-medium text-sm">
                        {entrega.atividade?.descricao || 'Atividade sem título'}
                      </h4>
                      <p className="text-xs text-gray-500">
                        Prazo: {entrega.atividade?.prazo_entrega ? formatDate(entrega.atividade.prazo_entrega) : 'Não definido'}
                      </p>
                      {entrega.funcao_responsabilidade && (
                        <p className="text-xs text-blue-600">
                          Função: {entrega.funcao_responsabilidade}
                        </p>
                      )}
                    </div>
                    <div className="ml-4">
                      {getStatusBadge(entrega.status)}
                    </div>
                  </div>
                ))}
                
                {entregas.length > 5 && (
                  <div className="text-center pt-2">
                    <p className="text-sm text-gray-500">
                      E mais {entregas.length - 5} atividade(s)...
                    </p>
                  </div>
                )}
              </div>
            )}
          </CardContent>
        </Card>

        {/* Card de progresso */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5" />
              <span>Seu Progresso</span>
            </CardTitle>
            <CardDescription>
              Acompanhe seu desempenho geral
            </CardDescription>
          </CardHeader>
          <CardContent>
            {stats && stats.total_entregas > 0 ? (
              <div className="space-y-4">
                {/* Barra de progresso */}
                <div>
                  <div className="flex justify-between text-sm mb-2">
                    <span>Taxa de Entrega</span>
                    <span className="font-medium">
                      {Math.round((stats.entregas_entregues / stats.total_entregas) * 100)}%
                    </span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-green-600 h-2 rounded-full transition-all duration-300"
                      style={{ 
                        width: `${(stats.entregas_entregues / stats.total_entregas) * 100}%` 
                      }}
                    ></div>
                  </div>
                </div>

                {/* Estatísticas detalhadas */}
                <div className="grid grid-cols-2 gap-4 pt-4">
                  <div className="text-center">
                    <div className="text-2xl font-bold text-green-600">
                      {stats.entregas_entregues}
                    </div>
                    <div className="text-xs text-gray-500">Entregues</div>
                  </div>
                  <div className="text-center">
                    <div className="text-2xl font-bold text-yellow-600">
                      {stats.entregas_pendentes}
                    </div>
                    <div className="text-xs text-gray-500">Pendentes</div>
                  </div>
                </div>

                {/* Dicas baseadas no desempenho */}
                <div className="mt-4 p-3 bg-blue-50 rounded-lg">
                  <p className="text-sm text-blue-700">
                    {stats.entregas_atrasadas === 0 
                      ? "🎯 Excelente! Continue mantendo suas entregas em dia."
                      : "⏰ Dica: Organize um cronograma para não perder prazos."
                    }
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center py-8">
                <TrendingUp className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">Sem dados de progresso</p>
                <p className="text-sm text-gray-400">
                  Complete algumas atividades para ver seu progresso
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default DashboardAluno;
