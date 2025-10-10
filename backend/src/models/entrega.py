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
    status = db.Column(db.String(20), default='pendente')  # pendente, entregue, atrasado
    funcao_responsabilidade = db.Column(db.String(200))
    
    # ⚠️ REMOVIDOS: feedback, nota, avaliado_por, data_avaliacao (não existem no banco)
    
    arquivo_url = db.Column(db.String(500))  # opcional, mantido caso queira usar depois
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
            # ⚠️ Removidos os campos que não existem
            'arquivo_url': self.arquivo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f'<Entrega {self.id}: Aluno {self.aluno_id} - Atividade {self.atividade_id}>'