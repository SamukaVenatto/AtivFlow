# Guia Rápido - AtivFlow

## 🎯 Para Professores

### 1. Fazer Login
```
URL: https://ativflow.onrender.com
Email: professor@senac.com
Senha: 123456
Tipo: Professor
```

### 2. Criar Atividade

**Campos obrigatórios:**
- **Título**: Nome da atividade (ex: "Trabalho de Python")
- **Descrição**: Detalhes da atividade
- **Formato**: `texto`, `upload` ou `multipla_escolha`
- **Tipo**: `individual` ou `grupo`
- **Prazo**: Data e hora limite (formato ISO: `2025-11-15T23:59:59`)

**Campos opcionais:**
- **Critérios de Avaliação**: Como será avaliado

### 3. Gerenciar Atividades

- **Ver todas**: Dashboard → Atividades
- **Editar**: Clicar na atividade → Editar
- **Excluir**: Clicar na atividade → Excluir
- **Ver entregas**: Clicar na atividade → Entregas

### 4. Avaliar Entregas

1. Acessar atividade
2. Ver lista de entregas
3. Clicar em entrega específica
4. Adicionar feedback
5. Marcar status: `revisado`, `aprovado` ou `reprovado`

### 5. Dashboard

**Métricas disponíveis:**
- Total de atividades criadas
- Atividades ativas
- Total de entregas
- Entregas pendentes
- Taxa de entrega (%)
- Atividades próximas do prazo

---

## 👨‍🎓 Para Alunos

### 1. Fazer Login
```
URL: https://ativflow.onrender.com
Email: seuemail@aluno.com
Senha: sua_senha
Tipo: Aluno
```

### 2. Ver Atividades

- Dashboard mostra todas as atividades disponíveis
- Filtrar por: pendentes, entregues, atrasadas

### 3. Fazer Entrega

1. Acessar atividade
2. Preencher resposta (conforme formato)
3. Adicionar justificativa (opcional)
4. Enviar

### 4. Acompanhar Status

- **Pendente**: Ainda não entregue
- **Entregue**: Enviada, aguardando avaliação
- **Atrasado**: Prazo vencido
- **Revisado**: Avaliada pelo professor

---

## 🔐 Gerenciar Conta

### Alterar Senha

```bash
POST /api/auth/alterar-senha
{
  "email": "seu@email.com",
  "senha_atual": "senha_antiga",
  "nova_senha": "senha_nova"
}
```

### Primeiro Acesso (Aluno)

Se você foi cadastrado pelo professor:

1. Acesse `/primeiro-acesso`
2. Digite seu email
3. Defina sua senha
4. Faça login normalmente

---

## 📱 Formatos de Atividade

### Texto
- Aluno digita resposta em campo de texto
- Ideal para: respostas curtas, dissertações

### Upload
- Aluno envia arquivo
- Ideal para: trabalhos, projetos, documentos

### Múltipla Escolha
- Aluno seleciona opções
- Ideal para: questionários, testes

---

## ⏰ Prazos e Status

### Status Automáticos

- **Pendente**: Criada, aguardando entrega
- **Entregue**: Aluno enviou dentro do prazo
- **Atrasado**: Prazo vencido sem entrega
- **Revisado**: Professor avaliou

### Notificações

- Atividades próximas do prazo aparecem no dashboard
- Próximos 7 dias são destacados

---

## 🆘 Problemas Comuns

### "Acesso negado"
**Causa**: Tentando acessar área do professor como aluno (ou vice-versa)
**Solução**: Fazer logout e login com tipo correto

### "Senha incorreta"
**Causa**: Senha digitada errada
**Solução**: Verificar caps lock, tentar novamente

### "Atividade não encontrada"
**Causa**: Atividade foi excluída ou você não tem permissão
**Solução**: Atualizar página, verificar com professor

### "Não autenticado"
**Causa**: Sessão expirou
**Solução**: Fazer login novamente

---

## 📞 Suporte

**Problemas técnicos:**
- GitHub Issues: https://github.com/SamukaVenatto/AtivFlow/issues

**Dúvidas sobre uso:**
- Contate o administrador do sistema
- Email: (configurar email de suporte)

---

## 🔄 Fluxo Completo

```
1. Professor cria atividade
   ↓
2. Sistema cria entregas automáticas para alunos (se individual)
   ↓
3. Alunos veem atividade no dashboard
   ↓
4. Alunos fazem entrega
   ↓
5. Professor visualiza entregas
   ↓
6. Professor avalia e dá feedback
   ↓
7. Alunos veem feedback
```

---

## 💡 Dicas

### Para Professores
- Defina critérios de avaliação claros
- Use prazos realistas
- Dê feedback construtivo
- Monitore taxa de entrega

### Para Alunos
- Verifique prazos regularmente
- Entregue com antecedência
- Leia critérios de avaliação
- Justifique atrasos quando necessário

---

**AtivFlow - Sistema ERP Acadêmico**
**Versão 2.0.0**
