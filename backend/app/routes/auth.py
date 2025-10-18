"""
Rotas de autenticação
"""
from flask import Blueprint, request, jsonify, session
from datetime import datetime
from app import db, limiter
from app.models.usuario import Usuario
from app.utils.auth import login_required, get_current_user

bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@bp.route('/login', methods=['POST'])
@limiter.limit("5 per 10 minutes")  # Rate limiting: 5 tentativas por 10 minutos
def login():
    """
    Endpoint de login com sessão por cookie HTTPOnly.
    
    Decisão de design: Usamos sessão server-side com cookie HTTPOnly ao invés de JWT
    por maior segurança contra XSS attacks. O cookie é marcado como HttpOnly, Secure
    (em produção) e SameSite=Strict para proteção contra CSRF.
    """
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('senha'):
        return jsonify({'ok': False, 'error': 'Email e senha são obrigatórios'}), 400
    
    # Buscar usuário
    usuario = Usuario.query.filter_by(email=data['email']).first()
    
    if not usuario or not usuario.check_password(data['senha']):
        return jsonify({'ok': False, 'error': 'Credenciais inválidas'}), 401
    
    # Verificar se usuário está ativo
    if usuario.status != 'ativo':
        return jsonify({'ok': False, 'error': 'Usuário inativo'}), 403
    
    # Criar sessão
    session['user_id'] = usuario.id
    session['user_tipo'] = usuario.tipo
    session.permanent = True
    
    # Atualizar último login
    usuario.ultimo_login = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'ok': True,
        'user': usuario.to_dict()
    }), 200

@bp.route('/logout', methods=['POST'])
@login_required
def logout():
    """Endpoint de logout"""
    session.clear()
    return jsonify({'ok': True, 'message': 'Logout realizado com sucesso'}), 200

@bp.route('/me', methods=['GET'])
@login_required
def me():
    """Retorna informações do usuário atual"""
    usuario = get_current_user()
    
    if not usuario:
        return jsonify({'ok': False, 'error': 'Usuário não encontrado'}), 404
    
    return jsonify({
        'ok': True,
        'user': usuario.to_dict()
    }), 200

@bp.route('/check', methods=['GET'])
def check():
    """Verifica se o usuário está autenticado"""
    if 'user_id' in session:
        usuario = get_current_user()
        if usuario:
            return jsonify({
                'ok': True,
                'authenticated': True,
                'user': usuario.to_dict()
            }), 200
    
    return jsonify({
        'ok': True,
        'authenticated': False
    }), 200

