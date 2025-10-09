# Instruções de Deploy - AtivFlow

## 📋 Resumo das Alterações Implementadas

### ✅ Funcionalidades Implementadas

1. **Aba do Professor Completa**
   - Criação de atividades com todos os campos (título, descrição, formato, prazo, critérios)
   - Listagem de atividades do professor
   - Edição e exclusão de atividades
   - Visualização de entregas por atividade
   - Avaliação de entregas com feedback
   - Dashboard com estatísticas

2. **Sistema de Autenticação Corrigido**
   - Login com email e senha (validação com hash)
   - Registro de novos usuários (professores e alunos)
   - Verificação de senha com werkzeug.security
   - Sessões seguras com Flask

3. **Modelos de Banco de Dados Atualizados**
   - Professor: adicionado `created_at`, métodos `set_senha()` e `verificar_senha()`
   - Aluno: adicionado `status`, `created_at`, método `to_dict()`
   - Atividade: adicionado `titulo`, `formato`, `criterios_avaliacao`, `professor_id`, `updated_at`
   - Relacionamentos: Professor → Atividades, Aluno → Entregas

4. **Integração Professor ↔ Aluno**
   - Atividades criadas pelo professor aparecem automaticamente para alunos
   - Entregas automáticas criadas quando atividade individual é publicada
   - Status de entregas: pendente, entregue, atrasado, revisado

## 🚀 Deploy no Render

### Passo 1: Preparar Repositório GitHub

```bash
# No seu ambiente local
cd ~/AtivFlow

# Adicionar todas as alterações
git add .

# Commit das mudanças
git commit -m "feat: Implementar aba do Professor e corrigir autenticação

- Adicionar rotas completas para gestão de atividades
- Corrigir sistema de autenticação com validação de senha
- Atualizar modelos de banco de dados
- Adicionar relacionamentos entre Professor, Atividade e Entrega
- Implementar dashboard do professor com estatísticas
- Migrar para PostgreSQL (psycopg2-binary)"

# Push para GitHub
git push origin main
```

### Passo 2: Configurar Banco de Dados PostgreSQL no Render

