# backend/src/main.py

import os
from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

# Importações relativas
from .database_config import db

def create_app():
    static_folder = os.path.join(os.path.dirname(__file__), 'static')
    app = Flask(__name__, static_folder=static_folder)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'ativflow-senac-321530-secret-key')
    CORS(app)

    # Banco de dados
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    else:
        database_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
        os.makedirs(os.path.dirname(database_path), exist_ok=True)
        app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{database_path}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    
    return app

app = create_app()

# Importar modelos e rotas (após db.init_app)
from .models.professor import Professor
from .models.atividade import Atividade
from .models.aluno import Aluno  
from .models.entrega import Entrega
from .models.grupo import Grupo, GrupoIntegrante

# Importar blueprints
from .routes.user import user_bp
from .routes.auth import auth_bp
from .routes.aluno import aluno_bp
from .routes.atividade import atividade_bp
from .routes.entrega import entrega_bp
from .routes.grupo import grupo_bp
from .routes.dashboard import dashboard_bp
from .routes.professor import professor_bp

# Registrar blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(aluno_bp, url_prefix='/api/alunos')
app.register_blueprint(atividade_bp, url_prefix='/api/atividades')
app.register_blueprint(entrega_bp, url_prefix='/api/entregas')
app.register_blueprint(grupo_bp, url_prefix='/api/grupos')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(professor_bp, url_prefix='/api/professor')

# === NOVAS ROTAS DE AUTENTICAÇÃO ===

@app.route('/primeiro-acesso')
def pagina_primeiro_acesso():
    return send_from_directory(app.static_folder, 'primeiro-acesso.html')

@app.route('/api/auth/primeiro-acesso', methods=['POST'])
def primeiro_acesso():
    data = request.get_json()
    email = data.get('email')
    nova_senha = data.get('senha')

    if not email or not nova_senha:
        return jsonify({"erro": "E-mail e senha são obrigatórios"}), 400

    aluno = Aluno.query.filter_by(email=email).first()
    if not aluno:
        return jsonify({"erro": "Aluno não encontrado"}), 404

    # Verifica se ainda está com senha padrão
    if not check_password_hash(aluno.senha, '123456'):
        return jsonify({"erro": "Este aluno já definiu uma senha"}), 403

    aluno.senha = generate_password_hash(nova_senha)
    aluno.senha_definida = True
    db.session.commit()
    return jsonify({"sucesso": "Senha definida com sucesso! Você já pode fazer login."}), 200

@app.route('/api/auth/alterar-senha', methods=['POST'])
def alterar_senha():
    data = request.get_json()
    email = data.get('email')
    senha_atual = data.get('senha_atual')
    nova_senha = data.get('nova_senha')

    aluno = Aluno.query.filter_by(email=email).first()
    if not aluno or not aluno.verificar_senha(senha_atual):
        return jsonify({"erro": "Credenciais inválidas"}), 401

    aluno.set_senha(nova_senha)
    db.session.commit()
    return jsonify({"sucesso": "Senha alterada com sucesso!"}), 200

# === FIM DAS NOVAS ROTAS ===

