"""
Modelo de Grupo
"""
from datetime import datetime
from app import db

class Grupo(db.Model):
    """
    Modelo de grupo para atividades em grupo.
    """
    __tablename__ = 'grupos'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False, index=True)
    lider_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), index=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default='ativo')  # ativo, concluido
    observacoes = db.Column(db.Text)
    
    # Relacionamentos
    membros = db.relationship('GrupoMembro', backref='grupo', lazy='dynamic', cascade='all, delete-orphan')
    entregas = db.relationship('Entrega', backref='grupo', lazy='dynamic', foreign_keys='Entrega.grupo_id')
    
    def to_dict(self):
        """Serializa o grupo para JSON"""
        return {
            'id': self.id,
            'nome': self.nome,
            'atividade_id': self.atividade_id,
            'lider_id': self.lider_id,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'membros': [m.to_dict() for m in self.membros]
        }
    
    def __repr__(self):
        return f'<Grupo {self.nome}>'


class GrupoMembro(db.Model):
    """
    Modelo de membro de grupo.
    """
    __tablename__ = 'grupo_membros'
    
    id = db.Column(db.Integer, primary_key=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False, index=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    papel = db.Column(db.String(50))  # Ex: desenvolvedor, designer, etc
    status_membro = db.Column(db.String(30), default='ativo')  # ativo, inativo
    data_entrada = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com usuário
    aluno = db.relationship('Usuario', backref='membros_grupo', foreign_keys=[aluno_id])
    
    def to_dict(self):
        """Serializa o membro para JSON"""
        return {
            'id': self.id,
            'grupo_id': self.grupo_id,
            'aluno_id': self.aluno_id,
            'aluno_nome': self.aluno.nome_completo if self.aluno else None,
            'papel': self.papel,
            'status_membro': self.status_membro,
            'data_entrada': self.data_entrada.isoformat() if self.data_entrada else None
        }
    
    def __repr__(self):
        return f'<GrupoMembro aluno_id={self.aluno_id} grupo_id={self.grupo_id}>'

