"""
Sistema de notificações do AtivFlow
"""
from src.database_config import db
from src.models.notificacao import Notificacao
from src.models.aluno import Aluno
from src.models.professor import Professor
from datetime import datetime
import logging

# Configurar logging para notificações
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def enviar_notificacao(destinatario_id, tipo_usuario, titulo, mensagem, 
                      tipo_notificacao='info', atividade_id=None, 
                      entrega_id=None, grupo_id=None):
    """
    Envia uma notificação para um usuário
    
    Args:
        destinatario_id: ID do usuário destinatário
        tipo_usuario: 'aluno' ou 'professor'
        titulo: Título da notificação
        mensagem: Mensagem da notificação
        tipo_notificacao: 'info', 'sucesso', 'aviso', 'erro'
        atividade_id: ID da atividade relacionada (opcional)
        entrega_id: ID da entrega relacionada (opcional)
        grupo_id: ID do grupo relacionado (opcional)
    
    Returns:
        bool: True se enviado com sucesso
    """
    try:
        # Verificar se o usuário existe
        if tipo_usuario == 'aluno':
            usuario = Aluno.query.get(destinatario_id)
        elif tipo_usuario == 'professor':
            usuario = Professor.query.get(destinatario_id)
        else:
            logger.error(f"Tipo de usuário inválido: {tipo_usuario}")
            return False
        
        if not usuario:
            logger.error(f"Usuário não encontrado: {destinatario_id} ({tipo_usuario})")
            return False
        
        # Criar notificação
        notificacao = Notificacao(
            usuario_id=destinatario_id,
            tipo_usuario=tipo_usuario,
            titulo=titulo,
            mensagem=mensagem,
            tipo_notificacao=tipo_notificacao,
            atividade_id=atividade_id,
            entrega_id=entrega_id,
            grupo_id=grupo_id
        )
        
        db.session.add(notificacao)
        db.session.commit()
        
        # Log da notificação
        logger.info(f"Notificação enviada para {usuario.nome} ({tipo_usuario}): {titulo}")
        
        return True
        
    except Exception as e:
        logger.error(f"Erro ao enviar notificação: {str(e)}")
        db.session.rollback()
        return False

def enviar_notificacao_para_todos_alunos(titulo, mensagem, tipo_notificacao='info',
                                        atividade_id=None, entrega_id=None, grupo_id=None):
    """
    Envia notificação para todos os alunos ativos
    
    Args:
        titulo: Título da notificação
        mensagem: Mensagem da notificação
        tipo_notificacao: 'info', 'sucesso', 'aviso', 'erro'
        atividade_id: ID da atividade relacionada (opcional)
        entrega_id: ID da entrega relacionada (opcional)
        grupo_id: ID do grupo relacionado (opcional)
    
    Returns:
        int: Número de notificações enviadas
    """
    try:
        alunos_ativos = Aluno.query.filter_by(status='ativo').all()
        enviadas = 0
        
        for aluno in alunos_ativos:
            if enviar_notificacao(
                aluno.id, 'aluno', titulo, mensagem, 
                tipo_notificacao, atividade_id, entrega_id, grupo_id
            ):
                enviadas += 1
        
        logger.info(f"Notificação enviada para {enviadas} alunos: {titulo}")
        return enviadas
        
    except Exception as e:
        logger.error(f"Erro ao enviar notificação para todos os alunos: {str(e)}")
        return 0

def enviar_notificacao_para_todos_professores(titulo, mensagem, tipo_notificacao='info',
                                            atividade_id=None, entrega_id=None, grupo_id=None):
    """
    Envia notificação para todos os professores
    
    Args:
        titulo: Título da notificação
        mensagem: Mensagem da notificação
        tipo_notificacao: 'info', 'sucesso', 'aviso', 'erro'
        atividade_id: ID da atividade relacionada (opcional)
        entrega_id: ID da entrega relacionada (opcional)
        grupo_id: ID do grupo relacionado (opcional)
    
    Returns:
        int: Número de notificações enviadas
    """
    try:
        professores = Professor.query.all()
        enviadas = 0
        
        for professor in professores:
            if enviar_notificacao(
                professor.id, 'professor', titulo, mensagem,
                tipo_notificacao, atividade_id, entrega_id, grupo_id
            ):
                enviadas += 1
        
        logger.info(f"Notificação enviada para {enviadas} professores: {titulo}")
        return enviadas
        
    except Exception as e:
        logger.error(f"Erro ao enviar notificação para todos os professores: {str(e)}")
        return 0

def notificar_nova_atividade(atividade):
    """
    Notifica sobre criação de nova atividade
    """
    titulo = "Nova Atividade Criada"
    mensagem = f"A atividade '{atividade.descricao}' foi criada. Prazo: {atividade.prazo_entrega.strftime('%d/%m/%Y')}"
    
    return enviar_notificacao_para_todos_alunos(
        titulo, mensagem, 'info', atividade_id=atividade.id
    )

def notificar_entrega_realizada(entrega):
    """
    Notifica professores sobre entrega realizada
    """
    titulo = "Nova Entrega Realizada"
    mensagem = f"O aluno {entrega.aluno.nome} realizou uma entrega para a atividade '{entrega.atividade.descricao}'"
    
    return enviar_notificacao_para_todos_professores(
        titulo, mensagem, 'info', atividade_id=entrega.atividade_id, entrega_id=entrega.id
    )

def notificar_avaliacao_concluida(entrega):
    """
    Notifica aluno sobre avaliação concluída
    """
    titulo = "Atividade Avaliada"
    mensagem = f"Sua entrega da atividade '{entrega.atividade.descricao}' foi avaliada"
    if entrega.nota:
        mensagem += f" - Nota: {entrega.nota}"
    
    return enviar_notificacao(
        entrega.aluno_id, 'aluno', titulo, mensagem, 'sucesso',
        atividade_id=entrega.atividade_id, entrega_id=entrega.id
    )

def notificar_prazo_proximo(atividade, dias_restantes):
    """
    Notifica sobre prazo próximo de atividade
    """
    titulo = "Prazo Próximo"
    mensagem = f"A atividade '{atividade.descricao}' vence em {dias_restantes} dia(s)"
    
    return enviar_notificacao_para_todos_alunos(
        titulo, mensagem, 'aviso', atividade_id=atividade.id
    )

def limpar_notificacoes_antigas(dias=30):
    """
    Remove notificações antigas (lidas) após X dias
    
    Args:
        dias: Número de dias para manter notificações lidas
    
    Returns:
        int: Número de notificações removidas
    """
    try:
        from datetime import timedelta
        
        data_limite = datetime.utcnow() - timedelta(days=dias)
        
        notificacoes_antigas = Notificacao.query.filter(
            Notificacao.lida == True,
            Notificacao.data_leitura < data_limite
        ).all()
        
        removidas = len(notificacoes_antigas)
        
        for notificacao in notificacoes_antigas:
            db.session.delete(notificacao)
        
        db.session.commit()
        
        logger.info(f"Removidas {removidas} notificações antigas")
        return removidas
        
    except Exception as e:
        logger.error(f"Erro ao limpar notificações antigas: {str(e)}")
        db.session.rollback()
        return 0
