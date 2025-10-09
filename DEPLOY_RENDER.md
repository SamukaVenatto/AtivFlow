# 🚀 Guia de Deploy do AtivFlow no Render.com

## 📋 Pré-requisitos

1. **Conta no GitHub** (gratuita)
2. **Conta no Render.com** (gratuita)

## 🔧 Passo a Passo para Deploy

### 1. **Criar Repositório no GitHub**

1. Acesse [github.com](https://github.com) e faça login
2. Clique em **"New repository"**
3. Nome do repositório: `ativflow-senac`
4. Marque como **"Public"** (necessário para plano gratuito)
5. Clique em **"Create repository"**

### 2. **Fazer Upload do Código**

No terminal do seu computador, execute:

```bash
# Clonar este projeto
git clone [URL_DO_SEU_REPOSITORIO]
cd ativflow-senac

# Copiar todos os arquivos do AtivFlow para o repositório
# (copie todos os arquivos da pasta /home/ubuntu/ativflow/)

# Fazer commit e push
git add .
git commit -m "Initial commit - AtivFlow Sistema"
git push origin main
```

### 3. **Configurar Deploy no Render**

1. Acesse [render.com](https://render.com) e faça login
2. Clique em **"New +"** → **"Web Service"**
3. Conecte sua conta do GitHub
4. Selecione o repositório `ativflow-senac`
5. Configure:
   - **Name**: `ativflow-senac`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `cd backend && python src/main.py`

### 4. **Configurações Avançadas**

Na seção **"Advanced"**:
- **Auto-Deploy**: `Yes` (deploy automático)
- **Environment Variables**: Nenhuma necessária

### 5. **Aguardar Deploy**

- O processo leva **5-10 minutos**
- Acompanhe os logs em tempo real
- Quando concluído, você receberá uma **URL permanente**

## 🌐 **Resultado Final**

Após o deploy, você terá:
- **URL permanente** (ex: `https://ativflow-senac.onrender.com`)
- **HTTPS automático** (certificado SSL gratuito)
- **Deploy automático** a cada push no GitHub
- **Banco de dados persistente**

## 📊 **Limites do Plano Gratuito**

- **750 horas/mês** (suficiente para uso contínuo)
- **512MB RAM**
- **Aplicação "dorme"** após 15min sem uso
- **"Acorda"** automaticamente quando acessada

## 🔄 **Atualizações Futuras**

Para atualizar o sistema:
1. Modifique os arquivos localmente
2. Faça commit: `git add . && git commit -m "Atualização"`
3. Push: `git push origin main`
4. **Deploy automático** no Render!

## 🆘 **Solução de Problemas**

### Build falha:
- Verifique se `build.sh` tem permissão de execução
- Confirme se `requirements.txt` está correto

### Aplicação não carrega:
- Verifique logs no painel do Render
- Confirme se a porta está configurada corretamente

### Banco de dados vazio:
- O banco é criado automaticamente no primeiro acesso
- Dados de exemplo são inseridos automaticamente

## 📞 **Suporte**

Se precisar de ajuda:
1. Verifique os **logs no Render**
2. Consulte a [documentação oficial](https://render.com/docs)
3. Entre em contato para suporte adicional

---

**🎉 Parabéns! Seu AtivFlow estará online permanentemente!**
