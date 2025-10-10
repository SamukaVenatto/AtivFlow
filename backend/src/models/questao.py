from datetime import datetime
from . import db
import json

class Questao(db.Model):
    __tablename__ = 'questoes'
    
    id = db.Column(db.Integer, primary_key=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False)
    pergunta = db.Column(db.Text, nullable=False)
    opcoes = db.Column(db.Text, nullable=False)  # JSON string com as opções
    resposta_correta = db.Column(db.String(10), nullable=False)  # Letra da resposta correta (A, B, C, D, E)
    pontos = db.Column(db.Float, default=1.0)  # Pontos que vale a questão
    ordem = db.Column(db.Integer, default=1)  # Ordem da questão na atividade
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    atividade = db.relationship('Atividade', backref='questoes')
    
    def get_opcoes(self):
        """
        Retorna as opções como dicionário Python
        """
        try:
            return json.loads(self.opcoes) if self.opcoes else {}
        except:
            return {}
    
    def set_opcoes(self, opcoes_dict):
        """
        Define as opções a partir de um dicionário Python
        """
        self.opcoes = json.dumps(opcoes_dict, ensure_ascii=False)
    
    def to_dict(self, include_resposta=False):
        """
        Converte para dicionário
        
        Args:
            include_resposta: Se True, inclui a resposta correta (para professores)
        """
        data = {
            'id': self.id,
            'atividade_id': self.atividade_id,
            'pergunta': self.pergunta,
            'opcoes': self.get_opcoes(),
            'pontos': self.pontos,
            'ordem': self.ordem,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_resposta:
            data['resposta_correta'] = self.resposta_correta
            
        return data
    
    def __repr__(self):
        return f'<Questao {self.id}: {self.pergunta[:50]}...>'


class RespostaAluno(db.Model):
    __tablename__ = 'respostas_aluno'
    
    id = db.Column(db.Integer, primary_key=True)
    questao_id = db.Column(db.Integer, db.ForeignKey('questoes.id'), nullable=False)
    aluno_id = db.Column(db.Integer, db.ForeignKey('alunos.id'), nullable=False)
    entrega_id = db.Column(db.Integer, db.ForeignKey('entregas.id'), nullable=False)
    resposta_escolhida = db.Column(db.String(10), nullable=False)  # Letra escolhida (A, B, C, D, E)
    correta = db.Column(db.Boolean, default=False)  # Se a resposta está correta
    pontos_obtidos = db.Column(db.Float, default=0.0)  # Pontos obtidos nesta questão
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    questao = db.relationship('Questao', backref='respostas')
    aluno = db.relationship('Aluno', backref='respostas')
    entrega = db.relationship('Entrega', backref='respostas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'questao_id': self.questao_id,
            'aluno_id': self.aluno_id,
            'entrega_id': self.entrega_id,
            'resposta_escolhida': self.resposta_escolhida,
            'correta': self.correta,
            'pontos_obtidos': self.pontos_obtidos,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<RespostaAluno {self.id}: Questão {self.questao_id} - Aluno {self.aluno_id}>'
