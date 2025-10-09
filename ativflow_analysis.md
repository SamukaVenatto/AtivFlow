# Análise do Repositório AtivFlow

## Estrutura do Projeto
- **Backend**: Flask (Python) com SQLAlchemy
- **Frontend**: React com Vite e Tailwind CSS
- **Banco**: SQLite (dev) / PostgreSQL (prod)
- **Deploy**: Render

## Arquivos Principais Identificados
- `backend/` - Código do servidor Flask
- `frontend/` - Aplicação React
- `README.md` - Documentação principal
- `requirements.txt` - Dependências Python
- `build.sh` - Script de build
- `followup_feature.patch` - Patch do módulo FollowUp

## Funcionalidades Já Implementadas
✅ Sistema de autenticação (professor/aluno)
✅ Dashboard do professor com métricas
✅ Gestão completa de alunos
✅ Interface responsiva e moderna
✅ Banco de dados estruturado
✅ API REST completa
✅ Deploy em produção

## Funcionalidades Em Desenvolvimento (Nosso Foco)
🚧 Gestão completa de atividades
🚧 Sistema de grupos funcionais
🚧 Relatórios e exportações
🚧 Dashboard do aluno
🚧 Sistema de notificações
🚧 Upload de arquivos

## Modelos de Banco Identificados
1. **Professores** - id, nome, email, senha, created_at
2. **Alunos** - id, nome, email, turma, status, senha, created_at
3. **Atividades** - id, descricao, prazo_entrega, tipo, status, created_at
4. **Entregas** - id, aluno_id, atividade_id, data_entrega, entregue, justificativa, status, funcao_responsabilidade
5. **Grupos** - id, nome_grupo, tema_projeto, prazo_entrega, lider_id, status, created_at
6. **Grupo_Integrantes** - id, grupo_id, aluno_id, funcao, created_at

## Próximos Passos
1. Clonar repositório
2. Analisar código backend atual
3. Implementar as 6 funcionalidades especificadas
