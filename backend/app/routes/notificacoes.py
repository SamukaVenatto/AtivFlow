"""
Rotas de gerenciamento de notificações
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.notificacao import Notificacao
from app.utils.auth import professor_required, login_required, get_current_user
from app.utils.notifications import criar_notificacao_global, notificar_turma, limpar_notificacoes_antigas

bp = Blueprint('notificacoes', __name__, url_prefix='/api/notificacoes')

@bp.route('/', methods=['GET'])
@login_required
def minhas_notificacoes():
    """
    Retorna notificações do usuário atual.
    Inclui notificações específicas e globais.
    """
    usuario = get_current_user()
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    lida = request.args.get('lida')
    
    # Buscar notificações específicas do usuário ou globais
    query = Notificacao.query.filter(
        (Notificacao.usuario_id == usuario.id) | (Notificacao.usuario_id == None)
    )
    
    if lida is not None:
        lida_bool = lida.lower() == 'true'
        query = query.filter_by(lida=lida_bool)
    
    query = query.order_by(Notificacao.data_envio.desc())
    
    notificacoes_paginadas = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'ok': True,
        'notificacoes': [n.to_dict() for n in notificacoes_paginadas.items],
        'total': notificacoes_paginadas.total,
        'page': page,
        'per_page': per_page,
        'pages': notificacoes_paginadas.pages
    }), 200

@bp.route('/<int:notificacao_id>/marcar-lida', methods=['PUT'])
@login_required
def marcar_lida(notificacao_id):
    """Marca uma notificação como lida"""
    usuario = get_current_user()
    
    notificacao = Notificacao.query.get(notificacao_id)
    
    if not notificacao:
        return jsonify({'ok': False, 'error': 'Notificação não encontrada'}), 404
    
    # Verificar permissão
    if notificacao.usuario_id and notificacao.usuario_id != usuario.id:
        return jsonify({'ok': False, 'error': 'Acesso negado'}), 403
    
    notificacao.lida = True
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Notificação marcada como lida'
    }), 200

@bp.route('/marcar-todas-lidas', methods=['PUT'])
@login_required
def marcar_todas_lidas():
    """Marca todas as notificações do usuário como lidas"""
    usuario = get_current_user()
    
    # Atualizar notificações específicas do usuário
    Notificacao.query.filter_by(usuario_id=usuario.id, lida=False).update({'lida': True})
    
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Todas as notificações foram marcadas como lidas'
    }), 200

@bp.route('/admin/notificacoes/enviar', methods=['POST'])
@professor_required
def enviar_notificacao_manual():
    """
    Professor envia notificação manual.
    Pode ser para uma turma específica ou global.
    """
    data = request.get_json()
    
    # Validações
    required_fields = ['titulo', 'mensagem']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'ok': False, 'error': f'Campo {field} é obrigatório'}), 400
    
    titulo = data['titulo']
    mensagem = data['mensagem']
    tipo = data.get('tipo', 'info')
    turma = data.get('turma')
    
    if turma:
        # Notificar turma específica
        notificar_turma(turma, titulo, mensagem, tipo)
        return jsonify({
            'ok': True,
            'message': f'Notificação enviada para a turma {turma}'
        }), 201
    else:
        # Notificação global
        criar_notificacao_global(titulo, mensagem, tipo)
        return jsonify({
            'ok': True,
            'message': 'Notificação global enviada'
        }), 201

@bp.route('/admin/notificacoes/limpar-antigas', methods=['DELETE'])
@professor_required
def limpar_antigas():
    """
    Remove notificações com mais de 30 dias (configurável).
    """
    dias = request.args.get('dias', 30, type=int)
    
    count = limpar_notificacoes_antigas(dias)
    
    return jsonify({
        'ok': True,
        'message': f'{count} notificações antigas foram removidas'
    }), 200

@bp.route('/nao-lidas/count', methods=['GET'])
@login_required
def count_nao_lidas():
    """Retorna contagem de notificações não lidas"""
    usuario = get_current_user()
    
    count = Notificacao.query.filter(
        (Notificacao.usuario_id == usuario.id) | (Notificacao.usuario_id == None),
        Notificacao.lida == False
    ).count()
    
    return jsonify({
        'ok': True,
        'count': count
    }), 200

