"""
Configurações de fixtures para testes Pytest
"""
import pytest
from app import create_app, db
from app.models.usuario import Usuario
from datetime import datetime

@pytest.fixture(scope=\'module\')
def test_app():
    """Fixture para criar uma instância da aplicação Flask para testes."""
    app = create_app(\'development\')
    app.config.update({
        \'TESTING\': True,
        \'SQLALCHEMY_DATABASE_URI\': \'sqlite:///:memory:\'  # Usar banco de dados em memória para testes
    })
    
    with app.app_context():
        db.create_all()  # Criar tabelas no banco de dados em memória
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope=\'module\')
def test_client(test_app):
    """Fixture para obter um cliente de teste da aplicação."""
    return test_app.test_client()

@pytest.fixture(scope=\'module\')
def init_database(test_app):
    """
    Fixture para inicializar o banco de dados com dados básicos para testes.
    Cria um professor e um aluno de teste.
    """
    with test_app.app_context():
        # Criar professor
        professor = Usuario(
            nome_completo=\'Professor Teste\',
            email=\'professor@test.com\',
            tipo=\'professor\',
            curso=\'Administração\',
            turma=\'TESTE101\',
            status=\'ativo\'
        )
        professor.set_password(\'testpass\')
        db.session.add(professor)
        db.session.commit()

        # Criar aluno
        aluno = Usuario(
            nome_completo=\'Aluno Teste\',
            email=\'aluno@test.com\',
            tipo=\'aluno\',
            curso=\'Administração\',
            turma=\'TESTE101\',
            status=\'ativo\'
        )
        aluno.set_password(\'testpass\')
        db.session.add(aluno)
        db.session.commit()

        yield db  # Retorna a instância do db para uso nos testes

        # Limpar dados após os testes (opcional, já que o banco é em memória)
        db.session.query(Usuario).delete()
        db.session.commit()

@pytest.fixture(scope=\'module\')
def auth_headers_professor(test_client, init_database):
    """
    Fixture para obter headers de autenticação para um professor de teste.
    Realiza o login e retorna os cookies de sessão.
    """
    response = test_client.post(
        \'/api/auth/login\',
        json={\'email\': \'professor@test.com\', \'senha\': \'testpass\'}
    )
    assert response.status_code == 200
    return {\'Cookie\': response.headers[\'Set-Cookie\']}

@pytest.fixture(scope=\'module\')
def auth_headers_aluno(test_client, init_database):
    """
    Fixture para obter headers de autenticação para um aluno de teste.
    Realiza o login e retorna os cookies de sessão.
    """
    response = test_client.post(
        \'/api/auth/login\',
        json={\'email\': \'aluno@test.com\', \'senha\': \'testpass\'}
    )
    assert response.status_code == 200
    return {\'Cookie\': response.headers[\'Set-Cookie\']}

