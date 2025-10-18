"""
Rotas de gerenciamento de questões (múltipla escolha)
"""
from flask import Blueprint, request, jsonify
from datetime import datetime
from app import db
from app.models.questao import Questao, Resposta
from app.models.atividade import Atividade
from app.utils.auth import professor_required, login_required, get_current_user

bp = Blueprint('questoes', __name__, url_prefix='/api')

# Rotas de questões (professor)
@bp.route('/atividades/<int:atividade_id>/questoes', methods=['GET'])
@login_required
def listar_questoes(atividade_id):
    """Lista questões de uma atividade"""
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    if atividade.tipo != 'multipla_escolha':
        return jsonify({'ok': False, 'error': 'Atividade não é do tipo múltipla escolha'}), 400
    
    questoes = Questao.query.filter_by(atividade_id=atividade_id).order_by(Questao.ordem).all()
    
    # Se for professor, incluir respostas corretas
    usuario = get_current_user()
    include_resposta = usuario.tipo in ['professor', 'admin']
    
    return jsonify({
        'ok': True,
        'questoes': [q.to_dict(include_resposta=include_resposta) for q in questoes]
    }), 200

@bp.route('/atividades/<int:atividade_id>/questoes', methods=['POST'])
@professor_required
def criar_questao(atividade_id):
    """Cria uma nova questão para atividade de múltipla escolha"""
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    if atividade.tipo != 'multipla_escolha':
        return jsonify({'ok': False, 'error': 'Atividade não é do tipo múltipla escolha'}), 400
    
    data = request.get_json()
    
    # Validações
    if not data.get('enunciado'):
        return jsonify({'ok': False, 'error': 'Campo enunciado é obrigatório'}), 400
    
    # Criar questão
    questao = Questao(
        atividade_id=atividade_id,
        enunciado=data['enunciado'],
        tipo=data.get('tipo', 'single'),
        pontuacao=data.get('pontuacao', 1.0),
        ordem=data.get('ordem', 0)
    )
    
    if 'alternativas' in data:
        questao.set_alternativas(data['alternativas'])
    
    if 'resposta_correta' in data:
        questao.set_resposta_correta(data['resposta_correta'])
    
    db.session.add(questao)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'questao': questao.to_dict(include_resposta=True),
        'message': 'Questão criada com sucesso'
    }), 201

@bp.route('/questoes/<int:questao_id>', methods=['PUT'])
@professor_required
def atualizar_questao(questao_id):
    """Atualiza uma questão existente"""
    questao = Questao.query.get(questao_id)
    
    if not questao:
        return jsonify({'ok': False, 'error': 'Questão não encontrada'}), 404
    
    data = request.get_json()
    
    # Atualizar campos
    if 'enunciado' in data:
        questao.enunciado = data['enunciado']
    if 'tipo' in data:
        questao.tipo = data['tipo']
    if 'alternativas' in data:
        questao.set_alternativas(data['alternativas'])
    if 'resposta_correta' in data:
        questao.set_resposta_correta(data['resposta_correta'])
    if 'pontuacao' in data:
        questao.pontuacao = data['pontuacao']
    if 'ordem' in data:
        questao.ordem = data['ordem']
    
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'questao': questao.to_dict(include_resposta=True),
        'message': 'Questão atualizada com sucesso'
    }), 200

@bp.route('/questoes/<int:questao_id>', methods=['DELETE'])
@professor_required
def deletar_questao(questao_id):
    """Deleta uma questão"""
    questao = Questao.query.get(questao_id)
    
    if not questao:
        return jsonify({'ok': False, 'error': 'Questão não encontrada'}), 404
    
    db.session.delete(questao)
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'message': 'Questão deletada com sucesso'
    }), 200

