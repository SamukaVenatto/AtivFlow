"""
Utilitários para gestão de entregas
"""
from src.database_config import db
from src.models.entrega import Entrega
from src.models.aluno import Aluno

def criar_entregas_automaticas(atividade):
    """
    Cria entregas automáticas para atividades individuais
    
    Args:
        atividade: Objeto Atividade
    
    Returns:
        int: Número de entregas criadas
    """
    try:
        # Só criar entregas automáticas para atividades individuais ou de múltipla escolha
        if atividade.tipo not in ['individual', 'multipla_escolha']:
            return 0
        
        # Buscar todos os alunos ativos
        alunos_ativos = Aluno.query.filter_by(status='ativo').all()
        
        entregas_criadas = 0
        
        for aluno in alunos_ativos:
            # Verificar se já existe entrega para este aluno/atividade
            entrega_existente = Entrega.query.filter_by(
                aluno_id=aluno.id,
                atividade_id=atividade.id
            ).first()
            
            if not entrega_existente:
                nova_entrega = Entrega(
                    aluno_id=aluno.id,
                    atividade_id=atividade.id,
                    entregue=False,
                    status='pendente'
                )
                
                db.session.add(nova_entrega)
                entregas_criadas += 1
        
        if entregas_criadas > 0:
            db.session.commit()
        
        return entregas_criadas
        
    except Exception as e:
        db.session.rollback()
        raise e

def criar_entrega_para_novo_aluno(aluno_id):
    """
    Cria entregas pendentes para um novo aluno em todas as atividades individuais ativas
    
    Args:
        aluno_id: ID do aluno
    
    Returns:
        int: Número de entregas criadas
    """
    try:
        from src.models.atividade import Atividade
        
        # Buscar atividades individuais e de múltipla escolha ativas
        atividades = Atividade.query.filter(
            Atividade.status == 'ativa',
            Atividade.tipo.in_(['individual', 'multipla_escolha'])
        ).all()
        
        entregas_criadas = 0
        
        for atividade in atividades:
            # Verificar se já existe entrega
            entrega_existente = Entrega.query.filter_by(
                aluno_id=aluno_id,
                atividade_id=atividade.id
            ).first()
            
            if not entrega_existente:
                nova_entrega = Entrega(
                    aluno_id=aluno_id,
                    atividade_id=atividade.id,
                    entregue=False,
                    status='pendente'
                )
                
                db.session.add(nova_entrega)
                entregas_criadas += 1
        
        if entregas_criadas > 0:
            db.session.commit()
        
        return entregas_criadas
        
    except Exception as e:
        db.session.rollback()
        raise e
