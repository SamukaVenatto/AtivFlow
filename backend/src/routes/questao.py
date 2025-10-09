from flask import Blueprint, request, jsonify, session
from datetime import datetime
from src.database_config import db
from src.models.questao import Questao, RespostaAluno
from src.models.atividade import Atividade
from src.models.entrega import Entrega
from src.models.aluno import Aluno
from src.utils.auth_decorators import login_required, professor_required, get_current_user_id, is_professor
from sqlalchemy import func

questao_bp = Blueprint('questao', __name__)

@questao_bp.route('/atividade/<int:atividade_id>/questoes', methods=['GET'])
@login_required
def get_questoes_atividade(atividade_id):
    """
    Lista questões de uma atividade
    """
    try:
        atividade = Atividade.query.get_or_404(atividade_id)
        
        # Verificar se é atividade de múltipla escolha
        if atividade.tipo != 'multipla_escolha':
            return jsonify({'error': 'Esta atividade não é de múltipla escolha'}), 400
        
        questoes = Questao.query.filter_by(atividade_id=atividade_id).order_by(Questao.ordem).all()
        
        # Professor vê as respostas corretas, aluno não
        include_resposta = is_professor()
        
        return jsonify([q.to_dict(include_resposta=include_resposta) for q in questoes])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questao_bp.route('/atividade/<int:atividade_id>/questoes', methods=['POST'])
@professor_required
def create_questao(atividade_id):
    """
    Cria uma nova questão para atividade de múltipla escolha
    """
    try:
        atividade = Atividade.query.get_or_404(atividade_id)
        
        if atividade.tipo != 'multipla_escolha':
            return jsonify({'error': 'Esta atividade não é de múltipla escolha'}), 400
        
        data = request.get_json()
        
        # Validar dados obrigatórios
        if not data.get('pergunta'):
            return jsonify({'error': 'Pergunta é obrigatória'}), 400
        
        if not data.get('opcoes'):
            return jsonify({'error': 'Opções são obrigatórias'}), 400
        
        if not data.get('resposta_correta'):
            return jsonify({'error': 'Resposta correta é obrigatória'}), 400
        
        # Validar opções
        opcoes = data['opcoes']
        if not isinstance(opcoes, dict) or len(opcoes) < 2:
            return jsonify({'error': 'Deve haver pelo menos 2 opções'}), 400
        
        # Validar resposta correta
        resposta_correta = data['resposta_correta'].upper()
        if resposta_correta not in opcoes:
            return jsonify({'error': 'Resposta correta deve ser uma das opções disponíveis'}), 400
        
        # Determinar ordem da questão
        ultima_ordem = db.session.query(func.max(Questao.ordem)).filter_by(atividade_id=atividade_id).scalar() or 0
        
        nova_questao = Questao(
            atividade_id=atividade_id,
            pergunta=data['pergunta'],
            resposta_correta=resposta_correta,
            pontos=float(data.get('pontos', 1.0)),
            ordem=ultima_ordem + 1
        )
        
        nova_questao.set_opcoes(opcoes)
        
        db.session.add(nova_questao)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Questão criada com sucesso',
            'questao': nova_questao.to_dict(include_resposta=True)
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questao_bp.route('/questoes/<int:questao_id>', methods=['PUT'])
@professor_required
def update_questao(questao_id):
    """
    Atualiza uma questão
    """
    try:
        questao = Questao.query.get_or_404(questao_id)
        data = request.get_json()
        
        if 'pergunta' in data:
            questao.pergunta = data['pergunta']
        
        if 'opcoes' in data:
            opcoes = data['opcoes']
            if not isinstance(opcoes, dict) or len(opcoes) < 2:
                return jsonify({'error': 'Deve haver pelo menos 2 opções'}), 400
            questao.set_opcoes(opcoes)
        
        if 'resposta_correta' in data:
            resposta_correta = data['resposta_correta'].upper()
            opcoes_atuais = questao.get_opcoes()
            if resposta_correta not in opcoes_atuais:
                return jsonify({'error': 'Resposta correta deve ser uma das opções disponíveis'}), 400
            questao.resposta_correta = resposta_correta
        
        if 'pontos' in data:
            questao.pontos = float(data['pontos'])
        
        if 'ordem' in data:
            questao.ordem = int(data['ordem'])
        
        questao.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Questão atualizada com sucesso',
            'questao': questao.to_dict(include_resposta=True)
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questao_bp.route('/questoes/<int:questao_id>', methods=['DELETE'])
@professor_required
def delete_questao(questao_id):
    """
    Remove uma questão
    """
    try:
        questao = Questao.query.get_or_404(questao_id)
        
        # Remover respostas associadas
        RespostaAluno.query.filter_by(questao_id=questao_id).delete()
        
        db.session.delete(questao)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Questão removida com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questao_bp.route('/atividade/<int:atividade_id>/responder', methods=['POST'])
