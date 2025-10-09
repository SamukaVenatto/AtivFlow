import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { 
  Users, 
  Crown, 
  Calendar, 
  Clock, 
  CheckCircle, 
  AlertTriangle,
  User,
  Briefcase
} from 'lucide-react';

const GruposAluno = () => {
  const { user } = useAuth();
  const [grupos, setGrupos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      fetchGrupos();
    }
  }, [user]);

  const fetchGrupos = async () => {
    try {
      setLoading(true);
      
      const response = await fetch('/api/grupos/');
      if (response.ok) {
        const data = await response.json();
        
        // Filtrar grupos onde o aluno é integrante ou líder
        const meus_grupos = data.filter(grupo => 
          grupo.lider_id === user.id || 
          grupo.integrantes.some(integrante => integrante.aluno_id === user.id)
        );
        
        setGrupos(meus_grupos);
      } else {
        setError('Erro ao carregar grupos');
      }
    } catch (error) {
      console.error('Erro ao carregar grupos:', error);
      setError('Erro ao carregar grupos');
    } finally {
      setLoading(false);
    }
  };

  const getStatusBadge = (status) => {
    const statusConfig = {
      'em_andamento': { color: 'bg-blue-100 text-blue-800', label: 'Em Andamento' },
      'entregue': { color: 'bg-green-100 text-green-800', label: 'Entregue' },
      'atrasado': { color: 'bg-red-100 text-red-800', label: 'Atrasado' }
    };
    
    const config = statusConfig[status] || statusConfig['em_andamento'];
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

  const isLider = (grupo) => {
    return grupo.lider_id === user.id;
  };

  const getMeuPapel = (grupo) => {
    if (isLider(grupo)) {
      return { papel: 'Líder', icon: Crown, color: 'text-yellow-600' };
    }
    
    const meuIntegrante = grupo.integrantes.find(integrante => integrante.aluno_id === user.id);
    return { 
      papel: meuIntegrante?.funcao || 'Integrante', 
      icon: User, 
      color: 'text-blue-600' 
    };
  };

  const getDiasRestantes = (prazoEntrega) => {
    const dias = Math.ceil((new Date(prazoEntrega) - new Date()) / (1000 * 60 * 60 * 24));
    return dias;
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
        <div className="grid gap-6">
          {[1, 2].map((i) => (
            <div key={i} className="animate-pulse">
              <div className="bg-gray-200 rounded-lg h-48"></div>
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
        <h1 className="text-3xl font-bold text-gray-900">Meus Grupos</h1>
        <p className="text-gray-600">
          Acompanhe os projetos em grupo dos quais você participa
        </p>
      </div>

      {error && (
        <Alert variant="destructive">
          <AlertTriangle className="h-4 w-4" />
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Estatísticas rápidas */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total de Grupos</CardTitle>
            <Users className="h-4 w-4 text-blue-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-blue-600">{grupos.length}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Como Líder</CardTitle>
            <Crown className="h-4 w-4 text-yellow-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-yellow-600">
              {grupos.filter(grupo => isLider(grupo)).length}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Em Andamento</CardTitle>
            <Clock className="h-4 w-4 text-green-600" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold text-green-600">
              {grupos.filter(grupo => grupo.status === 'em_andamento').length}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Lista de grupos */}
      {grupos.length === 0 ? (
        <Card>
          <CardContent className="text-center py-12">
            <Users className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Você não está em nenhum grupo
            </h3>
            <p className="text-gray-500">
              Quando o professor criar grupos ou você for adicionado a um, eles aparecerão aqui.
            </p>
          </CardContent>
        </Card>
      ) : (
        <div className="grid gap-6">
          {grupos.map((grupo) => {
            const meuPapel = getMeuPapel(grupo);
            const PapelIcon = meuPapel.icon;
            const diasRestantes = getDiasRestantes(grupo.prazo_entrega);
            const prazoVencido = diasRestantes < 0;
            
            return (
              <Card key={grupo.id} className={`hover:shadow-lg transition-shadow ${prazoVencido && grupo.status !== 'entregue' ? 'border-red-200' : ''}`}>
                <CardHeader>
                  <div className="flex justify-between items-start">
                    <div className="flex-1">
                      <CardTitle className="flex items-center space-x-2">
                        <Users className="h-5 w-5" />
                        <span>{grupo.nome_grupo}</span>
                        {isLider(grupo) && (
                          <Crown className="h-4 w-4 text-yellow-500" title="Você é o líder" />
                        )}
                      </CardTitle>
                      <CardDescription className="mt-2">
                        <div className="space-y-1">
                          <p><strong>Tema:</strong> {grupo.tema_projeto}</p>
                          <div className="flex items-center space-x-4 text-sm">
                            <div className="flex items-center space-x-1">
                              <Calendar className="h-4 w-4" />
                              <span>Prazo: {formatDate(grupo.prazo_entrega)}</span>
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
                        </div>
                      </CardDescription>
                    </div>
                    <div className="flex items-center space-x-2">
                      {getStatusBadge(grupo.status)}
                    </div>
                  </div>
                </CardHeader>
                
                <CardContent>
                  {/* Meu papel no grupo */}
                  <div className="mb-4 p-3 bg-blue-50 rounded-lg">
                    <div className="flex items-center space-x-2">
                      <PapelIcon className={`h-4 w-4 ${meuPapel.color}`} />
                      <span className="font-medium text-sm">Seu papel:</span>
                      <span className={`text-sm ${meuPapel.color}`}>{meuPapel.papel}</span>
                    </div>
                  </div>

                  {/* Informações do líder */}
                  {grupo.lider && (
                    <div className="mb-4">
                      <h4 className="font-medium text-sm mb-2 flex items-center space-x-1">
                        <Crown className="h-4 w-4 text-yellow-500" />
                        <span>Líder do Grupo:</span>
                      </h4>
                      <p className="text-sm text-gray-600">{grupo.lider.nome}</p>
                    </div>
                  )}

                  {/* Lista de integrantes */}
                  <div className="mb-4">
                    <h4 className="font-medium text-sm mb-2 flex items-center space-x-1">
                      <Users className="h-4 w-4" />
                      <span>Integrantes ({grupo.integrantes.length}):</span>
                    </h4>
                    <div className="space-y-2">
                      {grupo.integrantes.map((integrante) => (
                        <div key={integrante.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                          <div className="flex items-center space-x-2">
                            <User className="h-4 w-4 text-gray-500" />
                            <span className="text-sm">
                              {integrante.aluno?.nome || 'Nome não disponível'}
                              {integrante.aluno_id === user.id && (
                                <span className="text-blue-600 font-medium"> (Você)</span>
                              )}
                            </span>
                          </div>
                          {integrante.funcao && (
                            <div className="flex items-center space-x-1">
                              <Briefcase className="h-3 w-3 text-gray-400" />
                              <span className="text-xs text-gray-600">{integrante.funcao}</span>
                            </div>
                          )}
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Alertas de prazo */}
                  <div className="flex justify-between items-center">
                    <div>
                      {prazoVencido && grupo.status !== 'entregue' && (
                        <p className="text-sm text-red-600 font-medium flex items-center space-x-1">
                          <AlertTriangle className="h-4 w-4" />
                          <span>Prazo vencido</span>
                        </p>
                      )}
                      {!prazoVencido && diasRestantes <= 2 && grupo.status !== 'entregue' && (
                        <p className="text-sm text-orange-600 font-medium flex items-center space-x-1">
                          <Clock className="h-4 w-4" />
                          <span>Prazo próximo!</span>
                        </p>
                      )}
                      {grupo.status === 'entregue' && (
                        <p className="text-sm text-green-600 font-medium flex items-center space-x-1">
                          <CheckCircle className="h-4 w-4" />
                          <span>Projeto entregue</span>
                        </p>
                      )}
                    </div>
                    
                    {isLider(grupo) && (
                      <div className="text-xs text-gray-500 bg-yellow-50 px-2 py-1 rounded">
                        👑 Você é responsável por coordenar este grupo
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>
      )}

      {/* Dicas para trabalho em grupo */}
      {grupos.length > 0 && (
        <Card className="bg-blue-50 border-blue-200">
          <CardHeader>
            <CardTitle className="text-blue-800 flex items-center space-x-2">
              <Users className="h-5 w-5" />
              <span>Dicas para Trabalho em Grupo</span>
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-sm text-blue-700 space-y-2">
              <p>• <strong>Comunicação:</strong> Mantenha contato regular com os integrantes do grupo</p>
              <p>• <strong>Organização:</strong> Defina claramente as responsabilidades de cada membro</p>
              <p>• <strong>Prazos:</strong> Estabeleça prazos internos antes do prazo final</p>
              <p>• <strong>Liderança:</strong> Se você é líder, coordene as atividades e mantenha todos informados</p>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default GruposAluno;
