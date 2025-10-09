"""
Decoradores de autenticação para o sistema AtivFlow
"""
from functools import wraps
from flask import session, jsonify, request

def login_required(f):
    """
    Decorador que exige sessão autenticada
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        return f(*args, **kwargs)
    return decorated_function

def professor_required(f):
    """
    Decorador que exige perfil de professor
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        if session.get('user_type') != 'professor':
            return jsonify({'error': 'Acesso negado. Apenas professores podem acessar esta funcionalidade'}), 403
        
        return f(*args, **kwargs)
    return decorated_function

def get_current_user_id():
    """
    Função utilitária para obter o ID do usuário atual da sessão
    """
    return session.get('user_id')

def get_current_user_type():
    """
    Função utilitária para obter o tipo do usuário atual da sessão
    """
    return session.get('user_type')

def is_professor():
    """
    Função utilitária para verificar se o usuário atual é professor
    """
    return session.get('user_type') == 'professor'

def is_aluno():
    """
    Função utilitária para verificar se o usuário atual é aluno
    """
    return session.get('user_type') == 'aluno'
