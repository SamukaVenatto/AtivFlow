"""
Utilitários de autenticação e decoradores de autorização
"""
from functools import wraps
from flask import session, jsonify, request
from app.models.usuario import Usuario

def login_required(f):
    """
    Decorator para rotas que requerem autenticação.
    Verifica se o usuário está logado via sessão.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'ok': False, 'error': 'Autenticação necessária'}), 401
        return f(*args, **kwargs)
    return decorated_function

def professor_required(f):
    """
    Decorator para rotas que requerem permissão de professor.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'ok': False, 'error': 'Autenticação necessária'}), 401
        
        user = Usuario.query.get(session['user_id'])
        if not user or user.tipo not in ['professor', 'admin']:
            return jsonify({'ok': False, 'error': 'Permissão de professor necessária'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """
    Decorator para rotas que requerem permissão de admin.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'ok': False, 'error': 'Autenticação necessária'}), 401
        
        user = Usuario.query.get(session['user_id'])
        if not user or user.tipo != 'admin':
            return jsonify({'ok': False, 'error': 'Permissão de admin necessária'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """
    Retorna o usuário atual da sessão ou None.
    """
    if 'user_id' in session:
        return Usuario.query.get(session['user_id'])
    return None

