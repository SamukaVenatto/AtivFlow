from flask import Blueprint, request, jsonify, session
from werkzeug.security import check_password_hash, generate_password_hash
from src.database_config import db
from src.models.aluno import Aluno
from src.models.professor import Professor
from src.utils.auth_decorators import login_required, get_current_user_id, get_current_user_type

configuracoes_bp = Blueprint('configuracoes', __name__)

@configuracoes_bp.route('/configuracoes/alterar-senha', methods=['PUT'])
@login_required
def alterar_senha():
    """
    Permite ao usuário alterar sua própria senha
    """
    try:
        data = request.get_json()
        
        senha_atual = data.get('senha_atual')
        nova_senha = data.get('nova_senha')
        confirmar_senha = data.get('confirmar_senha')
        
        # Validações
        if not senha_atual or not nova_senha or not confirmar_senha:
            return jsonify({'error': 'Todos os campos são obrigatórios'}), 400
        
        if nova_senha != confirmar_senha:
            return jsonify({'error': 'Nova senha e confirmação não coincidem'}), 400
        
        if len(nova_senha) < 6:
            return jsonify({'error': 'Nova senha deve ter pelo menos 6 caracteres'}), 400
        
        # Obter dados do usuário atual
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        # Buscar usuário no banco
        if user_type == 'aluno':
            usuario = Aluno.query.get(user_id)
        elif user_type == 'professor':
            usuario = Professor.query.get(user_id)
        else:
            return jsonify({'error': 'Tipo de usuário inválido'}), 400
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Verificar senha atual
        if not check_password_hash(usuario.senha, senha_atual):
            return jsonify({'error': 'Senha atual incorreta'}), 400
        
        # Atualizar senha
        usuario.senha = generate_password_hash(nova_senha)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Senha alterada com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@configuracoes_bp.route('/configuracoes/perfil', methods=['GET'])
@login_required
def obter_perfil():
    """
    Obtém dados do perfil do usuário atual
    """
    try:
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        if user_type == 'aluno':
            usuario = Aluno.query.get(user_id)
            perfil = {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'turma': usuario.turma,
                'status': usuario.status,
                'tipo_usuario': 'aluno',
                'created_at': usuario.created_at.isoformat() if usuario.created_at else None
            }
        elif user_type == 'professor':
            usuario = Professor.query.get(user_id)
            perfil = {
                'id': usuario.id,
                'nome': usuario.nome,
                'email': usuario.email,
                'tipo_usuario': 'professor',
                'created_at': usuario.created_at.isoformat() if usuario.created_at else None
            }
        else:
            return jsonify({'error': 'Tipo de usuário inválido'}), 400
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'success': True,
            'perfil': perfil
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@configuracoes_bp.route('/configuracoes/atualizar-perfil', methods=['PUT'])
@login_required
def atualizar_perfil():
    """
    Atualiza dados do perfil do usuário (exceto senha)
    """
    try:
        data = request.get_json()
        user_id = get_current_user_id()
        user_type = get_current_user_type()
        
        if user_type == 'aluno':
            usuario = Aluno.query.get(user_id)
            # Aluno pode atualizar apenas nome
            if 'nome' in data:
                usuario.nome = data['nome']
        elif user_type == 'professor':
            usuario = Professor.query.get(user_id)
            # Professor pode atualizar nome
            if 'nome' in data:
                usuario.nome = data['nome']
        else:
            return jsonify({'error': 'Tipo de usuário inválido'}), 400
        
        if not usuario:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Perfil atualizado com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
