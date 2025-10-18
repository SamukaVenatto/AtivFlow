"""
Modelo de Questão e Resposta (Múltipla Escolha)
"""
from datetime import datetime
from app import db
import json

class Questao(db.Model):
    """
    Modelo de questão para atividades de múltipla escolha.
    """
    __tablename__ = 'questoes'
    
    id = db.Column(db.Integer, primary_key=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False, index=True)
    enunciado = db.Column(db.Text, nullable=False)
    tipo = db.Column(db.String(30), default='single')  # single, multiple, dissertativa
    alternativas = db.Column(db.Text)  # JSON com alternativas
    resposta_correta = db.Column(db.Text)  # JSON com resposta(s) correta(s)
    pontuacao = db.Column(db.Numeric(5, 2), default=1.0)
    ordem = db.Column(db.Integer, default=0)
    
    # Relacionamentos
    respostas = db.relationship('Resposta', backref='questao', lazy='dynamic', cascade='all, delete-orphan')
    
    def get_alternativas(self):
        """Retorna alternativas como lista"""
        if self.alternativas:
            try:
                return json.loads(self.alternativas)
            except:
                return []
        return []
    
    def set_alternativas(self, alternativas_list):
        """Define alternativas a partir de lista"""
        self.alternativas = json.dumps(alternativas_list)
    
    def get_resposta_correta(self):
        """Retorna resposta correta"""
        if self.resposta_correta:
            try:
                return json.loads(self.resposta_correta)
            except:
                return None
        return None
    
    def set_resposta_correta(self, resposta):
        """Define resposta correta"""
        self.resposta_correta = json.dumps(resposta)
    
    def to_dict(self, include_resposta=False):
        """Serializa a questão para JSON"""
        data = {
            'id': self.id,
            'atividade_id': self.atividade_id,
            'enunciado': self.enunciado,
            'tipo': self.tipo,
            'alternativas': self.get_alternativas(),
            'pontuacao': float(self.pontuacao) if self.pontuacao else 1.0,
            'ordem': self.ordem
        }
        if include_resposta:
            data['resposta_correta'] = self.get_resposta_correta()
        return data
    
    def __repr__(self):
        return f'<Questao id={self.id} atividade_id={self.atividade_id}>'


class Resposta(db.Model):
    """
    Modelo de resposta do aluno para questões.
    """
    __tablename__ = 'respostas'
    
    id = db.Column(db.Integer, primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'), nullable=False, index=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False, index=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False, index=True)
    resposta = db.Column(db.Text)  # JSON com resposta(s) do aluno
    correta = db.Column(db.Boolean)
    pontos_obtidos = db.Column(db.Numeric(5, 2))
    data_resposta = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com aluno
    aluno = db.relationship('Usuario', backref='respostas', foreign_keys=[aluno_id])
    
    def get_resposta(self):
        """Retorna resposta como objeto Python"""
        if self.resposta:
            try:
                return json.loads(self.resposta)
            except:
                return None
        return None
    
    def set_resposta(self, resposta_obj):
        """Define resposta a partir de objeto Python"""
        self.resposta = json.dumps(resposta_obj)
    
    def to_dict(self):
        """Serializa a resposta para JSON"""
        return {
            'id': self.id,
            'questao_id': self.questao_id,
            'aluno_id': self.aluno_id,
            'atividade_id': self.atividade_id,
            'resposta': self.get_resposta(),
            'correta': self.correta,
            'pontos_obtidos': float(self.pontos_obtidos) if self.pontos_obtidos else 0,
            'data_resposta': self.data_resposta.isoformat() if self.data_resposta else None
        }
    
    def __repr__(self):
        return f'<Resposta questao_id={self.questao_id} aluno_id={self.aluno_id}>'

