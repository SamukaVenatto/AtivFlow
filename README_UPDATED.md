# AtivFlow - Sistema de Gestão de Entregas de Atividades

## 📚 Sobre o Projeto

O **AtivFlow** é um sistema ERP educacional desenvolvido especificamente para a gestão de atividades escolares da turma 321530 do SENAC. O sistema permite o controle completo de entregas de atividades, formação de grupos, acompanhamento de desempenho, avaliação de entregas e geração de relatórios detalhados.

## 🚀 Funcionalidades Principais

### Para Professores
- **Dashboard Administrativo**: Visão geral completa da turma com métricas em tempo real
- **Gestão de Alunos**: Cadastro, edição e controle de status dos alunos
- **Gestão de Atividades**: Criação e acompanhamento de atividades individuais, em grupo, upload e múltipla escolha
- **Sistema de Avaliação**: Avaliação de entregas com feedback e notas
- **Gestão de Grupos**: Formação e monitoramento de grupos de trabalho
- **Sistema de Follow-Up**: Acompanhamento detalhado das atividades dos alunos
- **Atividades de Múltipla Escolha**: Criação de questões com correção automática
- **Sistema de Notificações**: Alertas sobre prazos, entregas e avaliações
- **Relatórios Detalhados**: Análises de desempenho e exportação de dados

### Para Alunos
- **Dashboard Pessoal**: Visão das atividades pendentes e entregues
- **Gestão de Entregas**: Controle de atividades individuais com upload de arquivos
- **Atividades de Múltipla Escolha**: Resposta a questões com correção automática
- **Participação em Grupos**: Visualização e interação com grupos
- **Sistema de Follow-Up**: Registro de atividades realizadas
- **Notificações**: Recebimento de alertas sobre atividades e avaliações
- **Histórico de Atividades**: Acompanhamento do próprio desempenho

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask** (Python) - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** (desenvolvimento) / **PostgreSQL** (produção) - Banco de dados
- **Flask-CORS** - Controle de CORS
- **Werkzeug** - Utilitários de segurança
- **Flask-Migrate** - Migrações de banco de dados

### Frontend
- **React** - Biblioteca JavaScript
- **Vite** - Build tool e servidor de desenvolvimento
- **Tailwind CSS** - Framework CSS
- **Lucide React** - Ícones
- **React Router** - Roteamento

## 📋 Estrutura do Banco de Dados

### Tabelas Principais

1. **Professores**
   - id, nome, email, senha, created_at

2. **Alunos**
   - id, nome, email, turma, status, senha, created_at

3. **Atividades**
   - id, descricao, prazo_entrega, tipo (individual/grupo/upload/multipla_escolha), status, created_at

4. **Entregas**
   - id, aluno_id, atividade_id, data_entrega, entregue, justificativa, status
   - **Novos campos**: feedback, nota, avaliado_por, data_avaliacao, arquivo_url

5. **Grupos**
   - id, nome_grupo, tema_projeto, prazo_entrega, lider_id, status, created_at

6. **Grupo_Integrantes**
   - id, grupo_id, aluno_id, funcao, created_at

7. **FollowUp** (Sistema de Acompanhamento)
   - id, aluno_id, atividade_id, atividade_texto, data_realizacao, funcao, realizado, justificativa, revisado, created_at

8. **Questoes** (Múltipla Escolha)
   - id, atividade_id, pergunta, opcoes (JSON), resposta_correta, pontos, ordem, created_at

9. **Respostas_Aluno** (Múltipla Escolha)
   - id, questao_id, aluno_id, entrega_id, resposta_escolhida, correta, pontos_obtidos, created_at

10. **Notificacoes**
    - id, usuario_id, tipo_usuario, titulo, mensagem, tipo_notificacao, lida, data_criacao, data_leitura

## 🔧 Instalação e Configuração

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- pnpm ou npm

### Backend (Flask)
```shell
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\\Scripts\\activate     # Windows
pip install -r requirements.txt
python src/main.py
```

### Frontend (React)
```shell
cd frontend
pnpm install
pnpm run dev
```

## 🌐 Deploy

O sistema está deployado e acessível em: **https://g8h3ilc399xw.manus.space**

### Credenciais de Teste

**Professor:**
- Email: professor@senac.com
- Senha: 123456

**Alunos de Exemplo:**
- Email: joao@aluno.com / Senha: 123456
- Email: maria@aluno.com / Senha: 123456
- Email: pedro@aluno.com / Senha: 123456
- Email: ana@aluno.com / Senha: 123456
- Email: carlos@aluno.com / Senha: 123456

## 📊 Funcionalidades Implementadas

### ✅ Concluídas

#### Sistema Base
- ✅ Sistema de autenticação (professor/aluno) com sessões
- ✅ Dashboard do professor com métricas
- ✅ Gestão completa de alunos
- ✅ Interface responsiva e moderna
- ✅ Banco de dados estruturado
- ✅ API REST completa
- ✅ Deploy em produção

#### Novas Funcionalidades (v2.0)
- ✅ **Sistema de Avaliação e Feedback**
  - Avaliação de entregas com notas (0-10)
  - Feedback textual do professor
  - Registro de quem avaliou e quando
  - Estatísticas de entregas avaliadas

- ✅ **Sistema de Upload de Arquivos**
  - Upload de arquivos para entregas
  - Suporte a múltiplos formatos (PDF, DOC, imagens, vídeos, etc.)
  - Armazenamento seguro em static/uploads
  - Validação de tipos de arquivo

