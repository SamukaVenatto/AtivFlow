# 🚀 Guia Completo: Upload AtivFlow para GitHub

## 📦 **O que você recebeu:**

✅ **AtivFlow Completo e Corrigido** com todas as funcionalidades:
- Sistema de gestão de alunos funcionando
- Página de atividades do professor COMPLETA
- Banco de dados corrigido (coluna status)
- APIs funcionais para todas as operações
- Interface moderna e responsiva

## 💻 **Passo a Passo no Terminal:**

### **1. Extrair o ZIP**
- Extraia o arquivo `ativflow-completo-corrigido.zip`
- Você terá uma pasta `ativflow` com tudo dentro

### **2. Abrir Terminal**
- Navegue até a pasta `ativflow` no Windows Explorer
- **Clique com botão direito** → **"Abrir no Terminal"** ou **"Git Bash here"**

### **3. Comandos para Executar:**

```bash
# Configurar Git (primeira vez)
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"

# Inicializar repositório
git init
git branch -M main

# Adicionar todos os arquivos
git add .

# Fazer commit
git commit -m "AtivFlow - Sistema completo com todas as correções"

# Conectar com GitHub (substitua SEU_USUARIO)
git remote add origin https://github.com/SEU_USUARIO/ativflow-senac.git

# Fazer upload
git push -u origin main
```

## 🔑 **Autenticação GitHub:**

Quando pedir login:
- **Username:** Seu usuário do GitHub
- **Password:** Use **Personal Access Token** (não a senha normal)

### **Criar Personal Access Token:**
1. GitHub.com → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. Marque: `repo`, `workflow`, `write:packages`
5. Copie o token e use como senha

## ✅ **Verificar se Funcionou:**

Após o upload:
1. Vá no seu repositório GitHub
2. Verifique se todos os arquivos estão lá
3. Deve ter as pastas: `backend`, `frontend`
4. Deve ter os arquivos: `README.md`, `requirements.txt`, etc.

## 🌐 **Deploy Automático no Render:**

Após o upload no GitHub:
1. Vá para **render.com**
2. Crie um **Web Service**
3. Conecte seu repositório
4. Configure:
   - **Build Command:** `./build.sh`
   - **Start Command:** `cd backend && python src/main.py`
5. Aguarde o deploy (5-10 minutos)
6. Receba sua **URL permanente**!

## 🎯 **Funcionalidades Que Vão Funcionar:**

### **Professor:**
- ✅ Login com `professor@senac.com` / `123456`
- ✅ Dashboard com estatísticas
- ✅ Gestão completa de alunos
- ✅ **Gestão completa de atividades** (NOVO!)
- ✅ Criar, editar, excluir atividades
- ✅ Buscar e filtrar atividades

### **Alunos:**
- ✅ Login com credenciais individuais
- ✅ Dashboard personalizado
- ✅ Visualização de atividades

## 🆘 **Se Precisar de Ajuda:**

- **Erro de autenticação:** Use Personal Access Token
- **Erro "repository not found":** Verifique o nome do repositório
- **Problemas no deploy:** Verifique os logs no Render

---

**🎉 Seu AtivFlow está pronto para ser o sistema oficial da turma 321530!**
