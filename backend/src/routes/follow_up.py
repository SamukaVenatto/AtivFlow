# backend/src/models/follow_up.py

from datetime import datetime
from src.database_config import db

class FollowUp(db.Model):
    __tablename__ = 'follow_up'

    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=True)  # FK opcional
    atividade_texto = db.Column(db.String(1000), nullable=True)  # entrada livre
    data_realizacao = db.Column(db.Date, nullable=False)
    funcao = db.Column(db.String(1000), nullable=True)
    realizado = db.Column(db.Boolean, default=False, nullable=False)
    justificativa = db.Column(db.String(1000), nullable=True)
    revisado = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_by = db.Column(db.Integer, nullable=True)  # opcional: id do usuario que inseriu (se diferir de aluno)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # relationship helpers (lazy loading)
    aluno = db.relationship('Aluno', backref=db.backref('followups', lazy='dynamic'), foreign_keys=[aluno_id], lazy=True)
    atividade = db.relationship('Atividade', backref=db.backref('followups', lazy='dynamic'), foreign_keys=[atividade_id], lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "aluno_id": self.aluno_id,
            "aluno_nome": getattr(self.aluno, "nome", None),
            "atividade_id": self.atividade_id,
            "atividade_texto": self.atividade_texto,
            "data_realizacao": self.data_realizacao.isoformat() if self.data_realizacao else None,
            "funcao": self.funcao,
            "realizado": self.realizado,
            "justificativa": self.justificativa,
            "revisado": self.revisado,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "created_by": self.created_by,
        }
