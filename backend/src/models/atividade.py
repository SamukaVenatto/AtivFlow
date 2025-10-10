from datetime import datetime
from src.database_config import db

class Atividade(db.Model):
    __tablename__ = 'atividades'
    
    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    prazo_entrega = db.Column(db.DateTime, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)  # individual/grupo/upload/multipla_escolha
    status = db.Column(db.String(20), default='ativa')  # ativa/inativa
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    entregas = db.relationship('Entrega', backref='atividade', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'descricao': self.descricao,
            'prazo_entrega': self.prazo_entrega.isoformat() if self.prazo_entrega else None,
            'tipo': self.tipo,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Atividade {self.id}: {self.descricao[:50]}>'
