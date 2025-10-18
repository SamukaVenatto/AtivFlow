"""
Testes para as rotas de usuários (alunos)
"""
from app.models.usuario import Usuario
from app import db

def test_criar_aluno_success(test_client, auth_headers_professor):
    """
    Testa a criação de um novo aluno por um professor.
    """
    response = test_client.post(
        '/api/alunos/',
        headers=auth_headers_professor,
        json={
            'nome_completo': 'Novo Aluno Teste',
            'curso': 'Logística',
            'turma': 'TESTE101',
            'senha': 'Aluno@Test123'
        }
    )
    assert response.status_code == 201
    assert response.json['ok'] is True
    assert 'aluno' in response.json
    assert response.json['aluno']['nome_completo'] == 'Novo Aluno Teste'
    assert 'novo.aluno.teste@logteste101.com' in response.json['aluno']['email']

def test_criar_aluno_missing_fields(test_client, auth_headers_professor):
    """
    Testa a criação de aluno com campos faltando.
    """
    response = test_client.post(
        '/api/alunos/',
        headers=auth_headers_professor,
        json={
            'nome_completo': 'Aluno Incompleto',
            'curso': 'Logística'
        }
    )
    assert response.status_code == 400
    assert response.json['ok'] is False
    assert 'Campo turma é obrigatório' in response.json['error']

def test_criar_aluno_email_exists(test_client, auth_headers_professor):
    """
    Testa a criação de aluno com e-mail já existente.
    """
    # Primeiro cria um aluno
    test_client.post(
        '/api/alunos/',
        headers=auth_headers_professor,
        json={
            'nome_completo': 'Aluno Existente',
            'curso': 'Administração',
            'turma': 'TESTE101',
            'senha': 'Aluno@Test123'
        }
    )

    # Tenta criar outro com o mesmo nome, curso e turma (gerará o mesmo e-mail)
    response = test_client.post(
        '/api/alunos/',
        headers=auth_headers_professor,
        json={
            'nome_completo': 'Aluno Existente',
            'curso': 'Administração',
            'turma': 'TESTE101',
            'senha': 'Aluno@Test123'
        }
    )
    assert response.status_code == 400
    assert response.json['ok'] is False
    assert 'E-mail já cadastrado' in response.json['error']

def test_listar_alunos_professor(test_client, auth_headers_professor, init_database):
    """
    Testa a listagem de alunos por um professor.
    """
    response = test_client.get('/api/alunos/', headers=auth_headers_professor)
    assert response.status_code == 200
    assert response.json['ok'] is True
    assert 'alunos' in response.json
    assert len(response.json['alunos']) >= 1 # Deve haver pelo menos o aluno de teste

def test_listar_alunos_aluno_forbidden(test_client, auth_headers_aluno):
    """
    Testa se um aluno não pode listar todos os alunos.
    """
    response = test_client.get('/api/alunos/', headers=auth_headers_aluno)
    assert response.status_code == 403 # Acesso negado

def test_obter_aluno_success(test_client, auth_headers_professor, init_database):
    """
    Testa a obtenção de detalhes de um aluno específico por um professor.
    """
    with test_client.application.app_context():
        aluno = Usuario.query.filter_by(email='aluno@test.com').first()
        response = test_client.get(f'/api/alunos/{aluno.id}', headers=auth_headers_professor)
        assert response.status_code == 200
        assert response.json['ok'] is True
        assert response.json['aluno']['email'] == 'aluno@test.com'

def test_atualizar_aluno_success(test_client, auth_headers_professor, init_database):
    """
    Testa a atualização de um aluno por um professor.
    """
    with test_client.application.app_context():
        aluno = Usuario.query.filter_by(email='aluno@test.com').first()
        response = test_client.put(
            f'/api/alunos/{aluno.id}',
            headers=auth_headers_professor,
            json={'status': 'inativo'}
        )
        assert response.status_code == 200
        assert response.json['ok'] is True
        assert response.json['aluno']['status'] == 'inativo'
        
        # Verifica no banco
        updated_aluno = Usuario.query.get(aluno.id)
        assert updated_aluno.status == 'inativo'

def test_deletar_aluno_success(test_client, auth_headers_professor, init_database):
    """
    Testa a inativação de um aluno por um professor.
    """
    with test_client.application.app_context():
        aluno = Usuario.query.filter_by(email='aluno@test.com').first()
        response = test_client.delete(f'/api/alunos/{aluno.id}', headers=auth_headers_professor)
        assert response.status_code == 200
        assert response.json['ok'] is True
        assert 'Aluno inativado com sucesso' in response.json['message']
        
        # Verifica no banco
        inactivated_aluno = Usuario.query.get(aluno.id)
        assert inactivated_aluno.status == 'inativo'