- ✅ **Atividades de Múltipla Escolha**
  - Criação de questões pelo professor
  - Opções configuráveis (A, B, C, D, E)
  - Correção automática
  - Sistema de pontuação
  - Estatísticas de desempenho

- ✅ **Criação Automática de Entregas**
  - Entregas automáticas para atividades individuais
  - Entregas automáticas para atividades de múltipla escolha
  - Criação automática para novos alunos

- ✅ **Sistema de Follow-Up Integrado**
  - Autenticação via sessão (substituiu headers)
  - Decoradores @login_required e @professor_required
  - Registro de atividades realizadas pelos alunos
  - Acompanhamento pelo professor

- ✅ **Sistema de Notificações**
  - Notificações para criação de atividades
  - Notificações para entregas realizadas
  - Notificações para avaliações concluídas
  - Sistema de leitura/não lida
  - Limpeza automática de notificações antigas

## 🔒 Segurança e Autenticação

- **Autenticação por Sessão**: Sistema seguro com Flask sessions
- **Decoradores de Segurança**: @login_required, @professor_required
- **Senhas Criptografadas**: Werkzeug para hash de senhas
- **Validação de Dados**: Frontend e backend
- **Controle de Acesso**: Por tipo de usuário
- **CORS Configurado**: Para comunicação frontend/backend

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- Desktop (1920px+)
- Tablet (768px - 1024px)
- Mobile (320px - 767px)

## 🎨 Design e Interface

O sistema utiliza uma interface moderna e intuitiva com:
- **Design responsivo** para desktop e mobile
- **Cores temáticas** do SENAC
- **Navegação intuitiva** com sidebar
- **Cards informativos** no dashboard
- **Tabelas interativas** para gestão de dados
- **Formulários otimizados** para entrada de dados

## 📈 Métricas do Dashboard

O dashboard do professor apresenta:
- Total de alunos cadastrados
- Atividades ativas por tipo
- Grupos formados
- Taxa de entrega geral
- Entregas avaliadas vs não avaliadas
- Nota média das entregas
- Gráficos de status das entregas
- Top alunos por entregas
- Atividades próximas do prazo
- Notificações não lidas

## 🔄 API Endpoints

### Autenticação
- `POST /api/auth/login` - Login de usuário
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Dados do usuário atual

### Atividades
- `GET /api/atividades/` - Listar atividades
- `POST /api/atividades/` - Criar atividade (professor)
- `PUT /api/atividades/{id}` - Atualizar atividade
- `DELETE /api/atividades/{id}` - Remover atividade

### Entregas
- `GET /api/entregas/` - Listar entregas
- `POST /api/entregas/` - Criar entrega
- `PUT /api/entregas/{id}/avaliar` - Avaliar entrega (professor)
- `POST /api/entregas/upload` - Upload de arquivo
- `GET /api/entregas/estatisticas` - Estatísticas (professor)

### Múltipla Escolha
- `GET /api/atividade/{id}/questoes` - Listar questões
- `POST /api/atividade/{id}/questoes` - Criar questão (professor)
- `PUT /api/questoes/{id}` - Atualizar questão (professor)
- `POST /api/atividade/{id}/responder` - Responder questões (aluno)
- `GET /api/atividade/{id}/estatisticas` - Estatísticas (professor)

### Follow-Up
- `POST /api/followups` - Criar follow-up (aluno)
- `GET /api/followups/me` - Meus follow-ups (aluno)
- `GET /api/admin/followups` - Listar follow-ups (professor)
- `PUT /api/admin/followups/{id}/revisar` - Marcar como revisado (professor)

### Notificações
- `GET /api/notificacoes` - Listar notificações
- `PUT /api/notificacoes/{id}/marcar-lida` - Marcar como lida
- `PUT /api/notificacoes/marcar-todas-lidas` - Marcar todas como lidas
- `POST /api/admin/notificacoes/enviar` - Enviar notificação (professor)

### Alunos
- `GET /api/alunos/` - Listar alunos
- `POST /api/alunos/` - Criar aluno (professor)
- `PUT /api/alunos/{id}` - Atualizar aluno
- `DELETE /api/alunos/{id}` - Remover aluno

## 🤝 Contribuição

Este projeto foi desenvolvido para a turma 321530 do SENAC como sistema de gestão educacional.

### Estrutura de Arquivos
```
AtivFlow/
├── backend/
│   ├── src/
│   │   ├── models/          # Modelos do banco de dados
│   │   ├── routes/          # Rotas da API
│   │   ├── utils/           # Utilitários e decoradores
│   │   ├── static/uploads/  # Arquivos enviados
│   │   └── main.py          # Arquivo principal
│   └── requirements.txt     # Dependências Python
├── frontend/                # Aplicação React
└── README.md               # Documentação
```

## 📄 Licença

Projeto desenvolvido para fins educacionais - SENAC 2025

**AtivFlow v2.0** - Sistema completo de gestão educacional! 📚✨

---

## 🆕 Changelog v2.0

### Novas Funcionalidades
1. **Sistema de Avaliação**: Professores podem avaliar entregas com notas e feedback
2. **Upload de Arquivos**: Alunos podem enviar arquivos nas entregas
3. **Múltipla Escolha**: Atividades com questões e correção automática
4. **Criação Automática**: Entregas geradas automaticamente para atividades individuais
5. **Follow-Up Integrado**: Sistema de acompanhamento com autenticação real
6. **Notificações**: Sistema completo de notificações em tempo real

### Melhorias Técnicas
- Autenticação por sessão substituindo headers
- Decoradores de segurança @login_required e @professor_required
- Validação robusta de dados
- Sistema de logs para notificações
- Estrutura modular com utilitários
- Documentação completa da API
