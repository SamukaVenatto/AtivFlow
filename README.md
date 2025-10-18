# AtivFlow - Sistema de Gerenciamento de Atividades

Este é o repositório completo do sistema AtivFlow, desenvolvido para gerenciar atividades acadêmicas com funcionalidades para alunos e professores. O projeto é composto por um backend em Flask (Python) e um frontend em React (JavaScript) com Vite e Tailwind CSS.

## Arquitetura

O sistema segue uma arquitetura modular, dividida em duas principais partes:

- **`backend/`**: Aplicação Flask em Python, responsável pela lógica de negócio, persistência de dados (SQLAlchemy), autenticação via sessão HTTPOnly, gerenciamento de arquivos e geração de relatórios.
- **`frontend/`**: Aplicação React com Vite, que consome a API do backend para fornecer uma interface interativa e responsiva para alunos e professores.

### Tecnologias Utilizadas

**Backend:**
- Python 3.11+
- Flask (framework web)
- SQLAlchemy (ORM)
- Flask-Migrate (migrations de banco de dados)
- Flask-CORS (Cross-Origin Resource Sharing)
- Flask-Limiter (Rate Limiting)
- Werkzeug (segurança de senhas com bcrypt)
- openpyxl (geração de XLSX)
- WeasyPrint (geração de PDF)
- Pytest (testes unitários)

**Frontend:**
- React 19
- Vite (build tool)
- Tailwind CSS (framework CSS)
- React Router (roteamento)
- Axios (cliente HTTP)
- Jest / React Testing Library (testes unitários)

**Banco de Dados:**
- SQLite (para desenvolvimento)
- PostgreSQL (para produção - configurável via `DATABASE_URL`)

## Como Rodar o Projeto Localmente

Siga os passos abaixo para configurar e executar o projeto em seu ambiente de desenvolvimento.

### Pré-requisitos

- Python 3.11+
- Node.js (recomendado versão LTS)
- pnpm (gerenciador de pacotes Node.js)
- Docker e Docker Compose (para execução via contêineres)

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd AtivFlow
```

### 2. Executar com Docker Compose (Recomendado para Desenvolvimento)

Esta é a forma mais fácil de subir o ambiente completo (backend e banco de dados).

```bash
# Na raiz do projeto (pasta AtivFlow)
docker compose up --build
```

Após os contêineres subirem, você pode seguir para a configuração e execução do frontend.

### 3. Configuração e Execução Manual (Alternativa)

#### 3.1 Configurar o Backend

```bash
cd backend

# Criar ambiente virtual e ativar
python3.11 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Copiar arquivo de ambiente e configurar
cp .env.example .env
# Edite o arquivo .env conforme necessário. Por padrão, ele usará SQLite.

# Inicializar migrations do banco de dados
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Popular o banco de dados com dados de exemplo (opcional, mas recomendado para testes)
python scripts/seed.py

# Executar o backend
python run.py
# O backend estará disponível em http://localhost:5000
```

#### 3.2 Configurar o Frontend

Abra um novo terminal e siga os passos:

```bash
cd frontend

# Instalar dependências
pnpm install

# Copiar arquivo de ambiente e configurar
cp .env.example .env
# Edite o arquivo .env se o backend estiver em uma URL diferente de http://localhost:5000/api

# Executar o frontend
pnpm dev
# O frontend estará disponível em http://localhost:5173
```

### 4. Acessar o Sistema

Após iniciar o backend e o frontend (via Docker Compose ou manualmente), abra seu navegador e acesse `http://localhost:5173`.

## Variáveis de Ambiente

### Backend (`backend/.env`)

- `FLASK_ENV`: `development` ou `production`
- `DEBUG`: `True` ou `False`
- `SECRET_KEY`: Chave secreta para segurança de sessões. **Mudar em produção!**
- `DATABASE_URL`: String de conexão com o banco de dados (ex: `sqlite:///ativflow.db` ou `postgresql://user:pass@host:port/dbname`)
- `FRONTEND_URL`: URL do frontend para configuração de CORS (ex: `http://localhost:5173`)
- `STORAGE_PROVIDER`: `local` ou `s3` (para upload de arquivos)
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`, `AWS_S3_REGION`: Credenciais AWS para S3 (se `STORAGE_PROVIDER=s3`)

### Frontend (`frontend/.env`)

- `VITE_API_URL`: URL base da API do backend (ex: `http://localhost:5000/api`)

