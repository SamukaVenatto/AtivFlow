"""
Modelo de Atividade
"""
from datetime import datetime
from app import db
import json

class Atividade(db.Model):
    """
    Modelo de atividade.
    Tipos: individual, grupo, multipla_escolha
    """
    __tablename__ = 'atividades'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    tipo = db.Column(db.String(30), nullable=False)  # individual, grupo, multipla_escolha
    prazo = db.Column(db.DateTime, nullable=False)
    criado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    config_json = db.Column(db.Text)  # JSON com configurações extras
    ativo = db.Column(db.Boolean, default=True)
    turma = db.Column(db.String(20))  # Turma alvo da atividade
    
    # Relacionamentos
    entregas = db.relationship('Entrega', backref='atividade', lazy='dynamic', cascade='all, delete-orphan')
    questoes = db.relationship('Questao', backref='atividade', lazy='dynamic', cascade='all, delete-orphan')
    grupos = db.relationship('Grupo', backref='atividade', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_config(self):
        """Retorna configurações como dicionário"""
        if self.config_json:
            try:
                return json.loads(self.config_json)
            except:
                return {}
        return {}
    
    def set_config(self, config_dict):
        """Define configurações a partir de dicionário"""
        self.config_json = json.dumps(config_dict)
    
    def to_dict(self):
        """Serializa a atividade para JSON"""
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'tipo': self.tipo,
            'prazo': self.prazo.isoformat() if self.prazo else None,
            'criado_por': self.criado_por,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'config': self.get_config(),
            'ativo': self.ativo,
            'turma': self.turma
        }
    
    def __repr__(self):
        return f'<Atividade {self.titulo}>'

