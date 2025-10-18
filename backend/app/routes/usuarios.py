"""
Rotas de gerenciamento de usuários (alunos)
"""
from flask import Blueprint, request, jsonify
from app import db
from app.models.usuario import Usuario
from app.utils.auth import professor_required, login_required
from app.utils.email_generator import gerar_email_aluno

bp = Blueprint('usuarios', __name__, url_prefix='/api/alunos')

@bp.route('/', methods=['GET'])
@professor_required
def listar_alunos():
    """Lista todos os alunos com filtros opcionais"""
    turma = request.args.get('turma')
    curso = request.args.get('curso')
    status = request.args.get('status', 'ativo')
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Usuario.query.filter_by(tipo='aluno')
    
    if turma:
        query = query.filter_by(turma=turma)
    if curso:
        query = query.filter_by(curso=curso)
    if status:
        query = query.filter_by(status=status)
    
    alunos_paginados = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'ok': True,
        'alunos': [aluno.to_dict() for aluno in alunos_paginados.items],
        'total': alunos_paginados.total,
        'page': page,
        'per_page': per_page,
        'pages': alunos_paginados.pages
    }), 200

@bp.route('/<int:aluno_id>', methods=['GET'])
@login_required
def obter_aluno(aluno_id):
    """Obtém detalhes de um aluno específico"""
    aluno = Usuario.query.get(aluno_id)
    
    if not aluno or aluno.tipo != 'aluno':
        return jsonify({'ok': False, 'error': 'Aluno não encontrado'}), 404
    
    return jsonify({
        'ok': True,
        'aluno': aluno.to_dict()
    }), 200

@bp.route('/', methods=['POST'])
@professor_required
def criar_aluno():
    """
    Cria um novo aluno.
    O e-mail é gerado automaticamente conforme as regras do SENAC.
    """
    data = request.get_json()
    
    # Validações
    required_fields = ['nome_completo', 'curso', 'turma', 'senha']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'ok': False, 'error': f'Campo {field} é obrigatório'}), 400
    
    # Gerar e-mail automaticamente
    email = gerar_email_aluno(data['nome_completo'], data['curso'], data['turma'])
    
    # Verificar se e-mail já existe
    if Usuario.query.filter_by(email=email).first():
        return jsonify({'ok': False, 'error': 'E-mail já cadastrado'}), 400
    
    # Criar aluno
    aluno = Usuario(
        nome_completo=data['nome_completo'],
        email=email,
        tipo='aluno',
        curso=data['curso'],
        turma=data['turma'],
        status='ativo'
    )
    aluno.set_password(data['senha'])
    
    db.session.add(aluno)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'aluno': aluno.to_dict(),
        'message': 'Aluno criado com sucesso'
    }), 201

@bp.route('/<int:aluno_id>', methods=['PUT'])
@professor_required
def atualizar_aluno(aluno_id):
    """Atualiza dados de um aluno"""
    aluno = Usuario.query.get(aluno_id)
    
    if not aluno or aluno.tipo != 'aluno':
        return jsonify({'ok': False, 'error': 'Aluno não encontrado'}), 404
    
    data = request.get_json()
    
    # Atualizar campos permitidos
    if 'nome_completo' in data:
        aluno.nome_completo = data['nome_completo']
    if 'curso' in data:
        aluno.curso = data['curso']
    if 'turma' in data:
        aluno.turma = data['turma']
    if 'status' in data:
        aluno.status = data['status']
    if 'senha' in data:
        aluno.set_password(data['senha'])
    
    # Se nome, curso ou turma mudaram, regenerar e-mail
    if 'nome_completo' in data or 'curso' in data or 'turma' in data:
        novo_email = gerar_email_aluno(aluno.nome_completo, aluno.curso, aluno.turma)
        # Verificar se novo e-mail já existe
        email_existente = Usuario.query.filter_by(email=novo_email).first()
        if email_existente and email_existente.id != aluno.id:
            return jsonify({'ok': False, 'error': 'E-mail gerado já está em uso'}), 400
        aluno.email = novo_email
    
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'aluno': aluno.to_dict(),
        'message': 'Aluno atualizado com sucesso'
    }), 200

@bp.route('/<int:aluno_id>', methods=['DELETE'])
@professor_required
def deletar_aluno(aluno_id):
    """
    Deleta (inativa) um aluno.
    Não remove do banco, apenas marca como inativo.
    """
    aluno = Usuario.query.get(aluno_id)
    
    if not aluno or aluno.tipo != 'aluno':
        return jsonify({'ok': False, 'error': 'Aluno não encontrado'}), 404
    
    aluno.status = 'inativo'
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Aluno inativado com sucesso'
    }), 200

