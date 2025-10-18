"""
Modelo de Usuário
"""
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class Usuario(db.Model):
    """
    Modelo de usuário do sistema.
    Tipos: aluno, professor, admin
    """
    __tablename__ = 'usuarios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_completo = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    senha_hash = db.Column(db.String(255), nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # aluno, professor, admin
    curso = db.Column(db.String(100))
    turma = db.Column(db.String(20))
    status = db.Column(db.String(20), default='ativo')  # ativo, inativo
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    ultimo_login = db.Column(db.DateTime)
    
    # Relacionamentos
    atividades_criadas = db.relationship('Atividade', backref='criador', lazy='dynamic', foreign_keys='Atividade.criado_por')
    entregas = db.relationship('Entrega', backref='aluno', lazy='dynamic', foreign_keys='Entrega.aluno_id')
    grupos_liderados = db.relationship('Grupo', backref='lider', lazy='dynamic', foreign_keys='Grupo.lider_id')
    avaliacoes_feitas = db.relationship('Avaliacao', backref='professor', lazy='dynamic', foreign_keys='Avaliacao.professor_id')
    followups = db.relationship('FollowUp', backref='aluno', lazy='dynamic', foreign_keys='FollowUp.aluno_id')
    notificacoes = db.relationship('Notificacao', backref='usuario', lazy='dynamic', foreign_keys='Notificacao.usuario_id')
    
    def set_password(self, password):
        """Define a senha com hash bcrypt (work factor 12)"""
        self.senha_hash = generate_password_hash(password, method='pbkdf2:sha256')
    
    def check_password(self, password):
        """Verifica se a senha está correta"""
        return check_password_hash(self.senha_hash, password)
    
    def to_dict(self):
        """Serializa o usuário para JSON"""
        return {
            'id': self.id,
            'nome_completo': self.nome_completo,
            'email': self.email,
            'tipo': self.tipo,
            'curso': self.curso,
            'turma': self.turma,
            'status': self.status,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'ultimo_login': self.ultimo_login.isoformat() if self.ultimo_login else None
        }
    
    def __repr__(self):
        return f'<Usuario {self.email}>'

