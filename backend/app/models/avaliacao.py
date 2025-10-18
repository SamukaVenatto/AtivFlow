"""
Modelo de Avaliação
"""
from datetime import datetime
from app import db

class Avaliacao(db.Model):
    """
    Modelo de avaliação de entrega.
    """
    __tablename__ = 'avaliacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    entrega_id = db.Column(db.Integer, db.ForeignKey('entregas.id'), nullable=False, index=True)
    professor_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    nota = db.Column(db.Numeric(5, 2), nullable=False)
    feedback = db.Column(db.Text)
    data_avaliacao = db.Column(db.DateTime, default=datetime.utcnow)
    rejeitado = db.Column(db.Boolean, default=False)
    
    def to_dict(self):
        """Serializa a avaliação para JSON"""
        return {
            'id': self.id,
            'entrega_id': self.entrega_id,
            'professor_id': self.professor_id,
            'nota': float(self.nota) if self.nota else 0,
            'feedback': self.feedback,
            'data_avaliacao': self.data_avaliacao.isoformat() if self.data_avaliacao else None,
            'rejeitado': self.rejeitado
        }
    
    def __repr__(self):
        return f'<Avaliacao entrega_id={self.entrega_id} professor_id={self.professor_id}>'

