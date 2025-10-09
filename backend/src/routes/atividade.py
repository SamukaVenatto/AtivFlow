from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.atividade import Atividade, db
from src.utils.auth_decorators import professor_required
from src.utils.entrega_utils import criar_entregas_automaticas

atividade_bp = Blueprint('atividade', __name__)

@atividade_bp.route('/', methods=['GET'])
def get_atividades():
    try:
        atividades = Atividade.query.all()
        return jsonify([atividade.to_dict() for atividade in atividades])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@atividade_bp.route('/<int:atividade_id>', methods=['GET'])
def get_atividade(atividade_id):
    try:
        atividade = Atividade.query.get_or_404(atividade_id)
        return jsonify(atividade.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@atividade_bp.route('/', methods=['POST'])
@professor_required
def create_atividade():
    try:
        data = request.get_json()
        descricao = data.get('descricao')
        prazo_entrega = data.get('prazo_entrega')
        tipo = data.get('tipo', 'individual')
        
        if not all([descricao, prazo_entrega]):
            return jsonify({'error': 'Descrição e prazo de entrega são obrigatórios'}), 400
        
        # Validar tipo de atividade
        tipos_validos = ['individual', 'grupo', 'upload', 'multipla_escolha']
        if tipo not in tipos_validos:
            return jsonify({'error': f'Tipo deve ser um dos seguintes: {", ".join(tipos_validos)}'}), 400
        
        # Converter string de data para datetime
        try:
            if 'T' in prazo_entrega:
                prazo_dt = datetime.fromisoformat(prazo_entrega.replace('Z', '+00:00'))
            else:
                prazo_dt = datetime.strptime(prazo_entrega, '%Y-%m-%d')
        except ValueError:
            return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD ou ISO format'}), 400
        
        nova_atividade = Atividade(
            descricao=descricao,
            prazo_entrega=prazo_dt,
            tipo=tipo
        )
        
        db.session.add(nova_atividade)
        db.session.flush()  # Para obter o ID da atividade
        
        # Criar entregas automáticas para atividades individuais e de múltipla escolha
        entregas_criadas = 0
        if tipo in ['individual', 'multipla_escolha']:
            entregas_criadas = criar_entregas_automaticas(nova_atividade)
        
        db.session.commit()
        
        # Enviar notificação sobre nova atividade
        try:
            from src.utils.notificacao_utils import notificar_nova_atividade
            notificar_nova_atividade(nova_atividade)
        except Exception as e:
            print(f"Erro ao enviar notificação: {e}")
        
        message = f'Atividade criada com sucesso'
        if entregas_criadas > 0:
            message += f' e {entregas_criadas} entregas automáticas foram geradas para os alunos'
        
        return jsonify({
            'success': True,
            'message': message,
            'atividade': nova_atividade.to_dict(),
            'entregas_criadas': entregas_criadas
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@atividade_bp.route('/<int:atividade_id>', methods=['PUT'])
def update_atividade(atividade_id):
    try:
        atividade = Atividade.query.get_or_404(atividade_id)
        data = request.get_json()
        
        if 'descricao' in data:
            atividade.descricao = data['descricao']
        if 'prazo_entrega' in data:
            try:
                if 'T' in data['prazo_entrega']:
                    atividade.prazo_entrega = datetime.fromisoformat(data['prazo_entrega'].replace('Z', '+00:00'))
                else:
                    atividade.prazo_entrega = datetime.strptime(data['prazo_entrega'], '%Y-%m-%d')
            except ValueError:
                return jsonify({'error': 'Formato de data inválido. Use YYYY-MM-DD'}), 400
        if 'tipo' in data:
            atividade.tipo = data['tipo']
        if 'status' in data:
            atividade.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Atividade atualizada com sucesso',
            'atividade': atividade.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@atividade_bp.route('/<int:atividade_id>', methods=['DELETE'])
def delete_atividade(atividade_id):
    try:
        atividade = Atividade.query.get_or_404(atividade_id)
        db.session.delete(atividade)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Atividade excluída com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@atividade_bp.route('/ativas', methods=['GET'])
def get_atividades_ativas():
    try:
        atividades = Atividade.query.filter_by(status='ativa').all()
        return jsonify([atividade.to_dict() for atividade in atividades])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
