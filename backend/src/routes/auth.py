from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.database_config import db
from src.models.aluno import Aluno
from src.models.professor import Professor

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        senha = data.get('senha')
        tipo_usuario = data.get('tipo_usuario', 'aluno')  # aluno ou professor
        
        if not email or not senha:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        if tipo_usuario == 'professor':
            usuario = Professor.query.filter_by(email=email).first()
        else:
            usuario = Aluno.query.filter_by(email=email).first()
        
        if usuario and check_password_hash(usuario.senha, senha):
            session['user_id'] = usuario.id
            session['user_type'] = tipo_usuario
            session['user_name'] = usuario.nome
            
            return jsonify({
                'success': True,
                'user': {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'tipo': tipo_usuario
                }
            })
        else:
            return jsonify({'error': 'Credenciais inválidas'}), 401
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Logout realizado com sucesso'})

@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    if 'user_id' not in session:
        return jsonify({'error': 'Usuário não autenticado'}), 401
    
    try:
        user_id = session['user_id']
        user_type = session['user_type']
        
        if user_type == 'professor':
            usuario = Professor.query.get(user_id)
        else:
            usuario = Aluno.query.get(user_id)
        
        if usuario:
            return jsonify({
                'user': {
                    'id': usuario.id,
                    'nome': usuario.nome,
                    'email': usuario.email,
                    'tipo': user_type
                }
            })
        else:
            return jsonify({'error': 'Usuário não encontrado'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/register/aluno', methods=['POST'])
def register_aluno():
    try:
        data = request.get_json()
        nome = data.get('nome')
        email = data.get('email')
        turma = data.get('turma')
        senha = data.get('senha')
        
        if not all([nome, email, turma, senha]):
            return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
        
        # Verificar se email já existe
        if Aluno.query.filter_by(email=email).first():
            return jsonify({'error': 'Email já cadastrado'}), 400
        
        # Criar novo aluno
        novo_aluno = Aluno(
            nome=nome,
            email=email,
            turma=turma,
            senha=generate_password_hash(senha)
        )
        
        db.session.add(novo_aluno)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Aluno cadastrado com sucesso',
            'aluno': novo_aluno.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
