"""
Rotas de gerenciamento de entregas
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.entrega import Entrega
from app.models.atividade import Atividade
from app.models.grupo import Grupo
from app.models.avaliacao import Avaliacao
from app.utils.auth import professor_required, login_required, get_current_user
from app.utils.file_upload import save_multiple_files
from app.utils.notifications import notificar_entrega_recebida, notificar_avaliacao_concluida

bp = Blueprint('entregas', __name__, url_prefix='/api/entregas')

@bp.route('/', methods=['GET'])
@login_required
def listar_entregas():
    """Lista entregas com filtros"""
    usuario = get_current_user()
    
    atividade_id = request.args.get('atividade_id', type=int)
    aluno_id = request.args.get('aluno_id', type=int)
    status = request.args.get('status')
    
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    query = Entrega.query
    
    # Se for aluno, só pode ver suas próprias entregas
    if usuario.tipo == 'aluno':
        query = query.filter_by(aluno_id=usuario.id)
    elif aluno_id:
        query = query.filter_by(aluno_id=aluno_id)
    
    if atividade_id:
        query = query.filter_by(atividade_id=atividade_id)
    
    if status:
        query = query.filter_by(status=status)
    
    # Ordenar por data de envio
    query = query.order_by(Entrega.data_envio.desc())
    
    entregas_paginadas = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'ok': True,
        'entregas': [entrega.to_dict() for entrega in entregas_paginadas.items],
        'total': entregas_paginadas.total,
        'page': page,
        'per_page': per_page,
        'pages': entregas_paginadas.pages
    }), 200

@bp.route('/<int:entrega_id>', methods=['GET'])
@login_required
def obter_entrega(entrega_id):
    """Obtém detalhes de uma entrega específica"""
    entrega = Entrega.query.get(entrega_id)
    
    if not entrega:
        return jsonify({'ok': False, 'error': 'Entrega não encontrada'}), 404
    
    # Verificar permissão
    usuario = get_current_user()
    if usuario.tipo == 'aluno' and entrega.aluno_id != usuario.id:
        return jsonify({'ok': False, 'error': 'Acesso negado'}), 403
    
    return jsonify({
        'ok': True,
        'entrega': entrega.to_dict()
    }), 200

@bp.route('/upload', methods=['POST'])
@login_required
def criar_entrega():
    """
    Cria uma nova entrega com upload de arquivos.
    Suporta entregas individuais e para o líder do grupo.
    """
    usuario = get_current_user()
    
    # Obter dados do formulário multipart
    atividade_id = request.form.get('atividade_id', type=int)
    observacoes = request.form.get('observacoes', '')
    destino_grupo = request.form.get('destino_grupo', 'false').lower() == 'true'
    encaminhado_para = request.form.get('encaminhado_para', type=int)
    
    if not atividade_id:
        return jsonify({'ok': False, 'error': 'Campo atividade_id é obrigatório'}), 400
    
    # Verificar se atividade existe
    atividade = Atividade.query.get(atividade_id)
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    # Verificar prazo
    agora = datetime.utcnow()
    status = 'entregue'
    if agora > atividade.prazo:
        status = 'atrasada'
    
    # Upload de arquivos
    arquivos = request.files.getlist('arquivos[]')
    arquivo_urls = []
    
    if arquivos:
        try:
            arquivo_urls = save_multiple_files(arquivos)
        except Exception as e:
            return jsonify({'ok': False, 'error': f'Erro ao fazer upload: {str(e)}'}), 500
    
    # Criar entrega
    entrega = Entrega(
        atividade_id=atividade_id,
        aluno_id=usuario.id,
        status=status,
        observacoes=observacoes,
        destino_grupo=destino_grupo,
        encaminhado_para=encaminhado_para
    )
    
    entrega.set_arquivos(arquivo_urls)
    
    db.session.add(entrega)
    db.session.commit()
    
    # Notificar professor ou líder
    if destino_grupo and encaminhado_para:
        # Notificar líder (implementar se necessário)
        pass
    else:
        # Notificar professor
        notificar_entrega_recebida(entrega, atividade.criado_por)
    
    return jsonify({
        'ok': True,
        'entrega': entrega.to_dict(),
        'message': 'Entrega enviada com sucesso'
    }), 201

@bp.route('/<int:entrega_id>/permitir-edicao', methods=['PUT'])
@professor_required
def permitir_edicao(entrega_id):
    """
    Permite que o aluno edite uma entrega já enviada.
    Apenas o professor pode autorizar.
    """
    entrega = Entrega.query.get(entrega_id)
    
    if not entrega:
        return jsonify({'ok': False, 'error': 'Entrega não encontrada'}), 404
    
    # Marcar entrega como editável (implementar lógica adicional se necessário)
    entrega.status = 'pendente'
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Edição permitida'
    }), 200

@bp.route('/<int:entrega_id>/avaliar', methods=['PUT'])
@professor_required
def avaliar_entrega(entrega_id):
    """
    Avalia uma entrega (nota e feedback).
    """
    usuario = get_current_user()
    entrega = Entrega.query.get(entrega_id)
    
    if not entrega:
        return jsonify({'ok': False, 'error': 'Entrega não encontrada'}), 404
    
    data = request.get_json()
    
    if 'nota' not in data:
        return jsonify({'ok': False, 'error': 'Campo nota é obrigatório'}), 400
    
    # Atualizar entrega
    entrega.nota = data['nota']
    entrega.avaliado_por = usuario.id
    entrega.data_avaliacao = datetime.utcnow()
    entrega.status = 'rejeitado' if data.get('rejeitado', False) else 'avaliado'
    
    # Criar registro de avaliação
    avaliacao = Avaliacao(
        entrega_id=entrega_id,
        professor_id=usuario.id,
        nota=data['nota'],
        feedback=data.get('feedback', ''),
        rejeitado=data.get('rejeitado', False)
    )
    
    db.session.add(avaliacao)
    db.session.commit()
    
    # Notificar aluno
    notificar_avaliacao_concluida(entrega)
    
    return jsonify({
        'ok': True,
        'entrega': entrega.to_dict(),
        'avaliacao': avaliacao.to_dict(),
        'message': 'Entrega avaliada com sucesso'
    }), 200

@bp.route('/lider/<int:grupo_id>', methods=['GET'])
@login_required
def entregas_para_lider(grupo_id):
    """
    Retorna entregas individuais dos membros do grupo para o líder consolidar.
    """
    usuario = get_current_user()
    
    # Verificar se usuário é líder do grupo
    grupo = Grupo.query.get(grupo_id)
    if not grupo:
        return jsonify({'ok': False, 'error': 'Grupo não encontrado'}), 404
    
    if grupo.lider_id != usuario.id:
        return jsonify({'ok': False, 'error': 'Apenas o líder pode acessar'}), 403
    
    # Buscar entregas dos membros
    entregas = Entrega.query.filter_by(
        destino_grupo=True,
        encaminhado_para=usuario.id
    ).all()
    
    return jsonify({
        'ok': True,
        'entregas': [entrega.to_dict() for entrega in entregas]
    }), 200

@bp.route('/consolidar/<int:grupo_id>', methods=['POST'])
@login_required
def consolidar_entrega_grupo(grupo_id):
    """
    Consolida entregas individuais e envia ao professor.
    Apenas o líder pode consolidar.
    """
    usuario = get_current_user()
    
    # Verificar se usuário é líder do grupo
    grupo = Grupo.query.get(grupo_id)
    if not grupo:
        return jsonify({'ok': False, 'error': 'Grupo não encontrado'}), 404
    
    if grupo.lider_id != usuario.id:
        return jsonify({'ok': False, 'error': 'Apenas o líder pode consolidar'}), 403
    
    data = request.get_json()
    
    # Criar entrega consolidada do grupo
    entrega_grupo = Entrega(
        atividade_id=grupo.atividade_id,
        grupo_id=grupo_id,
        status='entregue',
        observacoes=data.get('observacoes', ''),
        consolidada=True
    )
    
    # Coletar arquivos de todas as entregas individuais
    entregas_individuais = Entrega.query.filter_by(
        destino_grupo=True,
        encaminhado_para=usuario.id
    ).all()
    
    todos_arquivos = []
    for entrega in entregas_individuais:
        todos_arquivos.extend(entrega.get_arquivos())
    
    entrega_grupo.set_arquivos(todos_arquivos)
    
    db.session.add(entrega_grupo)
    db.session.commit()
    
    # Notificar professor
    notificar_entrega_recebida(entrega_grupo, grupo.atividade.criado_por)
    
    return jsonify({
        'ok': True,
        'entrega': entrega_grupo.to_dict(),
        'message': 'Entrega consolidada e enviada ao professor'
    }), 201

