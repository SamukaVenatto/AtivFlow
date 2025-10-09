# Changelog - AtivFlow

## [2.0.0] - 2025-10-06

### ✨ Novas Funcionalidades

#### Aba do Professor
- **Gestão Completa de Atividades**
  - Criar atividades com título, descrição, formato, prazo e critérios de avaliação
  - Listar todas as atividades do professor
  - Editar atividades existentes
  - Excluir atividades
  - Filtrar por status (ativa/inativa)

- **Controle de Entregas**
  - Visualizar todas as entregas de uma atividade
  - Ver detalhes de cada entrega individual
  - Avaliar entregas com feedback
  - Acompanhar status (pendente, entregue, atrasado, revisado)

- **Dashboard do Professor**
  - Total de atividades criadas
  - Atividades ativas
  - Total de entregas
  - Entregas pendentes e entregues
  - Taxa de entrega (%)
  - Atividades próximas do prazo (próximos 7 dias)

#### Sistema de Autenticação
- **Login Seguro**
  - Validação de email e senha
  - Hash de senha com werkzeug.security
  - Sessões persistentes com Flask
  - Diferenciação entre professor e aluno

- **Registro de Usuários**
  - Cadastro de novos professores
  - Cadastro de novos alunos
  - Validação de email único
  - Senha hasheada automaticamente

### 🔧 Correções

#### Modelos de Banco de Dados
- **Professor**
  - Adicionado campo `created_at`
  - Adicionado método `set_senha()`
  - Adicionado método `verificar_senha()`
  - Adicionado método `to_dict()`
  - Adicionado relacionamento com Atividades

- **Aluno**
  - Adicionado campo `status` (ativo/inativo)
  - Adicionado campo `created_at`
  - Adicionado método `to_dict()`
  - Adicionado relacionamento com Entregas

- **Atividade**
  - Adicionado campo `titulo` (obrigatório)
  - Adicionado campo `formato` (texto, upload, multipla_escolha)
  - Adicionado campo `criterios_avaliacao`
  - Adicionado campo `professor_id` (foreign key)
  - Adicionado campo `updated_at`
  - Corrigido relacionamento com Professor
  - Adicionado cascade delete para Entregas

- **Entrega**
  - Adicionado campo `updated_at`
  - Mantido relacionamento com Aluno e Atividade

#### Rotas de Autenticação
- Corrigido login sem validação de senha
- Removido criação automática de professor no login
- Adicionado validação de credenciais
- Adicionado mensagens de erro específicas

#### Integração
- Criação automática de entregas para alunos quando atividade individual é publicada
- Verificação automática de atraso baseada no prazo
- Sincronização entre professor e alunos

### 🗄️ Banco de Dados

#### Migração para PostgreSQL
- Adicionado suporte a PostgreSQL com `psycopg2-binary`
- Mantido compatibilidade com SQLite para desenvolvimento local
- Script de migração automática (`migrate_db.py`)
- Rotas de inicialização: `/init-db` e `/init-dados`

#### Novos Campos
```sql
-- professores
ALTER TABLE professores ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- alunos
ALTER TABLE alunos ADD COLUMN status VARCHAR(20) DEFAULT 'ativo';
ALTER TABLE alunos ADD COLUMN senha_definida BOOLEAN DEFAULT FALSE;
ALTER TABLE alunos ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- atividades
ALTER TABLE atividades ADD COLUMN titulo VARCHAR(200) NOT NULL;
ALTER TABLE atividades ADD COLUMN formato VARCHAR(50) NOT NULL;
ALTER TABLE atividades ADD COLUMN criterios_avaliacao TEXT;
ALTER TABLE atividades ADD COLUMN professor_id INTEGER REFERENCES professores(id) NOT NULL;
ALTER TABLE atividades ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;

-- entregas
ALTER TABLE entregas ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;
```

### 📡 Novas Rotas da API

#### Professor (`/api/professor`)
- `GET /atividades` - Listar atividades do professor
- `POST /atividades` - Criar nova atividade
- `GET /atividades/<id>` - Obter detalhes de uma atividade
- `PUT /atividades/<id>` - Editar atividade
- `DELETE /atividades/<id>` - Deletar atividade
- `GET /atividades/<id>/entregas` - Listar entregas de uma atividade
- `GET /entregas/<id>` - Visualizar entrega específica
- `POST /entregas/<id>/avaliar` - Avaliar entrega
- `GET /dashboard` - Dashboard com estatísticas

#### Autenticação (`/api/auth`)
- `POST /register` - Registrar novo usuário

### 🔒 Segurança

- Implementado middleware de verificação de professor
- Validação de propriedade de atividades (professor só acessa suas próprias)
- Hash de senhas com PBKDF2-SHA256
- Sessões seguras com secret key
- Validação de campos obrigatórios em todas as rotas

### 📦 Dependências

#### Adicionadas
- `psycopg2-binary==2.9.10` - Driver PostgreSQL
- `gunicorn==23.0.0` - Servidor WSGI para produção

### 🐛 Bugs Corrigidos

1. **Login sem senha** - Sistema permitia login apenas com email
2. **Acesso negado ao professor** - Faltava validação de sessão
3. **Erro ao criar atividade** - Campos obrigatórios faltando
4. **Import error timedelta** - Corrigido import no professor.py
5. **Inicialização do banco** - Corrigido dados de exemplo

### 📝 Documentação

- Adicionado `DEPLOY_INSTRUCTIONS.md` com guia completo de deploy
- Adicionado `CHANGELOG.md` com histórico de alterações
- Atualizado README.md com novas funcionalidades
- Documentado todas as rotas da API
- Exemplos de uso com curl

### 🧪 Testes

- Testado login de professor com senha
- Testado login de aluno com senha
- Testado criação de atividade
- Testado listagem de atividades
- Testado dashboard do professor
- Testado integração professor-aluno

### ⚠️ Breaking Changes

1. **Autenticação obrigatória com senha**
   - Antes: Login apenas com email
   - Agora: Login requer email + senha

2. **Campo `titulo` obrigatório em Atividades**
   - Antes: Apenas `descricao`
   - Agora: `titulo` e `descricao` obrigatórios

3. **Campo `professor_id` obrigatório em Atividades**
   - Todas as atividades devem estar associadas a um professor

### 🔄 Migração de Dados Existentes

Para migrar dados existentes:

```bash
# 1. Backup do banco atual
pg_dump $DATABASE_URL > backup.sql

# 2. Executar migração
python -m src.migrate_db --migrate

# 3. Atualizar senhas dos usuários existentes
# (necessário recriar senhas pois agora são hasheadas)
```

### 📊 Estatísticas

- **Arquivos modificados**: 8
- **Arquivos criados**: 3
- **Linhas de código adicionadas**: ~800
- **Rotas API adicionadas**: 9
- **Modelos atualizados**: 4

---

## [1.0.0] - 2025-09-XX

### Versão Inicial
- Sistema básico de gestão de alunos
- Dashboard administrativo
- Gestão de grupos
- Interface React com Tailwind CSS
