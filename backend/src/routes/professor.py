from flask import Blueprint, request, jsonify, session
from datetime import datetime, timedelta
from ..database_config import db
from ..models.professor import Professor
from ..models.atividade import Atividade
from ..models.entrega import Entrega
from ..models.aluno import Aluno

professor_bp = Blueprint('professor', __name__)

# Middleware para verificar se é professor
def verificar_professor():
    if 'user_id' not in session or session.get('user_type') != 'professor':
        return jsonify({'error': 'Acesso negado. Apenas professores podem acessar esta rota.'}), 403
    return None

# ==================== ATIVIDADES ====================

@professor_bp.route('/atividades', methods=['GET'])
def listar_atividades():
    """Lista todas as atividades do professor logado"""
    erro = verificar_professor()
    if erro:
        return erro
    
    professor_id = session['user_id']
    atividades = Atividade.query.filter_by(professor_id=professor_id).order_by(Atividade.created_at.desc()).all()
    
    return jsonify({
        'atividades': [atividade.to_dict() for atividade in atividades]
    })

@professor_bp.route('/atividades', methods=['POST'])
def criar_atividade():
    """Cria uma nova atividade"""
    erro = verificar_professor()
    if erro:
        return erro
    
    data = request.get_json()
    professor_id = session['user_id']
    
    # Validações
    campos_obrigatorios = ['titulo', 'descricao', 'formato', 'prazo_entrega', 'tipo']
    for campo in campos_obrigatorios:
        if not data.get(campo):
            return jsonify({'error': f'Campo {campo} é obrigatório'}), 400
    
    try:
        # Converter prazo para datetime
        prazo = datetime.fromisoformat(data['prazo_entrega'].replace('Z', '+00:00'))
        
        nova_atividade = Atividade(
            titulo=data['titulo'],
            descricao=data['descricao'],
            formato=data['formato'],
            prazo_entrega=prazo,
            tipo=data['tipo'],
            criterios_avaliacao=data.get('criterios_avaliacao', ''),
            professor_id=professor_id,
            status='ativa'
        )
        
        db.session.add(nova_atividade)
        db.session.commit()
        
        # Criar entregas automáticas para todos os alunos
        if data['tipo'] == 'individual':
            alunos = Aluno.query.all()
            for aluno in alunos:
                entrega = Entrega(
                    aluno_id=aluno.id,
                    atividade_id=nova_atividade.id,
                    status='pendente',
                    entregue=False
                )
                db.session.add(entrega)
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Atividade criada com sucesso!',
            'atividade': nova_atividade.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao criar atividade: {str(e)}'}), 500

@professor_bp.route('/atividades/<int:atividade_id>', methods=['GET'])
def obter_atividade(atividade_id):
    """Obtém detalhes de uma atividade específica"""
    erro = verificar_professor()
    if erro:
        return erro
    
    professor_id = session['user_id']
    atividade = Atividade.query.filter_by(id=atividade_id, professor_id=professor_id).first()
    
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada'}), 404
    
    return jsonify({'atividade': atividade.to_dict()})

@professor_bp.route('/atividades/<int:atividade_id>', methods=['PUT'])
def editar_atividade(atividade_id):
    """Edita uma atividade existente"""
    erro = verificar_professor()
    if erro:
        return erro
    
    professor_id = session['user_id']
    atividade = Atividade.query.filter_by(id=atividade_id, professor_id=professor_id).first()
    
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada'}), 404
    
    data = request.get_json()
    
    try:
        if 'titulo' in data:
            atividade.titulo = data['titulo']
        if 'descricao' in data:
            atividade.descricao = data['descricao']
        if 'formato' in data:
            atividade.formato = data['formato']
        if 'prazo_entrega' in data:
            atividade.prazo_entrega = datetime.fromisoformat(data['prazo_entrega'].replace('Z', '+00:00'))
        if 'tipo' in data:
            atividade.tipo = data['tipo']
        if 'criterios_avaliacao' in data:
            atividade.criterios_avaliacao = data['criterios_avaliacao']
        if 'status' in data:
            atividade.status = data['status']
        
        atividade.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Atividade atualizada com sucesso!',
            'atividade': atividade.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar atividade: {str(e)}'}), 500

@professor_bp.route('/atividades/<int:atividade_id>', methods=['DELETE'])
def deletar_atividade(atividade_id):
    """Deleta uma atividade"""
    erro = verificar_professor()
    if erro:
        return erro
    
    professor_id = session['user_id']
    atividade = Atividade.query.filter_by(id=atividade_id, professor_id=professor_id).first()
    
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada'}), 404
    
    try:
        db.session.delete(atividade)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Atividade deletada com sucesso!'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao deletar atividade: {str(e)}'}), 500

# ==================== ENTREGAS ====================