1. Acesse o [Dashboard do Render](https://dashboard.render.com)
2. Vá até o banco PostgreSQL existente: `dpg-d3hbnbjipnbc73d3qaig-a`
3. Copie a **Internal Database URL** (formato: `postgresql://user:pass@host/dbname`)

### Passo 3: Configurar Variáveis de Ambiente no Render

No serviço web do AtivFlow no Render, configure:

```
DATABASE_URL=postgresql://user:pass@host/dbname
SECRET_KEY=ativflow-senac-321530-secret-key-production
FLASK_ENV=production
```

### Passo 4: Atualizar Configuração do Render

Certifique-se que o arquivo `render.yaml` está correto:

```yaml
services:
  - type: web
    name: ativflow
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn -w 4 -b 0.0.0.0:$PORT src.main:app
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.0
```

### Passo 5: Inicializar Banco de Dados

Após o deploy, acesse a URL da aplicação e execute:

```
https://ativflow.onrender.com/init-db
```

Isso criará todas as tabelas no PostgreSQL.

Em seguida, inicialize os dados de exemplo:

```
https://ativflow.onrender.com/init-dados
```

### Passo 6: Migrar Dados Existentes (Opcional)

Se você já tem dados no banco antigo e quer migrá-los:

```bash
# No servidor Render, via SSH ou Shell
cd /opt/render/project/src/backend
python -m src.migrate_db --migrate
```

## 🔐 Credenciais Padrão

Após inicialização:

**Professor:**
- Email: `professor@senac.com`
- Senha: `123456`

**Alunos:**
- Email: `joao@aluno.com` | Senha: `123456`
- Email: `maria@aluno.com` | Senha: `123456`
- Email: `pedro@aluno.com` | Senha: `123456`
- Email: `ana@aluno.com` | Senha: `123456`
- Email: `carlos@aluno.com` | Senha: `123456`

## 📡 Rotas da API

### Autenticação

```
POST /api/auth/login
POST /api/auth/register
POST /api/auth/logout
GET  /api/auth/me
```

### Professor

```
GET    /api/professor/atividades
POST   /api/professor/atividades
GET    /api/professor/atividades/<id>
PUT    /api/professor/atividades/<id>
DELETE /api/professor/atividades/<id>
GET    /api/professor/atividades/<id>/entregas
GET    /api/professor/entregas/<id>
POST   /api/professor/entregas/<id>/avaliar
GET    /api/professor/dashboard
```

### Alunos

```
GET  /api/alunos
POST /api/alunos
GET  /api/alunos/<id>
PUT  /api/alunos/<id>
DELETE /api/alunos/<id>
```

### Atividades e Entregas

```
GET  /api/atividades
GET  /api/entregas
POST /api/entregas
```

## 🧪 Testar Localmente

```bash
cd backend

# Instalar dependências
pip install -r requirements.txt

# Configurar variável de ambiente (opcional, usa SQLite se não definir)
export DATABASE_URL=postgresql://user:pass@localhost/ativflow

# Iniciar servidor
FLASK_APP=src.main flask run

# Ou com Python direto
python -m flask --app src.main run
```

Acesse: `http://localhost:5000`

## 📝 Exemplo de Uso da API

### 1. Login do Professor

```bash
curl -X POST https://ativflow.onrender.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "professor@senac.com",
    "senha": "123456",
    "tipo_usuario": "professor"
  }'
```

### 2. Criar Nova Atividade

```bash
curl -X POST https://ativflow.onrender.com/api/professor/atividades \
  -H "Content-Type: application/json" \
  -H "Cookie: session=..." \
  -d '{
    "titulo": "Trabalho de Python",
    "descricao": "Desenvolver um sistema CRUD com Flask",
    "formato": "upload",
    "tipo": "individual",
    "prazo_entrega": "2025-11-15T23:59:59",
    "criterios_avaliacao": "Código limpo, documentação e funcionalidade"
  }'
```

### 3. Listar Atividades

```bash
curl -X GET https://ativflow.onrender.com/api/professor/atividades \
  -H "Cookie: session=..."
```

### 4. Ver Dashboard

```bash
curl -X GET https://ativflow.onrender.com/api/professor/dashboard \
  -H "Cookie: session=..."
```

## 🔧 Troubleshooting

### Erro: "Acesso negado. Apenas professores podem acessar esta rota"

**Solução:** Certifique-se de fazer login como professor antes de acessar rotas `/api/professor/*`

### Erro: "Professor não encontrado"

**Solução:** Execute `/init-dados` para criar o professor padrão

### Erro: "NOT NULL constraint failed"

**Solução:** Execute a migração do banco:
```bash
python -m src.migrate_db --migrate
```

### Erro: "Port 5000 is in use"

**Solução:** Mate o processo existente:
```bash
ps aux | grep flask | awk '{print $2}' | xargs kill
```

## 📊 Estrutura do Banco de Dados

### Tabela: professores
```sql
id              INTEGER PRIMARY KEY
nome            VARCHAR(100) NOT NULL
email           VARCHAR(120) UNIQUE NOT NULL
senha           VARCHAR(200) NOT NULL
created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### Tabela: alunos
```sql
id              INTEGER PRIMARY KEY
nome            VARCHAR(100) NOT NULL
email           VARCHAR(120) UNIQUE NOT NULL
turma           VARCHAR(20) NOT NULL
senha           VARCHAR(200) NOT NULL
senha_definida  BOOLEAN DEFAULT FALSE
status          VARCHAR(20) DEFAULT 'ativo'
created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### Tabela: atividades
```sql
id                      INTEGER PRIMARY KEY
titulo                  VARCHAR(200) NOT NULL
descricao               TEXT NOT NULL
formato                 VARCHAR(50) NOT NULL
prazo_entrega           TIMESTAMP NOT NULL
tipo                    VARCHAR(20) NOT NULL
status                  VARCHAR(20) DEFAULT 'ativa'
criterios_avaliacao     TEXT
professor_id            INTEGER REFERENCES professores(id) NOT NULL
created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

### Tabela: entregas
```sql
id                      INTEGER PRIMARY KEY
aluno_id                INTEGER REFERENCES alunos(id) NOT NULL
atividade_id            INTEGER REFERENCES atividades(id) NOT NULL
data_entrega            TIMESTAMP DEFAULT CURRENT_TIMESTAMP
entregue                BOOLEAN DEFAULT FALSE
justificativa           TEXT
status                  VARCHAR(20) DEFAULT 'pendente'
funcao_responsabilidade VARCHAR(200)
created_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
updated_at              TIMESTAMP DEFAULT CURRENT_TIMESTAMP
```

## ✅ Checklist de Deploy

- [ ] Código commitado e pushed para GitHub
- [ ] Variáveis de ambiente configuradas no Render
- [ ] DATABASE_URL apontando para PostgreSQL do Render
- [ ] Deploy automático ativado no Render
- [ ] Aguardar build e deploy completar
- [ ] Acessar `/init-db` para criar tabelas
- [ ] Acessar `/init-dados` para popular dados iniciais
- [ ] Testar login do professor
- [ ] Testar criação de atividade
- [ ] Testar login do aluno
- [ ] Verificar dashboard do professor

## 📞 Suporte

Em caso de dúvidas ou problemas:
- GitHub: https://github.com/SamukaVenatto/AtivFlow
- Issues: https://github.com/SamukaVenatto/AtivFlow/issues

---

**Desenvolvido por Samuka Venatto**
**AtivFlow - Sistema ERP Acadêmico**
