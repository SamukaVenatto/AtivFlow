import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Users, 
  BookOpen, 
  TrendingUp, 
  Clock, 
  CheckCircle, 
  AlertTriangle,
  Calendar,
  BarChart3,
  Target,
  Award
} from 'lucide-react';
import { PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const DashboardProfessor = () => {
  const { user } = useAuth();
  const [stats, setStats] = useState(null);
  const [entregasPorStatus, setEntregasPorStatus] = useState([]);
  const [entregasPorAluno, setEntregasPorAluno] = useState([]);
  const [atividadesProximas, setAtividadesProximas] = useState([]);
  const [gruposStatus, setGruposStatus] = useState([]);
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
      
      // Buscar estatísticas gerais
      const statsResponse = await fetch('/api/dashboard/stats');
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }

      // Buscar entregas por status
      const entregasStatusResponse = await fetch('/api/dashboard/entregas-por-status');
      if (entregasStatusResponse.ok) {
        const entregasStatusData = await entregasStatusResponse.json();
        setEntregasPorStatus(entregasStatusData);
      }

      // Buscar entregas por aluno
      const entregasAlunoResponse = await fetch('/api/dashboard/entregas-por-aluno');
      if (entregasAlunoResponse.ok) {
        const entregasAlunoData = await entregasAlunoResponse.json();
        setEntregasPorAluno(entregasAlunoData.slice(0, 10)); // Top 10
      }

      // Buscar atividades próximas
      const atividadesResponse = await fetch('/api/dashboard/atividades-proximas');
      if (atividadesResponse.ok) {
        const atividadesData = await atividadesResponse.json();
        setAtividadesProximas(atividadesData);
      }

      // Buscar status dos grupos
      const gruposResponse = await fetch('/api/dashboard/grupos-status');
      if (gruposResponse.ok) {
        const gruposData = await gruposResponse.json();
        setGruposStatus(gruposData);
      }

    } catch (error) {
      console.error('Erro ao carregar dados:', error);
      setError('Erro ao carregar dados do dashboard');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  };

  // Cores para os gráficos
  const COLORS = {
    'entregue': '#10B981',
    'pendente': '#F59E0B',
    'atrasado': '#EF4444',
    'em_analise': '#3B82F6',
    'em_andamento': '#3B82F6',
    'ativo': '#10B981'
  };

  const statusLabels = {
    'entregue': 'Entregues',
    'pendente': 'Pendentes',
    'atrasado': 'Atrasadas',
    'em_analise': 'Em Análise',
    'em_andamento': 'Em Andamento',
    'ativo': 'Ativos'
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[1, 2, 3, 4].map((i) => (
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
      {/* Header com saudação */}
      <div className="bg-gradient-to-r from-blue-600 to-purple-700 rounded-lg p-6 text-white">
        <h1 className="text-3xl font-bold mb-2">
          Olá, {user?.nome}! Seja bem-vindo ao AtivFlow 📚
        </h1>
        <p className="text-blue-100">
          Aqui está uma visão geral do desempenho da turma e das atividades
        </p>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Cards de estatísticas principais */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Alunos</CardTitle>
            <Users className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">
              {stats?.total_alunos || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              alunos ativos
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Atividades Ativas</CardTitle>
            <BookOpen className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {stats?.total_atividades || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              atividades criadas
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Grupos Ativos</CardTitle>
            <Users className="h-4 w-4 text-purple-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-purple-600">
              {stats?.total_grupos || 0}
            </div>
            <p className="text-xs text-muted-foreground">
              grupos criados
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-lg transition-shadow">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Taxa de Entrega</CardTitle>
            <TrendingUp className="h-4 w-4 text-orange-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-orange-600">
              {stats?.taxa_entrega || 0}%
            </div>
            <p className="text-xs text-muted-foreground">
              de {stats?.total_entregas || 0} entregas
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Gráficos e análises */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Gráfico de pizza - Status das entregas */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <BarChart3 className="h-5 w-5" />
              <span>Status das Entregas</span>
            </CardTitle>
            <CardDescription>
              Distribuição das entregas por status
            </CardDescription>
          </CardHeader>
          <CardContent>
            {entregasPorStatus.length > 0 ? (
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={entregasPorStatus}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ status, count, percent }) => 
                        `${statusLabels[status] || status}: ${count} (${(percent * 100).toFixed(0)}%)`
                      }
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="count"
                    >
                      {entregasPorStatus.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[entry.status] || '#8884d8'} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value, name, props) => [value, statusLabels[props.payload.status] || props.payload.status]} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-500">
                Nenhum dado disponível
              </div>
            )}
          </CardContent>
        </Card>

        {/* Gráfico de barras - Top alunos por entregas */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Award className="h-5 w-5" />
              <span>Top Alunos - Entregas</span>
            </CardTitle>
            <CardDescription>
              Alunos com mais atividades entregues
            </CardDescription>
          </CardHeader>
          <CardContent>
            {entregasPorAluno.length > 0 ? (
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={entregasPorAluno} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis 
                      dataKey="nome" 
                      angle={-45}
                      textAnchor="end"
                      height={80}
                      fontSize={12}
                    />
                    <YAxis />
                    <Tooltip />
                    <Bar dataKey="entregues" fill="#10B981" name="Entregues" />
                    <Bar dataKey="atrasadas" fill="#EF4444" name="Atrasadas" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="h-64 flex items-center justify-center text-gray-500">
                Nenhum dado disponível
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Atividades próximas do prazo */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <Clock className="h-5 w-5" />
            <span>Atividades Próximas do Prazo</span>
          </CardTitle>
          <CardDescription>
            Atividades que vencem nos próximos 7 dias
          </CardDescription>
        </CardHeader>
        <CardContent>
          {atividadesProximas.length === 0 ? (
            <div className="text-center py-8">
              <Calendar className="h-12 w-12 text-gray-300 mx-auto mb-4" />
              <p className="text-gray-500">Nenhuma atividade próxima do prazo</p>
            </div>
          ) : (
            <div className="space-y-4">
              {atividadesProximas.map((atividade) => (
                <div key={atividade.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium">{atividade.descricao}</h4>
                    <p className="text-sm text-gray-500">
                      Prazo: {formatDate(atividade.prazo_entrega)}
                    </p>
                    <div className="flex items-center space-x-4 mt-2">
                      <span className="text-xs text-gray-600">
                        {atividade.entregas_feitas}/{atividade.total_entregas} entregas
                      </span>
                      <Badge variant={atividade.dias_restantes <= 1 ? 'destructive' : 'secondary'}>
                        {atividade.dias_restantes === 0 ? 'Vence hoje' : `${atividade.dias_restantes} dias`}
                      </Badge>
                    </div>
                  </div>
                  <div className="ml-4">
                    <div className="text-right">
                      <div className="text-2xl font-bold text-blue-600">
                        {Math.round((atividade.entregas_feitas / (atividade.total_entregas || 1)) * 100)}%
                      </div>
                      <div className="text-xs text-gray-500">concluído</div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </CardContent>
      </Card>

      {/* Resumo de desempenho */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Estatísticas detalhadas */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Target className="h-5 w-5" />
              <span>Resumo de Entregas</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Total de Entregas</span>
                <span className="font-bold">{stats?.total_entregas || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-green-600">Entregues</span>
                <span className="font-bold text-green-600">{stats?.entregas_entregues || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-yellow-600">Pendentes</span>
                <span className="font-bold text-yellow-600">{stats?.entregas_pendentes || 0}</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-sm text-red-600">Atrasadas</span>
                <span className="font-bold text-red-600">{stats?.entregas_atrasadas || 0}</span>
              </div>
              
              {/* Barra de progresso geral */}
              <div className="pt-4">
                <div className="flex justify-between text-sm mb-2">
                  <span>Progresso Geral</span>
                  <span className="font-medium">{stats?.taxa_entrega || 0}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-600 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${stats?.taxa_entrega || 0}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Status dos grupos */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center space-x-2">
              <Users className="h-5 w-5" />
              <span>Status dos Grupos</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            {gruposStatus.length === 0 ? (
              <div className="text-center py-8">
                <Users className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500">Nenhum grupo criado</p>
              </div>
            ) : (
              <div className="space-y-3">
                {gruposStatus.map((status) => (
                  <div key={status.status} className="flex justify-between items-center">
                    <span className="text-sm capitalize">
                      {statusLabels[status.status] || status.status}
                    </span>
                    <Badge 
                      className={`${COLORS[status.status] ? 'text-white' : ''}`}
                      style={{ backgroundColor: COLORS[status.status] || '#6B7280' }}
                    >
                      {status.count}
                    </Badge>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Mensagem motivacional */}
      <Card className="bg-gradient-to-r from-green-50 to-blue-50 border-green-200">
        <CardContent className="pt-6">
          <div className="text-center">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              🎯 Continue o excelente trabalho!
            </h3>
            <p className="text-gray-600">
              {stats?.taxa_entrega >= 80 
                ? "A turma está com ótimo desempenho! Continue incentivando os alunos."
                : stats?.taxa_entrega >= 60
                ? "A turma está progredindo bem. Considere dar suporte aos alunos com dificuldades."
                : "Há espaço para melhorias. Considere revisar as estratégias de ensino e dar mais suporte."
              }
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
};

export default DashboardProfessor;
