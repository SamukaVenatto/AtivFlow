"""
Rotas de gerenciamento de atividades
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.atividade import Atividade
from app.models.usuario import Usuario
from app.utils.auth import professor_required, login_required, get_current_user
from app.utils.notifications import notificar_nova_atividade

bp = Blueprint('atividades', __name__, url_prefix='/api/atividades')

@bp.route('/', methods=['GET'])
@login_required
def listar_atividades():
    """Lista atividades com filtros"""
    usuario = get_current_user()
    
    tipo = request.args.get('tipo')
    turma = request.args.get('turma')
    ativo = request.args.get('ativo', 'true').lower() == 'true'
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Atividade.query
    
    # Filtrar por turma do aluno se for aluno
    if usuario.tipo == 'aluno':
        query = query.filter_by(turma=usuario.turma)
    elif turma:
        query = query.filter_by(turma=turma)
    
    if tipo:
        query = query.filter_by(tipo=tipo)
    
    query = query.filter_by(ativo=ativo)
    
    # Ordenar por prazo
    query = query.order_by(Atividade.prazo.asc())
    
    atividades_paginadas = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'ok': True,
        'atividades': [atividade.to_dict() for atividade in atividades_paginadas.items],
        'total': atividades_paginadas.total,
        'page': page,
        'per_page': per_page,
        'pages': atividades_paginadas.pages
    }), 200

@bp.route('/<int:atividade_id>', methods=['GET'])
@login_required
def obter_atividade(atividade_id):
    """Obtém detalhes de uma atividade específica"""
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    # Verificar permissão (aluno só pode ver atividades da sua turma)
    usuario = get_current_user()
    if usuario.tipo == 'aluno' and atividade.turma != usuario.turma:
        return jsonify({'ok': False, 'error': 'Acesso negado'}), 403
    
    return jsonify({
        'ok': True,
        'atividade': atividade.to_dict()
    }), 200

@bp.route('/', methods=['POST'])
@professor_required
def criar_atividade():
    """
    Cria uma nova atividade.
    Gera notificações automáticas para alunos da turma.
    """
    data = request.get_json()
    usuario = get_current_user()
    
    # Validações
    required_fields = ['titulo', 'descricao', 'tipo', 'prazo']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'ok': False, 'error': f'Campo {field} é obrigatório'}), 400
    
    # Validar tipo
    if data['tipo'] not in ['individual', 'grupo', 'multipla_escolha']:
        return jsonify({'ok': False, 'error': 'Tipo de atividade inválido'}), 400
    
    # Converter prazo para datetime
    try:
        prazo = datetime.fromisoformat(data['prazo'].replace('Z', '+00:00'))
    except:
        return jsonify({'ok': False, 'error': 'Formato de prazo inválido'}), 400
    
    # Criar atividade
    atividade = Atividade(
        titulo=data['titulo'],
        descricao=data['descricao'],
        tipo=data['tipo'],
        prazo=prazo,
        criado_por=usuario.id,
        turma=data.get('turma'),
        ativo=True
    )
    
    # Configurações extras
    if 'config_json' in data:
        atividade.set_config(data['config_json'])
    
    db.session.add(atividade)
    db.session.commit()
    
    # Notificar alunos
    if atividade.turma:
        notificar_nova_atividade(atividade)
    
    return jsonify({
        'ok': True,
        'atividade': atividade.to_dict(),
        'message': 'Atividade criada com sucesso'
    }), 201

@bp.route('/<int:atividade_id>', methods=['PUT'])
@professor_required
def atualizar_atividade(atividade_id):
    """Atualiza uma atividade existente"""
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    data = request.get_json()
    
    # Atualizar campos
    if 'titulo' in data:
        atividade.titulo = data['titulo']
    if 'descricao' in data:
        atividade.descricao = data['descricao']
    if 'tipo' in data:
        if data['tipo'] not in ['individual', 'grupo', 'multipla_escolha']:
            return jsonify({'ok': False, 'error': 'Tipo de atividade inválido'}), 400
        atividade.tipo = data['tipo']
    if 'prazo' in data:
        try:
            atividade.prazo = datetime.fromisoformat(data['prazo'].replace('Z', '+00:00'))
        except:
            return jsonify({'ok': False, 'error': 'Formato de prazo inválido'}), 400
    if 'turma' in data:
        atividade.turma = data['turma']
    if 'ativo' in data:
        atividade.ativo = data['ativo']
    if 'config_json' in data:
        atividade.set_config(data['config_json'])
    
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'atividade': atividade.to_dict(),
        'message': 'Atividade atualizada com sucesso'
    }), 200

@bp.route('/<int:atividade_id>', methods=['DELETE'])
@professor_required
def deletar_atividade(atividade_id):
    """
    Deleta (inativa) uma atividade.
    Não remove do banco, apenas marca como inativa.
    """
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    atividade.ativo = False
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Atividade inativada com sucesso'
    }), 200