@professor_bp.route('/atividades/<int:atividade_id>/entregas', methods=['GET'])
def listar_entregas_atividade(atividade_id):
    """Lista todas as entregas de uma atividade"""
    erro = verificar_professor()
    if erro:
        return erro
    
    professor_id = session['user_id']
    atividade = Atividade.query.filter_by(id=atividade_id, professor_id=professor_id).first()
    
    if not atividade:
        return jsonify({'error': 'Atividade não encontrada'}), 404
    
    entregas = Entrega.query.filter_by(atividade_id=atividade_id).all()
    
    entregas_detalhadas = []
    for entrega in entregas:
        aluno = Aluno.query.get(entrega.aluno_id)
        entrega_dict = entrega.to_dict()
        entrega_dict['aluno'] = {
            'id': aluno.id,
            'nome': aluno.nome,
            'email': aluno.email
        } if aluno else None
        
        # Verificar se está atrasado
        if not entrega.entregue and datetime.utcnow() > atividade.prazo_entrega:
            entrega_dict['status'] = 'atrasado'
        
        entregas_detalhadas.append(entrega_dict)
    
    return jsonify({
        'atividade': atividade.to_dict(),
        'entregas': entregas_detalhadas
    })

@professor_bp.route('/entregas/<int:entrega_id>', methods=['GET'])
def visualizar_entrega(entrega_id):
    """Visualiza detalhes de uma entrega específica"""
    erro = verificar_professor()
    if erro:
        return erro
    
    entrega = Entrega.query.get(entrega_id)
    if not entrega:
        return jsonify({'error': 'Entrega não encontrada'}), 404
    
    # Verificar se a atividade pertence ao professor
    atividade = Atividade.query.get(entrega.atividade_id)
    if atividade.professor_id != session['user_id']:
        return jsonify({'error': 'Acesso negado'}), 403
    
    aluno = Aluno.query.get(entrega.aluno_id)
    
    entrega_dict = entrega.to_dict()
    entrega_dict['aluno'] = aluno.to_dict() if hasattr(aluno, 'to_dict') else {
        'id': aluno.id,
        'nome': aluno.nome,
        'email': aluno.email
    }
    entrega_dict['atividade'] = atividade.to_dict()
    
    return jsonify({'entrega': entrega_dict})

@professor_bp.route('/entregas/<int:entrega_id>/avaliar', methods=['POST'])
def avaliar_entrega(entrega_id):
    """Avalia uma entrega (marca como revisada ou adiciona feedback)"""
    erro = verificar_professor()
    if erro:
        return erro
    
    entrega = Entrega.query.get(entrega_id)
    if not entrega:
        return jsonify({'error': 'Entrega não encontrada'}), 404
    
    # Verificar se a atividade pertence ao professor
    atividade = Atividade.query.get(entrega.atividade_id)
    if atividade.professor_id != session['user_id']:
        return jsonify({'error': 'Acesso negado'}), 403
    
    data = request.get_json()
    
    try:
        if 'status' in data:
            entrega.status = data['status']  # ex: 'revisado', 'aprovado', 'reprovado'
        
        if 'feedback' in data:
            entrega.justificativa = data['feedback']  # Usando campo justificativa para feedback
        
        entrega.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Entrega avaliada com sucesso!',
            'entrega': entrega.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao avaliar entrega: {str(e)}'}), 500

# ==================== DASHBOARD ====================

@professor_bp.route('/dashboard', methods=['GET'])
def dashboard_professor():
    """Retorna estatísticas e informações do dashboard do professor"""
    erro = verificar_professor()
    if erro:
        return erro
    
    professor_id = session['user_id']
    
    # Estatísticas
    total_atividades = Atividade.query.filter_by(professor_id=professor_id).count()
    atividades_ativas = Atividade.query.filter_by(professor_id=professor_id, status='ativa').count()
    
    # Entregas pendentes
    atividades_professor = Atividade.query.filter_by(professor_id=professor_id).all()
    atividades_ids = [a.id for a in atividades_professor]
    
    total_entregas = Entrega.query.filter(Entrega.atividade_id.in_(atividades_ids)).count()
    entregas_pendentes = Entrega.query.filter(
        Entrega.atividade_id.in_(atividades_ids),
        Entrega.status == 'pendente'
    ).count()
    entregas_entregues = Entrega.query.filter(
        Entrega.atividade_id.in_(atividades_ids),
        Entrega.entregue == True
    ).count()
    
    # Atividades próximas do prazo (próximos 7 dias)
    data_limite = datetime.utcnow() + timedelta(days=7)
    atividades_proximas = Atividade.query.filter(
        Atividade.professor_id == professor_id,
        Atividade.prazo_entrega <= data_limite,
        Atividade.prazo_entrega >= datetime.utcnow(),
        Atividade.status == 'ativa'
    ).order_by(Atividade.prazo_entrega).limit(5).all()
    
    return jsonify({
        'estatisticas': {
            'total_atividades': total_atividades,
            'atividades_ativas': atividades_ativas,
            'total_entregas': total_entregas,
            'entregas_pendentes': entregas_pendentes,
            'entregas_entregues': entregas_entregues,
            'taxa_entrega': round((entregas_entregues / total_entregas * 100) if total_entregas > 0 else 0, 2)
        },
        'atividades_proximas': [a.to_dict() for a in atividades_proximas]
    })
