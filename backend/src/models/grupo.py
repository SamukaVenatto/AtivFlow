from datetime import datetime
from src.database_config import db

class Grupo(db.Model):
    __tablename__ = 'grupos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome_grupo = db.Column(db.String(100), nullable=False)
    tema_projeto = db.Column(db.String(200), nullable=False)
    prazo_entrega = db.Column(db.DateTime, nullable=False)
    lider_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    status = db.Column(db.String(20), default='em_andamento')  # em_andamento/entregue/atrasado
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    integrantes = db.relationship('GrupoIntegrante', backref='grupo', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome_grupo': self.nome_grupo,
            'tema_projeto': self.tema_projeto,
            'prazo_entrega': self.prazo_entrega.isoformat() if self.prazo_entrega else None,
            'lider_id': self.lider_id,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'integrantes': [integrante.to_dict() for integrante in self.integrantes]
        }
    
    def __repr__(self):
        return f'<Grupo {self.nome_grupo}>'


class GrupoIntegrante(db.Model):
    __tablename__ = 'grupo_integrantes'
    
    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    funcao = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'grupo_id': self.grupo_id,
            'aluno_id': self.aluno_id,
            'funcao': self.funcao,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<GrupoIntegrante {self.id}: Grupo {self.grupo_id} - Aluno {self.aluno_id}>'
