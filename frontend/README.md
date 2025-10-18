# AtivFlow - Frontend

Frontend do sistema AtivFlow desenvolvido com React + Vite, Tailwind CSS e React Router.

## Tecnologias

- **React 19** - Biblioteca para construção de interfaces
- **Vite** - Build tool e dev server
- **React Router** - Roteamento
- **Axios** - Cliente HTTP
- **Tailwind CSS** - Framework CSS utilitário

## Estrutura de Diretórios

```
src/
├── components/       # Componentes reutilizáveis
│   ├── auth/        # Componentes de autenticação
│   ├── aluno/       # Componentes específicos do aluno
│   ├── professor/   # Componentes específicos do professor
│   └── common/      # Componentes comuns
├── contexts/        # Contextos React (AuthContext, etc)
├── pages/           # Páginas da aplicação
│   ├── auth/        # Páginas de autenticação
│   ├── aluno/       # Páginas do aluno
│   └── professor/   # Páginas do professor
├── services/        # Serviços de API
├── utils/           # Utilitários
└── index.css        # Estilos globais com Tailwind
```

## Instalação

```bash
# Instalar dependências
pnpm install

# Copiar arquivo de ambiente
cp .env.example .env

# Editar .env com a URL da API
```

## Executar em Desenvolvimento

```bash
pnpm dev
```

A aplicação estará disponível em `http://localhost:5173`

## Build para Produção

```bash
pnpm build
```

Os arquivos de produção serão gerados na pasta `dist/`

## Variáveis de Ambiente

- `VITE_API_URL` - URL da API do backend (padrão: http://localhost:5000/api)

## Credenciais de Teste

### Professor
- Email: maria.santos@senac.edu.br
- Senha: Prof@123

### Aluno
- Email: samuel.ribeiro@adm321530.com
- Senha: Aluno@123

