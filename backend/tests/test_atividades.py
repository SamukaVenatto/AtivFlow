"""
Testes para as rotas de atividades
"""
from app.models.atividade import Atividade
from app.models.usuario import Usuario
from app import db
from datetime import datetime, timedelta

def test_criar_atividade_success(test_client, auth_headers_professor, init_database):
    """
    Testa a criação de uma nova atividade por um professor.
    """
    with test_client.application.app_context():
        professor = Usuario.query.filter_by(email=\'professor@test.com\').first()
        response = test_client.post(
            \'/api/atividades/\',
            headers=auth_headers_professor,
            json={
                \'titulo\': \'Nova Atividade Teste\',
                \'descricao\': \'Descrição da atividade de teste\',
                \'tipo\': \'individual\',
                \'prazo\': (datetime.utcnow() + timedelta(days=7)).isoformat() + \'Z\',
                \'turma\': \'TESTE101\'
            }
        )
        assert response.status_code == 201
        assert response.json[\'ok\'] is True
        assert \'atividade\' in response.json
        assert response.json[\'atividade\'][\'titulo\'] == \'Nova Atividade Teste\'

def test_listar_atividades_professor(test_client, auth_headers_professor, init_database):
    """
    Testa a listagem de atividades por um professor.
    """
    # Criar uma atividade para garantir que haja algo para listar
    with test_client.application.app_context():
        professor = Usuario.query.filter_by(email=\'professor@test.com\').first()
        atividade = Atividade(
            titulo=\'Atividade Listagem Teste\',
            descricao=\'Descrição\',
            tipo=\'individual\',
            prazo=datetime.utcnow() + timedelta(days=10),
            criado_por=professor.id,
            turma=\'TESTE101\'
        )
        db.session.add(atividade)
        db.session.commit()

    response = test_client.get(\'/api/atividades/\', headers=auth_headers_professor)
    assert response.status_code == 200
    assert response.json[\'ok\'] is True
    assert \'atividades\' in response.json
    assert len(response.json[\'atividades\']) >= 1

def test_listar_atividades_aluno(test_client, auth_headers_aluno, init_database):
    """
    Testa a listagem de atividades por um aluno (apenas as da sua turma).
    """
    # Criar uma atividade para a turma do aluno
    with test_client.application.app_context():
        professor = Usuario.query.filter_by(email=\'professor@test.com\').first()
        atividade_aluno = Atividade(
            titulo=\'Atividade Aluno Teste\',
            descricao=\'Descrição\',
            tipo=\'individual\',
            prazo=datetime.utcnow() + timedelta(days=10),
            criado_por=professor.id,
            turma=\'TESTE101\'
        )
        db.session.add(atividade_aluno)
        
        # Criar uma atividade para outra turma
        atividade_outra_turma = Atividade(
            titulo=\'Atividade Outra Turma\',
            descricao=\'Descrição\',
            tipo=\'individual\',
            prazo=datetime.utcnow() + timedelta(days=10),
            criado_por=professor.id,
            turma=\'OUTRA_TURMA\'
        )
        db.session.add(atividade_outra_turma)
        db.session.commit()

    response = test_client.get(\'/api/atividades/\', headers=auth_headers_aluno)
    assert response.status_code == 200
    assert response.json[\'ok\'] is True
    assert \'atividades\' in response.json
    assert len(response.json[\'atividades\']) == 1 # Deve ver apenas a atividade da sua turma
    assert response.json[\'atividades\'][0][\'titulo\'] == \'Atividade Aluno Teste\'

def test_obter_atividade_success(test_client, auth_headers_professor, init_database):
    """
    Testa a obtenção de detalhes de uma atividade específica.
    """
    with test_client.application.app_context():
        professor = Usuario.query.filter_by(email=\'professor@test.com\').first()
        atividade = Atividade(
            titulo=\'Atividade Detalhe Teste\',
            descricao=\'Descrição\',
            tipo=\'individual\',
            prazo=datetime.utcnow() + timedelta(days=10),
            criado_por=professor.id,
            turma=\'TESTE101\'
        )
        db.session.add(atividade)
        db.session.commit()
        atividade_id = atividade.id

    response = test_client.get(f\'/api/atividades/{atividade_id}\\' , headers=auth_headers_professor)
    assert response.status_code == 200
    assert response.json[\'ok\'] is True
    assert response.json[\'atividade\'][\'titulo\'] == \'Atividade Detalhe Teste\'

def test_atualizar_atividade_success(test_client, auth_headers_professor, init_database):
    """
    Testa a atualização de uma atividade existente.
    """
    with test_client.application.app_context():
        professor = Usuario.query.filter_by(email=\'professor@test.com\').first()
        atividade = Atividade(
            titulo=\'Atividade para Atualizar\',
            descricao=\'Descrição antiga\',
            tipo=\'individual\',
            prazo=datetime.utcnow() + timedelta(days=10),
            criado_por=professor.id,
            turma=\'TESTE101\'
        )
        db.session.add(atividade)
        db.session.commit()
        atividade_id = atividade.id

    response = test_client.put(
        f\'/api/atividades/{atividade_id}\\' ,
        headers=auth_headers_professor,
        json={\'descricao\': \'Nova descrição atualizada\', \'ativo\': False}
    )
    assert response.status_code == 200
    assert response.json[\'ok\'] is True
    assert response.json[\'atividade\'][\'descricao\'] == \'Nova descrição atualizada\'
    assert response.json[\'atividade\'][\'ativo\'] is False

def test_deletar_atividade_success(test_client, auth_headers_professor, init_database):
    """
    Testa a inativação de uma atividade.
    """
    with test_client.application.app_context():
        professor = Usuario.query.filter_by(email=\'professor@test.com\').first()
        atividade = Atividade(
            titulo=\'Atividade para Deletar\',
            descricao=\'Descrição\',
            tipo=\'individual\',
            prazo=datetime.utcnow() + timedelta(days=10),
            criado_por=professor.id,
            turma=\'TESTE101\'
        )
        db.session.add(atividade)
        db.session.commit()
        atividade_id = atividade.id

    response = test_client.delete(f\'/api/atividades/{atividade_id}\\' , headers=auth_headers_professor)
    assert response.status_code == 200
    assert response.json[\'ok\'] is True
    assert \'message\' in response.json
    assert \'Atividade inativada com sucesso\' in response.json[\'message\']

    with test_client.application.app_context():
        inactivated_atividade = Atividade.query.get(atividade_id)
        assert inactivated_atividade.ativo is False