def init_database():
    with app.app_context():
        db.create_all()

        # Professor padrão
        professor = Professor.query.filter_by(email='professor@senac.com').first()
        if not professor:
            professor = Professor(
                nome='Professor SENAC',
                email='professor@senac.com',
                senha='123456'  # Será hasheado automaticamente
            )
            db.session.add(professor)
            db.session.commit()
            print("✅ Professor padrão criado")

        # Alunos de exemplo
        alunos_exemplo = [
            {'nome': 'João Silva', 'email': 'joao@aluno.com', 'turma': '321530'},
            {'nome': 'Maria Santos', 'email': 'maria@aluno.com', 'turma': '321530'},
            {'nome': 'Pedro Costa', 'email': 'pedro@aluno.com', 'turma': '321530'},
            {'nome': 'Ana Oliveira', 'email': 'ana@aluno.com', 'turma': '321530'},
            {'nome': 'Carlos Ferreira', 'email': 'carlos@aluno.com', 'turma': '321530'}
        ]
        for aluno_data in alunos_exemplo:
            if not Aluno.query.filter_by(email=aluno_data['email']).first():
                aluno = Aluno(
                    nome=aluno_data['nome'],
                    email=aluno_data['email'],
                    turma=aluno_data['turma'],
                    senha=generate_password_hash('123456')
                )
                db.session.add(aluno)
        db.session.commit()
        print("✅ Alunos de exemplo criados")

        # Atividades de exemplo (somente se professor existir)
        professor = Professor.query.filter_by(email='professor@senac.com').first()
        if professor:
            atividades_exemplo = [
                {
                    'titulo': 'Projeto Final - Sistema Web',
                    'descricao': 'Desenvolver um sistema web completo utilizando Flask e React',
                    'formato': 'upload',
                    'tipo': 'grupo',
                    'prazo': datetime.now() + timedelta(days=30)
                },
                {
                    'titulo': 'Exercício de HTML/CSS',
                    'descricao': 'Criar uma página web responsiva utilizando HTML5 e CSS3',
                    'formato': 'texto',
                    'tipo': 'individual',
                    'prazo': datetime.now() + timedelta(days=7)
                },
                {
                    'titulo': 'Apresentação do Projeto',
                    'descricao': 'Apresentar o projeto final desenvolvido durante o semestre',
                    'formato': 'multipla_escolha',
                    'tipo': 'grupo',
                    'prazo': datetime.now() + timedelta(days=45)
                }
            ]
            for ativ_data in atividades_exemplo:
                if not Atividade.query.filter_by(titulo=ativ_data['titulo']).first():
                    atividade = Atividade(
                        titulo=ativ_data['titulo'],
                        descricao=ativ_data['descricao'],
                        formato=ativ_data['formato'],
                        tipo=ativ_data['tipo'],
                        prazo_entrega=ativ_data['prazo'],
                        professor_id=professor.id,
                        criterios_avaliacao='Critérios a serem definidos'
                    )
                    db.session.add(atividade)
            db.session.commit()
            print("✅ Atividades de exemplo criadas")

        print("✅ Banco de dados inicializado com dados de exemplo.")

# Inicializa só em desenvolvimento
if not os.environ.get('DATABASE_URL'):
    try:
        init_database()
    except Exception as e:
        print(f"⚠️ Aviso: Não foi possível inicializar o banco: {e}")

# Servir frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder = app.static_folder
    if not static_folder:
        return "Static folder not configured", 404

    full_path = os.path.join(static_folder, path)
    if path != "" and os.path.exists(full_path):
        return send_from_directory(static_folder, path)
    else:
        index_path = os.path.join(static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder, 'index.html')
        else:
            return "index.html not found", 404

# Rota temporária para PostgreSQL (plano gratuito)
@app.route('/init-db')
def init_db_route():
    try:
        with app.app_context():
            db.create_all()
        return "✅ Banco de dados inicializado com sucesso!", 200
    except Exception as e:
        return f"❌ Erro ao inicializar o banco: {str(e)}", 500

# Execução local
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = not os.environ.get('DATABASE_URL')
    app.run(host='0.0.0.0', port=port, debug=debug)

@app.route('/init-dados')
def init_dados():
    try:
        with app.app_context():
            # Professor padrão
            if not Professor.query.filter_by(email='professor@senac.com').first():
                professor = Professor(
                    nome='Professor SENAC',
                    email='professor@senac.com',
                    senha=generate_password_hash('123456')
                )
                db.session.add(professor)
            
            # Alunos de exemplo
            alunos_exemplo = [
                {'nome': 'João Silva', 'email': 'joao@aluno.com', 'turma': '321530'},
                {'nome': 'Maria Santos', 'email': 'maria@aluno.com', 'turma': '321530'},
                {'nome': 'Pedro Costa', 'email': 'pedro@aluno.com', 'turma': '321530'},
                {'nome': 'Ana Oliveira', 'email': 'ana@aluno.com', 'turma': '321530'},
                {'nome': 'Carlos Ferreira', 'email': 'carlos@aluno.com', 'turma': '321530'}
            ]
            for aluno_data in alunos_exemplo:
                if not Aluno.query.filter_by(email=aluno_data['email']).first():
                    aluno = Aluno(
                        nome=aluno_data['nome'],
                        email=aluno_data['email'],
                        turma=aluno_data['turma'],
                        senha=generate_password_hash('123456')
                    )
                    db.session.add(aluno)
            
            db.session.commit()
        return "✅ Dados de exemplo inseridos com sucesso!", 200
    except Exception as e:
        return f"❌ Erro ao inserir dados: {str(e)}", 500
