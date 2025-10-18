"""
Testes para as rotas de autenticação (auth.py)
"""

def test_login_success(test_client, init_database):
    """
    Testa o login bem-sucedido de um usuário.
    """
    response = test_client.post(
        '/api/auth/login',
        json={'email': 'professor@test.com', 'senha': 'testpass'}
    )
    assert response.status_code == 200
    assert response.json['ok'] is True
    assert 'user' in response.json
    assert 'Set-Cookie' in response.headers

def test_login_invalid_credentials(test_client, init_database):
    """
    Testa o login com credenciais inválidas.
    """
    response = test_client.post(
        '/api/auth/login',
        json={'email': 'professor@test.com', 'senha': 'wrongpass'}
    )
    assert response.status_code == 401
    assert response.json['ok'] is False
    assert 'error' in response.json

def test_login_missing_fields(test_client, init_database):
    """
    Testa o login com campos faltando.
    """
    response = test_client.post(
        '/api/auth/login',
        json={'email': 'professor@test.com'}
    )
    assert response.status_code == 400
    assert response.json['ok'] is False
    assert 'error' in response.json

def test_logout(test_client, auth_headers_professor):
    """
    Testa o logout de um usuário autenticado.
    """
    response = test_client.post('/api/auth/logout', headers=auth_headers_professor)
    assert response.status_code == 200
    assert response.json['ok'] is True
    assert 'message' in response.json

def test_me_authenticated(test_client, auth_headers_professor):
    """
    Testa a rota /me para um usuário autenticado.
    """
    response = test_client.get('/api/auth/me', headers=auth_headers_professor)
    assert response.status_code == 200
    assert response.json['ok'] is True
    assert 'user' in response.json
    assert response.json['user']['email'] == 'professor@test.com'

def test_me_unauthenticated(test_client):
    """
    Testa a rota /me para um usuário não autenticado.
    """
    response = test_client.get('/api/auth/me')
    assert response.status_code == 401
    assert response.json['ok'] is False

def test_check_authenticated(test_client, auth_headers_professor):
    """
    Testa a rota /check para um usuário autenticado.
    """
    response = test_client.get('/api/auth/check', headers=auth_headers_professor)
    assert response.status_code == 200
    assert response.json['ok'] is True
    assert response.json['authenticated'] is True
    assert 'user' in response.json

def test_check_unauthenticated(test_client):
    """
    Testa a rota /check para um usuário não autenticado.
    """
    response = test_client.get('/api/auth/check')
    assert response.status_code == 200
    assert response.json['ok'] is True
    assert response.json['authenticated'] is False

