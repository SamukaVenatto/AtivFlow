"""
Rotas de gerenciamento de grupos
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.grupo import Grupo, GrupoMembro
from app.models.atividade import Atividade
from app.models.usuario import Usuario
from app.utils.auth import professor_required, login_required, get_current_user

bp = Blueprint('grupos', __name__, url_prefix='/api/grupos')

@bp.route('/', methods=['GET'])
@login_required
def listar_grupos():
    """Lista grupos com filtros"""
    atividade_id = request.args.get('atividade_id', type=int)
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Grupo.query
    
    if atividade_id:
        query = query.filter_by(atividade_id=atividade_id)
    
    grupos_paginados = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'ok': True,
        'grupos': [grupo.to_dict() for grupo in grupos_paginados.items],
        'total': grupos_paginados.total,
        'page': page,
        'per_page': per_page,
        'pages': grupos_paginados.pages
    }), 200

@bp.route('/<int:grupo_id>', methods=['GET'])
@login_required
def obter_grupo(grupo_id):
    """Obtém detalhes de um grupo específico"""
    grupo = Grupo.query.get(grupo_id)
    
    if not grupo:
        return jsonify({'ok': False, 'error': 'Grupo não encontrado'}), 404
    
    return jsonify({
        'ok': True,
        'grupo': grupo.to_dict()
    }), 200

@bp.route('/', methods=['POST'])
@professor_required
def criar_grupo():
    """Cria um novo grupo para uma atividade"""
    data = request.get_json()
    
    # Validações
    required_fields = ['nome', 'atividade_id']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'ok': False, 'error': f'Campo {field} é obrigatório'}), 400
    
    # Verificar se atividade existe e é do tipo grupo
    atividade = Atividade.query.get(data['atividade_id'])
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    if atividade.tipo != 'grupo':
        return jsonify({'ok': False, 'error': 'Atividade não é do tipo grupo'}), 400
    
    # Criar grupo
    grupo = Grupo(
        nome=data['nome'],
        atividade_id=data['atividade_id'],
        lider_id=data.get('lider_id'),
        observacoes=data.get('observacoes'),
        status='ativo'
    )
    
    db.session.add(grupo)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'grupo': grupo.to_dict(),
        'message': 'Grupo criado com sucesso'
    }), 201

@bp.route('/<int:grupo_id>', methods=['PUT'])
@professor_required
def atualizar_grupo(grupo_id):
    """Atualiza um grupo existente"""
    grupo = Grupo.query.get(grupo_id)
    
    if not grupo:
        return jsonify({'ok': False, 'error': 'Grupo não encontrado'}), 404
    
    data = request.get_json()
    
    # Atualizar campos
    if 'nome' in data:
        grupo.nome = data['nome']
    if 'lider_id' in data:
        grupo.lider_id = data['lider_id']
    if 'status' in data:
        grupo.status = data['status']
    if 'observacoes' in data:
        grupo.observacoes = data['observacoes']
    
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'grupo': grupo.to_dict(),
        'message': 'Grupo atualizado com sucesso'
    }), 200

@bp.route('/<int:grupo_id>/membros', methods=['POST'])
@professor_required
def adicionar_membro(grupo_id):
    """Adiciona um membro ao grupo"""
    grupo = Grupo.query.get(grupo_id)
    
    if not grupo:
        return jsonify({'ok': False, 'error': 'Grupo não encontrado'}), 404
    
    data = request.get_json()
    
    if not data.get('aluno_id'):
        return jsonify({'ok': False, 'error': 'Campo aluno_id é obrigatório'}), 400
    
    # Verificar se aluno existe
    aluno = Usuario.query.get(data['aluno_id'])
    if not aluno or aluno.tipo != 'aluno':
        return jsonify({'ok': False, 'error': 'Aluno não encontrado'}), 404
    
    # Verificar se aluno já é membro
    membro_existente = GrupoMembro.query.filter_by(
        grupo_id=grupo_id,
        aluno_id=data['aluno_id']
    ).first()
    
    if membro_existente:
        return jsonify({'ok': False, 'error': 'Aluno já é membro deste grupo'}), 400
    
    # Adicionar membro
    membro = GrupoMembro(
        grupo_id=grupo_id,
        aluno_id=data['aluno_id'],
        papel=data.get('papel'),
        status_membro='ativo'
    )
    
    db.session.add(membro)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'membro': membro.to_dict(),
        'message': 'Membro adicionado com sucesso'
    }), 201

@bp.route('/<int:grupo_id>/membros/<int:membro_id>', methods=['DELETE'])
@professor_required
def remover_membro(grupo_id, membro_id):
    """Remove um membro do grupo"""
    membro = GrupoMembro.query.filter_by(
        id=membro_id,
        grupo_id=grupo_id
    ).first()
    
    if not membro:
        return jsonify({'ok': False, 'error': 'Membro não encontrado'}), 404
    
    db.session.delete(membro)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Membro removido com sucesso'
    }), 200

@bp.route('/meus-grupos', methods=['GET'])
@login_required
def meus_grupos():
    """Retorna grupos dos quais o usuário atual é membro"""
    usuario = get_current_user()
    
    membros = GrupoMembro.query.filter_by(aluno_id=usuario.id).all()
    grupos = [membro.grupo.to_dict() for membro in membros]
    
    return jsonify({
        'ok': True,
        'grupos': grupos
    }), 200

