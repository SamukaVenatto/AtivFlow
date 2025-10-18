"""
Modelo de Notificação
"""
from datetime import datetime
from app import db

class Notificacao(db.Model):
    """
    Modelo de notificação para usuários.
    """
    __tablename__ = 'notificacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), index=True)  # Null para notificações globais
    titulo = db.Column(db.String(255), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(30), default='info')  # info, alert, prazo
    lida = db.Column(db.Boolean, default=False)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def to_dict(self):
        """Serializa a notificação para JSON"""
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'titulo': self.titulo,
            'mensagem': self.mensagem,
            'tipo': self.tipo,
            'lida': self.lida,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None
        }
    
    def __repr__(self):
        return f'<Notificacao id={self.id} usuario_id={self.usuario_id}>'

