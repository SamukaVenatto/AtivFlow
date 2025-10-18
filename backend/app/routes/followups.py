"""
Rotas de gerenciamento de follow-ups (registros diários)
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, date
from app import db
from app.models.followup import FollowUp
from app.utils.auth import professor_required, login_required, get_current_user

bp = Blueprint('followups', __name__, url_prefix='/api/followups')

@bp.route('/me', methods=['GET'])
@login_required
def meus_followups():
    """
    Retorna histórico de follow-ups do aluno (read-only).
    """
    usuario = get_current_user()
    
    if usuario.tipo != 'aluno':
        return jsonify({'ok': False, 'error': 'Apenas alunos podem acessar'}), 403
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    followups_paginados = FollowUp.query.filter_by(aluno_id=usuario.id)\
        .order_by(FollowUp.data.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'ok': True,
        'followups': [f.to_dict() for f in followups_paginados.items],
        'total': followups_paginados.total,
        'page': page,
        'per_page': per_page,
        'pages': followups_paginados.pages
    }), 200

@bp.route('/', methods=['POST'])
@login_required
def criar_followup():
    """
    Cria um novo registro de follow-up.
    Alunos podem criar registros diariamente.
    """
    usuario = get_current_user()
    
    if usuario.tipo != 'aluno':
        return jsonify({'ok': False, 'error': 'Apenas alunos podem criar follow-ups'}), 403
    
    data = request.get_json()
    
    # Validações
    required_fields = ['atividade_realizada', 'data']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'ok': False, 'error': f'Campo {field} é obrigatório'}), 400
    
    # Converter data
    try:
        data_followup = datetime.strptime(data['data'], '%Y-%m-%d').date()
    except:
        return jsonify({'ok': False, 'error': 'Formato de data inválido (use YYYY-MM-DD)'}), 400
    
    # Verificar se já existe follow-up para esta data
    followup_existente = FollowUp.query.filter_by(
        aluno_id=usuario.id,
        data=data_followup
    ).first()
    
    if followup_existente:
        return jsonify({'ok': False, 'error': 'Já existe um follow-up para esta data'}), 400
    
    # Criar follow-up
    followup = FollowUp(
        aluno_id=usuario.id,
        atividade_realizada=data['atividade_realizada'],
        assunto_aula=data.get('assunto_aula'),
        data=data_followup,
        responsabilidade=data.get('responsabilidade'),
        status='pendente',
        justificativa=data.get('justificativa')
    )
    
    db.session.add(followup)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'followup': followup.to_dict(),
        'message': 'Follow-up criado com sucesso'
    }), 201

@bp.route('/<int:followup_id>', methods=['PUT'])
@login_required
def atualizar_followup(followup_id):
    """
    Atualiza um follow-up.
    Aluno só pode editar se pode_editar=True (liberado pelo professor).
    """
    usuario = get_current_user()
    followup = FollowUp.query.get(followup_id)
    
    if not followup:
        return jsonify({'ok': False, 'error': 'Follow-up não encontrado'}), 404
    
    # Verificar permissão
    if usuario.tipo == 'aluno':
        if followup.aluno_id != usuario.id:
            return jsonify({'ok': False, 'error': 'Acesso negado'}), 403
        
        if not followup.pode_editar:
            return jsonify({'ok': False, 'error': 'Edição não permitida. Solicite ao professor.'}), 403
    
    data = request.get_json()
    
    # Atualizar campos (aluno)
    if usuario.tipo == 'aluno':
        if 'atividade_realizada' in data:
            followup.atividade_realizada = data['atividade_realizada']
        if 'assunto_aula' in data:
            followup.assunto_aula = data['assunto_aula']
        if 'responsabilidade' in data:
            followup.responsabilidade = data['responsabilidade']
        if 'justificativa' in data:
            followup.justificativa = data['justificativa']
    
    # Atualizar campos (professor)
    if usuario.tipo in ['professor', 'admin']:
        if 'feedback_professor' in data:
            followup.feedback_professor = data['feedback_professor']
            followup.revisado = True
            followup.status = 'revisado'
        if 'pode_editar' in data:
            followup.pode_editar = data['pode_editar']
    
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'followup': followup.to_dict(),
        'message': 'Follow-up atualizado com sucesso'
    }), 200

@bp.route('/admin/followups', methods=['GET'])
@professor_required
def listar_followups_admin():
    """
    Lista follow-ups com filtros (professor).
    Permite filtrar por aluno, data, status.
    """
    aluno_id = request.args.get('aluno_id', type=int)
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')
    status = request.args.get('status')
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = FollowUp.query
    
    if aluno_id:
        query = query.filter_by(aluno_id=aluno_id)
    
    if data_inicio:
        try:
            data_inicio_obj = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            query = query.filter(FollowUp.data >= data_inicio_obj)
        except:
            pass
    
    if data_fim:
        try:
            data_fim_obj = datetime.strptime(data_fim, '%Y-%m-%d').date()
            query = query.filter(FollowUp.data <= data_fim_obj)
        except:
            pass
    
    if status:
        query = query.filter_by(status=status)
    
    query = query.order_by(FollowUp.data.desc())
    
    followups_paginados = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'ok': True,
        'followups': [f.to_dict() for f in followups_paginados.items],
        'total': followups_paginados.total,
        'page': page,
        'per_page': per_page,
        'pages': followups_paginados.pages
    }), 200

@bp.route('/<int:followup_id>/liberar-edicao', methods=['PUT'])
@professor_required
def liberar_edicao_followup(followup_id):
    """
    Professor libera edição de um follow-up para o aluno.
    """
    followup = FollowUp.query.get(followup_id)
    
    if not followup:
        return jsonify({'ok': False, 'error': 'Follow-up não encontrado'}), 404
    
    followup.pode_editar = True
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Edição liberada para o aluno'
    }), 200

