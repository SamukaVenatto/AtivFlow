"""
Modelo de Follow-Up (Registro Diário)
"""
from datetime import datetime
from app import db

class FollowUp(db.Model):
    """
    Modelo de follow-up (registro diário de atividades do aluno).
    """
    __tablename__ = 'followups'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    atividade_realizada = db.Column(db.Text, nullable=False)
    assunto_aula = db.Column(db.String(255))
    data = db.Column(db.Date, nullable=False, index=True)
    responsabilidade = db.Column(db.String(255))
    status = db.Column(db.String(30), default='pendente')  # pendente, revisado
    justificativa = db.Column(db.Text)
    feedback_professor = db.Column(db.Text)
    revisado = db.Column(db.Boolean, default=False)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    pode_editar = db.Column(db.Boolean, default=False)  # Professor pode liberar edição
    
    def to_dict(self):
        """Serializa o follow-up para JSON"""
        return {
            'id': self.id,
            'aluno_id': self.aluno_id,
            'atividade_realizada': self.atividade_realizada,
            'assunto_aula': self.assunto_aula,
            'data': self.data.isoformat() if self.data else None,
            'responsabilidade': self.responsabilidade,
            'status': self.status,
            'justificativa': self.justificativa,
            'feedback_professor': self.feedback_professor,
            'revisado': self.revisado,
            'criado_em': self.criado_em.isoformat() if self.criado_em else None,
            'pode_editar': self.pode_editar
        }
    
    def __repr__(self):
        return f'<FollowUp aluno_id={self.aluno_id} data={self.data}>'