# Rotas de respostas (aluno)
@bp.route('/atividades/<int:atividade_id>/responder', methods=['POST'])
@login_required
def responder_atividade(atividade_id):
    """
    Aluno responde questões de múltipla escolha.
    Correção automática e cálculo de nota.
    """
    usuario = get_current_user()
    
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    if atividade.tipo != 'multipla_escolha':
        return jsonify({'ok': False, 'error': 'Atividade não é do tipo múltipla escolha'}), 400
    
    data = request.get_json()
    respostas_data = data.get('respostas', [])
    
    if not respostas_data:
        return jsonify({'ok': False, 'error': 'Nenhuma resposta fornecida'}), 400
    
    # Processar respostas
    respostas_criadas = []
    nota_total = 0
    pontos_possiveis = 0
    
    for resp_data in respostas_data:
        questao_id = resp_data.get('questao_id')
        resposta_aluno = resp_data.get('resposta')
        
        questao = Questao.query.get(questao_id)
        if not questao or questao.atividade_id != atividade_id:
            continue
        
        # Verificar se já existe resposta (evitar duplicatas)
        resposta_existente = Resposta.query.filter_by(
            questao_id=questao_id,
            aluno_id=usuario.id,
            atividade_id=atividade_id
        ).first()
        
        if resposta_existente:
            continue
        
        # Correção automática
        resposta_correta_obj = questao.get_resposta_correta()
        correta = False
        pontos_obtidos = 0
        
        if resposta_correta_obj is not None:
            if isinstance(resposta_correta_obj, list):
                # Múltipla escolha (multiple)
                correta = set(resposta_aluno) == set(resposta_correta_obj)
            else:
                # Única escolha (single)
                correta = resposta_aluno == resposta_correta_obj
            
            if correta:
                pontos_obtidos = float(questao.pontuacao)
        
        # Criar resposta
        resposta = Resposta(
            questao_id=questao_id,
            aluno_id=usuario.id,
            atividade_id=atividade_id,
            correta=correta,
            pontos_obtidos=pontos_obtidos
        )
        resposta.set_resposta(resposta_aluno)
        
        db.session.add(resposta)
        respostas_criadas.append(resposta)
        
        nota_total += pontos_obtidos
        pontos_possiveis += float(questao.pontuacao)
    
    db.session.commit()
    
    # Calcular nota percentual
    nota_percentual = (nota_total / pontos_possiveis * 100) if pontos_possiveis > 0 else 0
    
    return jsonify({
        'ok': True,
        'respostas': [r.to_dict() for r in respostas_criadas],
        'nota_total': nota_total,
        'pontos_possiveis': pontos_possiveis,
        'nota_percentual': round(nota_percentual, 2),
        'message': 'Respostas enviadas e corrigidas com sucesso'
    }), 201

@bp.route('/atividades/<int:atividade_id>/minhas-respostas', methods=['GET'])
@login_required
def minhas_respostas(atividade_id):
    """Retorna respostas do aluno para uma atividade"""
    usuario = get_current_user()
    
    respostas = Resposta.query.filter_by(
        atividade_id=atividade_id,
        aluno_id=usuario.id
    ).all()
    
    return jsonify({
        'ok': True,
        'respostas': [r.to_dict() for r in respostas]
    }), 200

@bp.route('/atividades/<int:atividade_id>/estatisticas', methods=['GET'])
@professor_required
def estatisticas_atividade(atividade_id):
    """
    Retorna estatísticas de uma atividade de múltipla escolha.
    Taxa de acerto por questão, média geral, etc.
    """
    atividade = Atividade.query.get(atividade_id)
    
    if not atividade:
        return jsonify({'ok': False, 'error': 'Atividade não encontrada'}), 404
    
    if atividade.tipo != 'multipla_escolha':
        return jsonify({'ok': False, 'error': 'Atividade não é do tipo múltipla escolha'}), 400
    
    questoes = Questao.query.filter_by(atividade_id=atividade_id).all()
    
    estatisticas = []
    
    for questao in questoes:
        respostas = Resposta.query.filter_by(questao_id=questao.id).all()
        
        total_respostas = len(respostas)
        corretas = sum(1 for r in respostas if r.correta)
        taxa_acerto = (corretas / total_respostas * 100) if total_respostas > 0 else 0
        
        estatisticas.append({
            'questao_id': questao.id,
            'enunciado': questao.enunciado,
            'total_respostas': total_respostas,
            'respostas_corretas': corretas,
            'taxa_acerto': round(taxa_acerto, 2)
        })
    
    return jsonify({
        'ok': True,
        'estatisticas': estatisticas
    }), 200

