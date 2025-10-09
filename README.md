
## 📚 Sobre o Projeto

O **AtivFlow** é um sistema ERP educacional desenvolvido especificamente para a gestão de atividades escolares da turma 321530 do SENAC. O sistema permite o controle completo de entregas de atividades, formação de grupos, acompanhamento de desempenho e geração de relatórios detalhados.

## 🚀 Funcionalidades Principais

### Para Professores
- **Dashboard Administrativo**: Visão geral completa da turma
- **Gestão de Alunos**: Cadastro, edição e controle de status dos alunos
- **Gestão de Atividades**: Criação e acompanhamento de atividades individuais e em grupo
- **Gestão de Grupos**: Formação e monitoramento de grupos de trabalho
- **Relatórios Detalhados**: Análises de desempenho e exportação de dados
- **Sistema de Notificações**: Alertas sobre prazos e entregas

### Para Alunos
- **Dashboard Pessoal**: Visão das atividades pendentes e entregues
- **Gestão de Entregas**: Controle de atividades individuais
- **Participação em Grupos**: Visualização e interação com grupos
- **Histórico de Atividades**: Acompanhamento do próprio desempenho

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask** (Python) - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados
- **Flask-CORS** - Controle de CORS
- **Werkzeug** - Utilitários de segurança

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
   - id, descricao, prazo_entrega, tipo, status, created_at
