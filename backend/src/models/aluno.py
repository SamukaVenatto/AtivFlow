from datetime import datetime
from . import db

class Aluno(db.Model):
    __tablename__ = 'alunos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    turma = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='ativo')  # ativo/inativo
    senha = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    entregas = db.relationship('Entrega', backref='aluno', lazy=True)
    grupo_integrantes = db.relationship('GrupoIntegrante', backref='aluno', lazy=True)
    grupos_liderados = db.relationship('Grupo', backref='lider', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'turma': self.turma,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Aluno {self.nome}>'