@login_required
def responder_questoes(atividade_id):
    """
    Aluno responde questões de múltipla escolha
    Corpo esperado:
    {
        "respostas": {
            "questao_id": "letra_escolhida",
            "questao_id": "letra_escolhida"
        }
    }
    """
    try:
        user_id = get_current_user_id()
        user_type = session.get('user_type')
        
        if user_type != 'aluno':
            return jsonify({'error': 'Apenas alunos podem responder questões'}), 403
        
        atividade = Atividade.query.get_or_404(atividade_id)
        
        if atividade.tipo != 'multipla_escolha':
            return jsonify({'error': 'Esta atividade não é de múltipla escolha'}), 400
        
        data = request.get_json()
        respostas = data.get('respostas', {})
        
        if not respostas:
            return jsonify({'error': 'Nenhuma resposta fornecida'}), 400
        
        # Buscar ou criar entrega
        entrega = Entrega.query.filter_by(aluno_id=user_id, atividade_id=atividade_id).first()
        if not entrega:
            entrega = Entrega(
                aluno_id=user_id,
                atividade_id=atividade_id,
                entregue=False,
                status='pendente'
            )
            db.session.add(entrega)
            db.session.flush()  # Para obter o ID
        
        # Remover respostas anteriores
        RespostaAluno.query.filter_by(entrega_id=entrega.id).delete()
        
        total_pontos = 0
        total_questoes = 0
        acertos = 0
        
        # Processar respostas
        for questao_id_str, resposta_escolhida in respostas.items():
            questao_id = int(questao_id_str)
            questao = Questao.query.get(questao_id)
            
            if not questao or questao.atividade_id != atividade_id:
                continue
            
            resposta_escolhida = resposta_escolhida.upper()
            correta = resposta_escolhida == questao.resposta_correta
            pontos_obtidos = questao.pontos if correta else 0
            
            resposta_aluno = RespostaAluno(
                questao_id=questao_id,
                aluno_id=user_id,
                entrega_id=entrega.id,
                resposta_escolhida=resposta_escolhida,
                correta=correta,
                pontos_obtidos=pontos_obtidos
            )
            
            db.session.add(resposta_aluno)
            
            total_pontos += pontos_obtidos
            total_questoes += 1
            if correta:
                acertos += 1
        
        # Calcular nota (0-10)
        questoes_atividade = Questao.query.filter_by(atividade_id=atividade_id).all()
        pontos_maximos = sum(q.pontos for q in questoes_atividade)
        nota = (total_pontos / pontos_maximos * 10) if pontos_maximos > 0 else 0
        
        # Atualizar entrega
        entrega.entregue = True
        entrega.status = 'entregue'
        entrega.nota = round(nota, 2)
        entrega.data_entrega = datetime.utcnow()
        entrega.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Respostas enviadas com sucesso',
            'resultado': {
                'nota': entrega.nota,
                'acertos': acertos,
                'total_questoes': total_questoes,
                'pontos_obtidos': total_pontos,
                'pontos_maximos': pontos_maximos,
                'percentual_acerto': round((acertos / total_questoes * 100), 2) if total_questoes > 0 else 0
            },
            'entrega': entrega.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questao_bp.route('/atividade/<int:atividade_id>/estatisticas', methods=['GET'])
@professor_required
def get_estatisticas_multipla_escolha(atividade_id):
    """
    Estatísticas de atividade de múltipla escolha para o professor
    """
    try:
        atividade = Atividade.query.get_or_404(atividade_id)
        
        if atividade.tipo != 'multipla_escolha':
            return jsonify({'error': 'Esta atividade não é de múltipla escolha'}), 400
        
        # Estatísticas gerais
        total_alunos = Aluno.query.filter_by(status='ativo').count()
        entregas_realizadas = Entrega.query.filter_by(atividade_id=atividade_id, entregue=True).count()
        
        # Nota média
        nota_media = db.session.query(func.avg(Entrega.nota)).filter(
            Entrega.atividade_id == atividade_id,
            Entrega.nota.isnot(None)
        ).scalar()
        nota_media = round(float(nota_media), 2) if nota_media else 0
        
        # Taxa de acerto por questão
        questoes = Questao.query.filter_by(atividade_id=atividade_id).order_by(Questao.ordem).all()
        estatisticas_questoes = []
        
        for questao in questoes:
            total_respostas = RespostaAluno.query.filter_by(questao_id=questao.id).count()
            acertos = RespostaAluno.query.filter_by(questao_id=questao.id, correta=True).count()
            taxa_acerto = (acertos / total_respostas * 100) if total_respostas > 0 else 0
            
            estatisticas_questoes.append({
                'questao_id': questao.id,
                'pergunta': questao.pergunta[:100] + '...' if len(questao.pergunta) > 100 else questao.pergunta,
                'total_respostas': total_respostas,
                'acertos': acertos,
                'taxa_acerto': round(taxa_acerto, 2)
            })
        
        return jsonify({
            'atividade_id': atividade_id,
            'total_alunos': total_alunos,
            'entregas_realizadas': entregas_realizadas,
            'taxa_participacao': round((entregas_realizadas / total_alunos * 100), 2) if total_alunos > 0 else 0,
            'nota_media': nota_media,
            'total_questoes': len(questoes),
            'estatisticas_questoes': estatisticas_questoes
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
