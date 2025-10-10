// src/pages/AtividadesAluno.jsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Send } from 'lucide-react';

const AtividadesAluno = () => {
  const { user } = useAuth();
  const [entregas, setEntregas] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Estado do formulário
  const [formData, setFormData] = useState({
    nome: user?.nome || '',
    atividade: '',
    data_realizacao: new Date().toISOString().split('T')[0],
    funcao_responsabilidade: '',
    realizado: false,
    justificativa: ''
  });

  useEffect(() => {
    if (user) {
      fetchEntregas();
    }
  }, [user]);

  const fetchEntregas = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/entregas/aluno/${user.id}`);
      if (response.ok) {
        const data = await response.json();
        setEntregas(data);
      } else {
        throw new Error('Erro ao carregar entregas');
      }
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('/api/entregas', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...formData,
          aluno_id: user.id
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(data.message);
        setFormData({
          nome: user.nome || '',
          atividade: '',
          data_realizacao: new Date().toISOString().split('T')[0],
          funcao_responsabilidade: '',
          realizado: false,
          justificativa: ''
        });
        fetchEntregas(); // Recarrega a lista
        setTimeout(() => setSuccess(''), 3000);
      } else {
        setError(data.error || 'Erro ao enviar atividade');
      }
    } catch (err) {
      setError('Erro de conexão com o servidor');
    }
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
      <Card>
        <CardHeader>
          <CardTitle className="text-center">FOLLOW UP - PREENCHIMENTO INDIVIDUAL</CardTitle>
        </CardHeader>
      </Card>

      {/* Formulário */}
      <Card>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="text-sm font-medium">NOME</label>
                <Input
                  name="nome"
                  value={formData.nome}
                  onChange={handleChange}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">ATIVIDADE REALIZADA</label>
                <Input
                  name="atividade"
                  value={formData.atividade}
                  onChange={handleChange}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">DATA DE REALIZAÇÃO</label>
                <Input
                  type="date"
                  name="data_realizacao"
                  value={formData.data_realizacao}
                  onChange={handleChange}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">FUNÇÃO RESPONSABILIDADE</label>
                <Input
                  name="funcao_responsabilidade"
                  value={formData.funcao_responsabilidade}
                  onChange={handleChange}
                  required
                />
              </div>
              <div>
                <label className="text-sm font-medium">REALIZADO</label>
                <div className="flex items-center space-x-4">
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      name="realizado"
                      checked={!formData.realizado}
                      onChange={() => setFormData({ ...formData, realizado: false })}
                    />
                    <span>Não</span>
                  </label>
                  <label className="flex items-center space-x-2">
                    <input
                      type="radio"
                      name="realizado"
                      checked={formData.realizado}
                      onChange={() => setFormData({ ...formData, realizado: true })}
                    />
                    <span>Sim</span>
                  </label>
                </div>
              </div>
              <div>
                <label className="text-sm font-medium">JUSTIFICATIVA</label>
                <Textarea
                  name="justificativa"
                  value={formData.justificativa}
                  onChange={handleChange}
                  rows={2}
                />
              </div>
            </div>

            <Button type="submit" className="w-full flex items-center justify-center space-x-2">
              <Send className="h-4 w-4" />
              <span>ENVIAR ATIVIDADE</span>
            </Button>
          </form>
        </CardContent>
      </Card>

      {/* Mensagens */}
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

      {/* Tabela de histórico */}
      <Card>
        <CardHeader>
          <CardTitle>Histórico de Atividades</CardTitle>
        </CardHeader>
        <CardContent>
          {entregas.length === 0 ? (
            <p className="text-center text-gray-500 py-8">Nenhuma atividade registrada.</p>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>NOME</TableHead>
                  <TableHead>ATIVIDADE REALIZADA</TableHead>
                  <TableHead>DATA DE REALIZAÇÃO</TableHead>
                  <TableHead>FUNÇÃO RESPONSABILIDADE</TableHead>
                  <TableHead>REALIZADO</TableHead>
                  <TableHead>JUSTIFICATIVA</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {entregas.map((entrega, i) => (
                  <TableRow key={i}>
                    <TableCell>{entrega.nome}</TableCell>
                    <TableCell>{entrega.atividade}</TableCell>
                    <TableCell>{new Date(entrega.data_realizacao).toLocaleDateString()}</TableCell>
                    <TableCell>{entrega.funcao_responsabilidade}</TableCell>
                    <TableCell>{entrega.realizado ? 'Sim' : 'Não'}</TableCell>
                    <TableCell>{entrega.justificativa || '-'}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default AtividadesAluno;