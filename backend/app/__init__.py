"""
Inicialização da aplicação Flask
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

# Inicialização de extensões
db = SQLAlchemy()
migrate = Migrate()
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

def create_app(config_name='default'):
    """Factory para criar a aplicação Flask"""
    app = Flask(__name__)
    
    # Carregar configurações
    from app.config import config
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    
    # Definir origem permitida para o frontend no Render
    frontend_url = app.config.get("FRONTEND_URL", "https://ativflow-frontend.onrender.com")
    
    # Configurar CORS com domínio fixo e suporte a credenciais
    CORS(app, 
         resources={r"/*": {"origins": [frontend_url]}},
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization', 'X-CSRF-Token'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
    
    # Criar diretório de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Registrar blueprints (rotas)
    from app.routes import (
        auth, usuarios, atividades, entregas,
        grupos, questoes, followups, notificacoes, relatorios
    )
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(usuarios.bp)
    app.register_blueprint(atividades.bp)
    app.register_blueprint(entregas.bp)
    app.register_blueprint(grupos.bp)
    app.register_blueprint(questoes.bp)
    app.register_blueprint(followups.bp)
    app.register_blueprint(notificacoes.bp)
    app.register_blueprint(relatorios.bp)
    
    # Importar modelos para que o Flask-Migrate os reconheça
    with app.app_context():
        from app import models
        from app.models import Usuario

        # --- Criação automática de usuários de teste ---
        if not Usuario.query.filter_by(email="maria.santos@senac.edu.br").first():
            prof = Usuario(
                nome="Maria Santos",
                email="maria.santos@senac.edu.br",
                tipo="professor"
            )
            prof.set_password("Prof@123")
            db.session.add(prof)

        if not Usuario.query.filter_by(email="samuel.ribeiro@adm321530.com").first():
            aluno = Usuario(
                nome="Samuel Ribeiro",
                email="samuel.ribeiro@adm321530.com",
                tipo="aluno"
            )
            aluno.set_password("Aluno@123")
            db.session.add(aluno)

        db.session.commit()
        print("Usuários de teste verificados/criados com sucesso.")

    return app
