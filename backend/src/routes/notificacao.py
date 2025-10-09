from flask import Blueprint, request, jsonify, session
from datetime import datetime
from src.database_config import db
from src.models.notificacao import Notificacao
from src.utils.auth_decorators import login_required, professor_required, get_current_user_id, get_current_user_type
from src.utils.notificacao_utils import enviar_notificacao, limpar_notificacoes_antigas

notificacao_bp = Blueprint('notificacao', __name__)

@notificacao_bp.route('/notificacoes', methods=['GET'])
@login_required
def get_notificacoes():
    """
    Lista notificações do usuário atual
    """
    try:
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        # Parâmetros de filtro
        apenas_nao_lidas = request.args.get('apenas_nao_lidas', 'false').lower() == 'true'
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Query base
        query = Notificacao.query.filter_by(
            usuario_id=user_id,
            tipo_usuario=user_type
        )
        
        # Filtrar apenas não lidas se solicitado
        if apenas_nao_lidas:
            query = query.filter_by(lida=False)
        
        # Ordenar por data de criação (mais recentes primeiro)
        query = query.order_by(Notificacao.data_criacao.desc())
        
        # Paginação
        paginacao = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Contar não lidas
        nao_lidas = Notificacao.query.filter_by(
            usuario_id=user_id,
            tipo_usuario=user_type,
            lida=False
        ).count()
        
        return jsonify({
            'notificacoes': [n.to_dict() for n in paginacao.items],
            'total': paginacao.total,
            'page': paginacao.page,
            'per_page': paginacao.per_page,
            'total_pages': paginacao.pages,
            'nao_lidas': nao_lidas
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacao_bp.route('/notificacoes/<int:notificacao_id>/marcar-lida', methods=['PUT'])
@login_required
def marcar_notificacao_lida(notificacao_id):
    """
    Marca uma notificação como lida
    """
    try:
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        notificacao = Notificacao.query.filter_by(
            id=notificacao_id,
            usuario_id=user_id,
            tipo_usuario=user_type
        ).first_or_404()
        
        if not notificacao.lida:
            notificacao.marcar_como_lida()
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notificação marcada como lida',
            'notificacao': notificacao.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notificacao_bp.route('/notificacoes/marcar-todas-lidas', methods=['PUT'])
@login_required
def marcar_todas_notificacoes_lidas():
    """
    Marca todas as notificações do usuário como lidas
    """
    try:
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        notificacoes_nao_lidas = Notificacao.query.filter_by(
            usuario_id=user_id,
            tipo_usuario=user_type,
            lida=False
        ).all()
        
        marcadas = 0
        for notificacao in notificacoes_nao_lidas:
            notificacao.marcar_como_lida()
            marcadas += 1
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'{marcadas} notificações marcadas como lidas'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notificacao_bp.route('/notificacoes/<int:notificacao_id>', methods=['DELETE'])
@login_required
def deletar_notificacao(notificacao_id):
    """
    Remove uma notificação
    """
    try:
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        notificacao = Notificacao.query.filter_by(
            id=notificacao_id,
            usuario_id=user_id,
            tipo_usuario=user_type
        ).first_or_404()
        
        db.session.delete(notificacao)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Notificação removida com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@notificacao_bp.route('/admin/notificacoes/enviar', methods=['POST'])
@professor_required
def enviar_notificacao_admin():
    """
    Permite ao professor enviar notificação personalizada
    """
    try:
        data = request.get_json()
        
        titulo = data.get('titulo')
        mensagem = data.get('mensagem')
        destinatarios = data.get('destinatarios', 'todos_alunos')  # todos_alunos, todos_professores, aluno_especifico
        destinatario_id = data.get('destinatario_id')
        tipo_notificacao = data.get('tipo_notificacao', 'info')
        
        if not titulo or not mensagem:
            return jsonify({'error': 'Título e mensagem são obrigatórios'}), 400
        
        enviadas = 0
        
        if destinatarios == 'todos_alunos':
            from src.utils.notificacao_utils import enviar_notificacao_para_todos_alunos
            enviadas = enviar_notificacao_para_todos_alunos(titulo, mensagem, tipo_notificacao)
            
        elif destinatarios == 'todos_professores':
            from src.utils.notificacao_utils import enviar_notificacao_para_todos_professores
            enviadas = enviar_notificacao_para_todos_professores(titulo, mensagem, tipo_notificacao)
            
        elif destinatarios == 'aluno_especifico' and destinatario_id:
            if enviar_notificacao(destinatario_id, 'aluno', titulo, mensagem, tipo_notificacao):
                enviadas = 1
                
        elif destinatarios == 'professor_especifico' and destinatario_id:
            if enviar_notificacao(destinatario_id, 'professor', titulo, mensagem, tipo_notificacao):
                enviadas = 1
        
        return jsonify({
            'success': True,
            'message': f'Notificação enviada para {enviadas} usuário(s)',
            'enviadas': enviadas
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacao_bp.route('/admin/notificacoes/limpar-antigas', methods=['POST'])
@professor_required
def limpar_notificacoes_antigas_admin():
    """
    Remove notificações antigas (apenas professores)
    """
    try:
        data = request.get_json() or {}
        dias = int(data.get('dias', 30))
        
        removidas = limpar_notificacoes_antigas(dias)
        
        return jsonify({
            'success': True,
            'message': f'{removidas} notificações antigas foram removidas',
            'removidas': removidas
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@notificacao_bp.route('/notificacoes/estatisticas', methods=['GET'])
@login_required
def get_estatisticas_notificacoes():
    """
    Estatísticas de notificações do usuário
    """
    try:
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        total = Notificacao.query.filter_by(
            usuario_id=user_id,
            tipo_usuario=user_type
        ).count()
        
        nao_lidas = Notificacao.query.filter_by(
            usuario_id=user_id,
            tipo_usuario=user_type,
            lida=False
        ).count()
        
        lidas = total - nao_lidas
        
        # Notificações por tipo
        tipos = db.session.query(
            Notificacao.tipo_notificacao,
            db.func.count(Notificacao.id)
        ).filter_by(
            usuario_id=user_id,
            tipo_usuario=user_type
        ).group_by(Notificacao.tipo_notificacao).all()
        
        tipos_dict = {tipo: count for tipo, count in tipos}
        
        return jsonify({
            'total': total,
            'lidas': lidas,
            'nao_lidas': nao_lidas,
            'por_tipo': tipos_dict
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
