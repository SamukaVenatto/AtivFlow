from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash
from src.database_config import db
from src.models.aluno import Aluno
from src.utils.auth_decorators import professor_required
from src.utils.entrega_utils import criar_entrega_para_novo_aluno

aluno_bp = Blueprint('aluno', __name__)

@aluno_bp.route('/', methods=['GET'])
def get_alunos():
    try:
        alunos = Aluno.query.all()
        return jsonify([aluno.to_dict() for aluno in alunos])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/<int:aluno_id>', methods=['GET'])
def get_aluno(aluno_id):
    try:
        aluno = Aluno.query.get_or_404(aluno_id)
        return jsonify(aluno.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/', methods=['POST'])
@professor_required
def create_aluno():
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        turma = data.get('turma')
        senha = data.get('senha', '123456')  # senha padrão
        status = data.get('status', 'ativo')
        
        if not all([nome, email, turma]):
            return jsonify({'error': 'Nome, email e turma são obrigatórios'}), 400
        
        # Verificar se email já existe
        if Aluno.query.filter_by(email=email).first():
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        novo_aluno = Aluno(
            nome=nome,
            email=email,
            turma=turma,
            status=status,
            senha=generate_password_hash(senha)
        )
        
        db.session.add(novo_aluno)
        db.session.flush()  # Para obter o ID do aluno
        
        # Criar entregas automáticas para atividades individuais ativas
        entregas_criadas = 0
        if status == 'ativo':
            entregas_criadas = criar_entrega_para_novo_aluno(novo_aluno.id)
        
        db.session.commit()
        
        message = 'Aluno criado com sucesso'
        if entregas_criadas > 0:
            message += f' e {entregas_criadas} entregas automáticas foram geradas'
        
        return jsonify({
            'success': True,
            'message': message,
            'aluno': novo_aluno.to_dict(),
            'entregas_criadas': entregas_criadas
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/<int:aluno_id>', methods=['PUT'])
def update_aluno(aluno_id):
    try:
        aluno = Aluno.query.get_or_404(aluno_id)
        data = request.get_json()
        
        if 'nome' in data:
            aluno.nome = data['nome']
        if 'email' in data:
            # Verificar se novo email já existe
            if data['email'] != aluno.email and Aluno.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Email já cadastrado'}), 400
            aluno.email = data['email']
        if 'turma' in data:
            aluno.turma = data['turma']
        if 'status' in data:
            aluno.status = data['status']
        if 'senha' in data:
            aluno.senha = generate_password_hash(data['senha'])
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Aluno atualizado com sucesso',
            'aluno': aluno.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/<int:aluno_id>', methods=['DELETE'])
def delete_aluno(aluno_id):
    try:
        aluno = Aluno.query.get_or_404(aluno_id)
        db.session.delete(aluno)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Aluno excluído com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@aluno_bp.route('/turmas', methods=['GET'])
def get_turmas():
    try:
        turmas = db.session.query(Aluno.turma).distinct().all()
        return jsonify([turma[0] for turma in turmas])
    except Exception as e:
        return jsonify({'error': str(e)}), 500