## Credenciais de Teste (após executar `python scripts/seed.py`)

### Professor
- **Email**: `maria.santos@senac.edu.br`
- **Senha**: `Prof@123`

### Aluno
- **Email**: `samuel.ribeiro@adm321530.com`
- **Senha**: `Aluno@123`

## Testes Automatizados

### Backend (Pytest)

```bash
cd backend
source venv/bin/activate
pytest
```

### Frontend (Jest / React Testing Library)

```bash
cd frontend
pnpm test
```

## Critérios de Aceite (Checklist de QA)

Para validar as principais funcionalidades do sistema, siga os passos abaixo:

1.  **Inicialização:**
    *   Verifique se o backend inicia sem erros e conecta ao banco de dados (SQLite por padrão).
    *   Verifique se o frontend inicia e está acessível em `http://localhost:5173`.

2.  **Autenticação:**
    *   Acesse `/login` e teste o login como Professor (`maria.santos@senac.edu.br` / `Prof@123`). Deve ser redirecionado para o dashboard do professor.
    *   Faça logout e teste o login como Aluno (`samuel.ribeiros@adm321530.com` / `Aluno@123`). Deve ser redirecionado para o dashboard do aluno.
    *   Tente acessar uma rota protegida sem login (ex: `/aluno/dashboard`). Deve ser redirecionado para `/login`.

3.  **Gerenciamento de Atividades (Professor):**
    *   Faça login como Professor.
    *   Crie uma nova atividade do tipo grupo, designe um líder (um aluno existente) e adicione alguns membros.
    *   Verifique se a atividade aparece na lista de atividades.
    *   Edite uma atividade existente e verifique se as alterações são salvas.
    *   Inative uma atividade e verifique se ela não aparece mais como ativa.

4.  **Fluxo do Líder (Aluno):**
    *   Faça login como o aluno designado como líder do grupo criado na etapa anterior.
    *   Acesse o painel do líder (`/aluno/lider/:grupo_id`).
    *   Simule o envio de entregas individuais por outros membros (via API ou seed de dados, se necessário).
    *   Consolide as entregas e envie ao professor.

5.  **Entregas e Avaliação (Professor/Aluno):**
    *   Faça login como Aluno.
    *   Envie uma entrega para uma atividade individual.
    *   Faça login como Professor.
    *   Acesse a entrega enviada pelo aluno e avalie-a (dê uma nota e feedback).
    *   Verifique se as notificações são geradas e visíveis para o aluno.

6.  **Múltipla Escolha:**
    *   Faça login como Aluno.
    *   Responda a uma atividade de múltipla escolha.
    *   Verifique se a correção automática funciona e a nota é calculada.
    *   Faça login como Professor e verifique as estatísticas da atividade.

7.  **Follow-Up:**
    *   Faça login como Aluno.
    *   Crie um registro de follow-up diário.
    *   Faça login como Professor.
    *   Acesse o follow-up do aluno, adicione feedback e libere a edição.
    *   Faça login como Aluno novamente e verifique se pode editar o follow-up.

8.  **Relatórios:**
    *   Faça login como Professor.
    *   Acesse a página de relatórios (`/professor/report`).
    *   Gere um relatório de desempenho em PDF e XLSX para uma turma específica.
    *   Verifique se os arquivos são baixados corretamente e contêm os dados esperados.

9.  **Testes:**
    *   Execute os testes de backend (`pytest`) e frontend (`pnpm test`) e verifique se todos passam.

## Observações Finais

-   **Segurança**: Senhas são armazenadas com hash bcrypt. Cookies de sessão são configurados com `HttpOnly`, `Secure` (em produção) e `SameSite=Strict`.
-   **Upload de Arquivos**: Em desenvolvimento, os arquivos são armazenados localmente (`backend/uploads/`). O sistema está preparado para integração com S3 em produção via variáveis de ambiente.
-   **Limpeza de Notificações**: Um script `cleanup_notifications` é previsto para remoção/arquivamento de notificações antigas, podendo ser agendado via cron ou APScheduler.
-   **Horários**: Todos os horários são tratados em UTC no backend e devem ser convertidos para o fuso horário do usuário no frontend.

