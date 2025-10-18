"""
Testes para os modelos do SQLAlchemy
"""
from app.models.usuario import Usuario
from app import db

def test_usuario_password_hashing(test_app):
    """
    Testa se a senha do usuário é corretamente hashed e verificada.
    """
    with test_app.app_context():
        user = Usuario(
            nome_completo=\'Teste User\',
            email=\'test@example.com\',
            tipo=\'aluno\'
        )
        user.set_password(\'mysecretpassword\')
        db.session.add(user)
        db.session.commit()

        retrieved_user = Usuario.query.filter_by(email=\'test@example.com\').first()
        assert retrieved_user is not None
        assert retrieved_user.check_password(\'mysecretpassword\') is True
        assert retrieved_user.check_password(\'wrongpassword\') is False
        assert retrieved_user.senha_hash is not None
        assert retrieved_user.senha_hash != \'mysecretpassword\'

def test_usuario_to_dict(test_app):
    """
    Testa a serialização do modelo Usuario para dicionário.
    """
    with test_app.app_context():
        user = Usuario(
            nome_completo=\'Outro Teste\',
            email=\'outro@example.com\',
            tipo=\'professor\',
            curso=\'Matemática\',
            turma=\'202\'
        )
        user.set_password(\'outrasenha\')
        db.session.add(user)
        db.session.commit()

        user_dict = user.to_dict()
        assert user_dict[\'nome_completo\'] == \'Outro Teste\'
        assert user_dict[\'email\'] == \'outro@example.com\'
        assert user_dict[\'tipo\'] == \'professor\'
        assert \'senha_hash\' not in user_dict # Não deve expor o hash da senha

