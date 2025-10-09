# AtivFlow API Guide v2.0

Este guia apresenta exemplos de uso das novas rotas implementadas no AtivFlow v2.0.

## Autenticação

Todas as rotas protegidas requerem autenticação via sessão. Faça login primeiro:

```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "professor@senac.com",
    "senha": "123456",
    "tipo_usuario": "professor"
  }'
```

## 1. Sistema de Avaliação

### Avaliar uma entrega (Professor)
```bash
curl -X PUT http://localhost:5000/api/entregas/1/avaliar \
  -H "Content-Type: application/json" \
  -d '{
    "feedback": "Excelente trabalho! Código bem estruturado.",
    "nota": 9.5,
    "status": "revisado"
  }'
```

### Obter estatísticas de entregas (Professor)
```bash
curl -X GET http://localhost:5000/api/entregas/estatisticas
```

## 2. Upload de Arquivos

### Fazer upload de arquivo para entrega
```bash
curl -X POST http://localhost:5000/api/entregas/upload \
  -F "file=@documento.pdf" \
  -F "entrega_id=1"
```

### Remover arquivo de entrega
```bash
curl -X DELETE http://localhost:5000/api/entregas/1/remover-arquivo
```

## 3. Atividades de Múltipla Escolha

### Criar atividade de múltipla escolha (Professor)
```bash
curl -X POST http://localhost:5000/api/atividades/ \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Quiz de JavaScript Básico",
    "prazo_entrega": "2024-12-31",
    "tipo": "multipla_escolha"
  }'
```

### Criar questão (Professor)
```bash
curl -X POST http://localhost:5000/api/atividade/1/questoes \
  -H "Content-Type: application/json" \
  -d '{
    "pergunta": "O que é JavaScript?",
    "opcoes": {
      "A": "Uma linguagem de programação",
      "B": "Um framework CSS",
      "C": "Um banco de dados",
      "D": "Um editor de texto"
    },
    "resposta_correta": "A",
    "pontos": 2.0
  }'
```

### Listar questões de uma atividade
```bash
curl -X GET http://localhost:5000/api/atividade/1/questoes
```

### Responder questões (Aluno)
```bash
curl -X POST http://localhost:5000/api/atividade/1/responder \
  -H "Content-Type: application/json" \
  -d '{
    "respostas": {
      "1": "A",
      "2": "B",
      "3": "C"
    }
  }'
```

### Obter estatísticas da atividade (Professor)
```bash
curl -X GET http://localhost:5000/api/atividade/1/estatisticas
```

## 4. Sistema de Follow-Up

### Criar follow-up (Aluno)
```bash
curl -X POST http://localhost:5000/api/followups \
  -H "Content-Type: application/json" \
  -d '{
    "atividade_texto": "Estudei React hooks",
    "data_realizacao": "2024-01-15",
    "funcao": "Estudos",
    "realizado": true
  }'
```

### Listar meus follow-ups (Aluno)
```bash
curl -X GET http://localhost:5000/api/followups/me?page=1&per_page=10
```

### Listar follow-ups com filtros (Professor)
```bash
curl -X GET "http://localhost:5000/api/admin/followups?aluno_id=1&realizado=true&date_from=2024-01-01"
```

### Marcar follow-up como revisado (Professor)
```bash
curl -X PUT http://localhost:5000/api/admin/followups/1/revisar
```

### Exportar follow-ups para CSV (Professor)
```bash
curl -X GET http://localhost:5000/api/admin/followups/export
```

## 5. Sistema de Notificações

### Listar notificações do usuário
```bash
curl -X GET http://localhost:5000/api/notificacoes?apenas_nao_lidas=true&page=1&per_page=20
```

### Marcar notificação como lida
```bash
curl -X PUT http://localhost:5000/api/notificacoes/1/marcar-lida
```

### Marcar todas as notificações como lidas
```bash
curl -X PUT http://localhost:5000/api/notificacoes/marcar-todas-lidas
```

### Enviar notificação personalizada (Professor)
```bash
curl -X POST http://localhost:5000/api/admin/notificacoes/enviar \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "Lembrete Importante",
    "mensagem": "Não esqueçam da entrega do projeto final!",
    "destinatarios": "todos_alunos",
    "tipo_notificacao": "aviso"
  }'
```

### Obter estatísticas de notificações
```bash
curl -X GET http://localhost:5000/api/notificacoes/estatisticas
```

## 6. Gestão de Alunos e Atividades

### Criar aluno (Professor)
```bash
curl -X POST http://localhost:5000/api/alunos/ \
  -H "Content-Type: application/json" \
  -d '{
    "nome": "Novo Aluno",
    "email": "novo@aluno.com",
    "turma": "321530",
    "status": "ativo"
  }'
```

### Criar atividade individual (Professor)
```bash
curl -X POST http://localhost:5000/api/atividades/ \
  -H "Content-Type: application/json" \
  -d '{
    "descricao": "Exercício de CSS Grid",
    "prazo_entrega": "2024-02-15",
    "tipo": "individual"
  }'
```

## Códigos de Status HTTP

- `200` - Sucesso
- `201` - Criado com sucesso
- `400` - Erro de validação
- `401` - Não autenticado
- `403` - Acesso negado
- `404` - Não encontrado
- `500` - Erro interno do servidor

## Formato de Resposta Padrão

### Sucesso
```json
{
  "success": true,
  "message": "Operação realizada com sucesso",
  "data": { ... }
}
```

### Erro
```json
{
  "error": "Descrição do erro"
}
```

## Tipos de Atividade

- `individual` - Atividade individual (cria entregas automáticas)
- `grupo` - Atividade em grupo
- `upload` - Atividade com upload de arquivo
- `multipla_escolha` - Atividade de múltipla escolha (cria entregas automáticas)

## Status de Entrega

- `pendente` - Entrega não realizada
- `entregue` - Entrega realizada
- `atrasado` - Entrega realizada após o prazo
- `em_analise` - Entrega em análise pelo professor
- `revisado` - Entrega avaliada pelo professor

## Tipos de Notificação

- `info` - Informação geral
- `sucesso` - Operação bem-sucedida
- `aviso` - Alerta importante
- `erro` - Erro ou problema

## Extensões de Arquivo Permitidas

Para upload de arquivos:
- Documentos: `txt`, `pdf`, `doc`, `docx`, `xls`, `xlsx`, `ppt`, `pptx`
- Imagens: `png`, `jpg`, `jpeg`, `gif`
- Vídeos: `mp4`, `avi`, `mov`
- Áudio: `mp3`, `wav`
- Compactados: `zip`, `rar`, `7z`
