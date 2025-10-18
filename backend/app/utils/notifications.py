"""
Utilitário para criação de notificações automáticas
"""
from datetime import datetime, timedelta
from app import db
from app.models.notificacao import Notificacao
from app.models.usuario import Usuario

def criar_notificacao(usuario_id, titulo, mensagem, tipo='info'):
    """
    Cria uma notificação para um usuário específico.
    """
    notificacao = Notificacao(
        usuario_id=usuario_id,
        titulo=titulo,
        mensagem=mensagem,
        tipo=tipo
    )
    db.session.add(notificacao)
    db.session.commit()
    return notificacao

def criar_notificacao_global(titulo, mensagem, tipo='info'):
    """
    Cria uma notificação global (para todos os usuários).
    """
    notificacao = Notificacao(
        usuario_id=None,
        titulo=titulo,
        mensagem=mensagem,
        tipo=tipo
    )
    db.session.add(notificacao)
    db.session.commit()
    return notificacao

def notificar_turma(turma, titulo, mensagem, tipo='info'):
    """
    Cria notificações para todos os alunos de uma turma.
    """
    alunos = Usuario.query.filter_by(turma=turma, tipo='aluno', status='ativo').all()
    
    for aluno in alunos:
        criar_notificacao(aluno.id, titulo, mensagem, tipo)

def notificar_nova_atividade(atividade):
    """
    Notifica alunos sobre uma nova atividade criada.
    """
    titulo = f"Nova atividade: {atividade.titulo}"
    mensagem = f"Uma nova atividade foi criada. Prazo: {atividade.prazo.strftime('%d/%m/%Y %H:%M')}"
    
    if atividade.turma:
        notificar_turma(atividade.turma, titulo, mensagem, tipo='info')

def notificar_entrega_recebida(entrega, professor_id):
    """
    Notifica o professor sobre uma nova entrega.
    """
    titulo = "Nova entrega recebida"
    mensagem = f"Uma nova entrega foi enviada para a atividade '{entrega.atividade.titulo}'"
    criar_notificacao(professor_id, titulo, mensagem, tipo='info')

def notificar_avaliacao_concluida(entrega):
    """
    Notifica o aluno ou grupo sobre avaliação concluída.
    """
    titulo = "Atividade avaliada"
    mensagem = f"Sua entrega da atividade '{entrega.atividade.titulo}' foi avaliada. Nota: {entrega.nota}"
    
    if entrega.aluno_id:
        criar_notificacao(entrega.aluno_id, titulo, mensagem, tipo='info')
    elif entrega.grupo_id:
        # Notificar todos os membros do grupo
        for membro in entrega.grupo.membros:
            criar_notificacao(membro.aluno_id, titulo, mensagem, tipo='info')

def notificar_prazo_proximo(atividade):
    """
    Notifica alunos sobre prazo próximo (48h).
    """
    titulo = f"Prazo próximo: {atividade.titulo}"
    mensagem = f"Atenção! O prazo da atividade '{atividade.titulo}' termina em {atividade.prazo.strftime('%d/%m/%Y %H:%M')}"
    
    if atividade.turma:
        notificar_turma(atividade.turma, titulo, mensagem, tipo='prazo')

def verificar_prazos_proximos():
    """
    Verifica atividades com prazo próximo (48h) e cria notificações.
    Esta função deve ser executada periodicamente (cron/scheduler).
    """
    from app.models.atividade import Atividade
    
    agora = datetime.utcnow()
    limite = agora + timedelta(hours=48)
    
    # Buscar atividades com prazo nas próximas 48h
    atividades = Atividade.query.filter(
        Atividade.prazo >= agora,
        Atividade.prazo <= limite,
        Atividade.ativo == True
    ).all()
    
    for atividade in atividades:
        # Verificar se já foi enviada notificação (evitar duplicatas)
        # Aqui poderíamos adicionar uma flag na atividade ou verificar notificações existentes
        notificar_prazo_proximo(atividade)

def limpar_notificacoes_antigas(dias=30):
    """
    Remove notificações com mais de X dias.
    """
    limite = datetime.utcnow() - timedelta(days=dias)
    
    notificacoes_antigas = Notificacao.query.filter(
        Notificacao.data_envio < limite
    ).all()
    
    count = len(notificacoes_antigas)
    
    for notificacao in notificacoes_antigas:
        db.session.delete(notificacao)
    
    db.session.commit()
    
    return count

