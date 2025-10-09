from datetime import datetime
from src.database_config import db

class Entrega(db.Model):
    __tablename__ = 'entregas'
    
    id = db.Column(db.Integer, primary_key=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)
    data_entrega = db.Column(db.DateTime, default=datetime.utcnow)
    entregue = db.Column(db.Boolean, default=False)
    justificativa = db.Column(db.Text)
    status = db.Column(db.String(20), default='pendente')  # pendente/entregue/atrasado/em_analise/revisado
    funcao_responsabilidade = db.Column(db.String(200))
    
    # Campos de avaliação
    feedback = db.Column(db.Text)  # Feedback do professor
    nota = db.Column(db.Float)  # Nota da entrega
    avaliado_por = db.Column(db.Integer, db.ForeignKey('professores.id'))  # Professor que avaliou
    data_avaliacao = db.Column(db.DateTime)  # Data da avaliação
    arquivo_url = db.Column(db.String(500))  # URL do arquivo enviado
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'aluno_id': self.aluno_id,
            'atividade_id': self.atividade_id,
            'data_entrega': self.data_entrega.isoformat() if self.data_entrega else None,
            'entregue': self.entregue,
            'justificativa': self.justificativa,
            'status': self.status,
            'funcao_responsabilidade': self.funcao_responsabilidade,
            'feedback': self.feedback,
            'nota': self.nota,
            'avaliado_por': self.avaliado_por,
            'data_avaliacao': self.data_avaliacao.isoformat() if self.data_avaliacao else None,
            'arquivo_url': self.arquivo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Entrega {self.id}: Aluno {self.aluno_id} - Atividade {self.atividade_id}>'
