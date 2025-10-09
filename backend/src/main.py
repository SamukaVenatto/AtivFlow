import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from werkzeug.security import generate_password_hash

# Importar configuração do banco
from src.database_config import db
from flask_migrate import Migrate  # ✅ Importado após Flask, mas antes de app

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'ativflow-senac-321530-secret-key'

# Habilitar CORS
CORS(app)

# Configuração do banco de dados
db_url = os.getenv("DATABASE_URL", None)
if db_url:
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
else:
    database_path = os.path.join(os.path.dirname(__file__), "database", "app.db")
    os.makedirs(os.path.dirname(database_path), exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{database_path}"

app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_size": 10,
    "max_overflow": 5,
    "pool_timeout": 30
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensões
db.init_app(app)
migrate = Migrate(app, db)  # ✅ Agora app e db já existem

# Importar modelos (para registrar no SQLAlchemy)
from src.models.aluno import Aluno
from src.models.atividade import Atividade
from src.models.entrega import Entrega
from src.models.grupo import Grupo, GrupoIntegrante
from src.models.professor import Professor
from src.models.follow_up import FollowUp  # ✅ Modelo registrado
from src.models.questao import Questao, RespostaAluno  # ✅ Novos modelos
from src.models.notificacao import Notificacao  # ✅ Sistema de notificações

# Importar blueprints
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.aluno import aluno_bp
from src.routes.atividade import atividade_bp
from src.routes.entrega import entrega_bp
from src.routes.grupo import grupo_bp
from src.routes.dashboard import dashboard_bp
from src.routes.follow_up import follow_up_bp  # ✅ Só uma vez
from src.routes.questao import questao_bp  # ✅ Novo blueprint
from src.routes.notificacao import notificacao_bp  # ✅ Sistema de notificações
from src.routes.configuracoes import configuracoes_bp  # ✅ Sistema de configurações

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix="/api")
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(aluno_bp, url_prefix="/api/alunos")
app.register_blueprint(atividade_bp, url_prefix="/api/atividades")
app.register_blueprint(entrega_bp, url_prefix="/api/entregas")
app.register_blueprint(grupo_bp, url_prefix="/api/grupos")
app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
app.register_blueprint(follow_up_bp, url_prefix="/api")  # ✅ Só uma vez, com prefixo
app.register_blueprint(questao_bp, url_prefix="/api")  # ✅ Novo blueprint
app.register_blueprint(notificacao_bp, url_prefix="/api")  # ✅ Sistema de notificações
app.register_blueprint(configuracoes_bp, url_prefix="/api")  # ✅ Sistema de configurações

def init_database():
    """⚠️ Só use em desenvolvimento! Apaga e recria o banco."""
    with app.app_context():
        db.drop_all()
        db.create_all()
        db.session.commit()

        # Dados iniciais (opcional)
        try:
            from src.models.professor import Professor
            from src.models.aluno import Aluno
            from src.models.atividade import Atividade
            from datetime import datetime, timedelta

            if not Professor.query.filter_by(email='professor@senac.com').first():
                professor = Professor(
                    nome='Professor SENAC',
                    email='professor@senac.com',
                    senha=generate_password_hash('123456')
                )
                db.session.add(professor)

            alunos_iniciais = [
                {"nome": "João Silva", "email": "joao@aluno.com", "turma": "321530", "status": "ativo"},
                {"nome": "Maria Souza", "email": "maria@aluna.com", "turma": "321530", "status": "ativo"}
            ]
            for aluno_data in alunos_iniciais:
                if not Aluno.query.filter_by(email=aluno_data['email']).first():
                    novo_aluno = Aluno(
                        nome=aluno_data['nome'],
                        email=aluno_data['email'],
                        turma=aluno_data['turma'],
                        status=aluno_data.get('status', 'ativo'),
                        senha=generate_password_hash('123456')
                    )
                    db.session.add(novo_aluno)

            atividades_iniciais = [
                {'descricao': 'Projeto Final - Sistema Web', 'tipo': 'grupo', 'prazo': datetime.now() + timedelta(days=30)},
                {'descricao': 'Exercício de HTML/CSS', 'tipo': 'individual', 'prazo': datetime.now() + timedelta(days=7)},
                {'descricao': 'Apresentação do Projeto', 'tipo': 'grupo', 'prazo': datetime.now() + timedelta(days=45)}
            ]
            for ativ_data in atividades_iniciais:
                if not Atividade.query.filter_by(descricao=ativ_data['descricao']).first():
                    nova_atividade = Atividade(
                        descricao=ativ_data['descricao'],
                        tipo=ativ_data['tipo'],
                        prazo_entrega=ativ_data['prazo']
                    )
                    db.session.add(nova_atividade)

            db.session.commit()
            print("\033[92m✅ Banco de dados recriado e populado com sucesso!\033[0m")
        except Exception as e:
            print(f"\033[93m⚠️ Erro ao inicializar dados: {e}\033[0m")

# Rotas de SPA
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if not static_folder_path:
        return "Static folder not configured", 404
    full_path = os.path.join(static_folder_path, path)
    if path != "" and os.path.exists(full_path):
        return send_from_directory(static_folder_path, path)
    index_path = os.path.join(static_folder_path, 'index.html')
    if os.path.exists(index_path):
        return send_from_directory(static_folder_path, 'index.html')
    return "index.html not found", 404

# Inicializar banco (só em desenvolvimento!)
if os.getenv("FLASK_ENV") != "production":
    init_database()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=(os.getenv("FLASK_ENV") != "production"))