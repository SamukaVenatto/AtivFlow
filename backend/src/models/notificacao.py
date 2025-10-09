from datetime import datetime
from src.database_config import db

class Notificacao(db.Model):
    __tablename__ = 'notificacoes'
    
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, nullable=False)  # ID do usuário (aluno ou professor)
    tipo_usuario = db.Column(db.String(20), nullable=False)  # 'aluno' ou 'professor'
    titulo = db.Column(db.String(200), nullable=False)
    mensagem = db.Column(db.Text, nullable=False)
    tipo_notificacao = db.Column(db.String(50), default='info')  # info, sucesso, aviso, erro
    lida = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)
    data_leitura = db.Column(db.DateTime)
    
    # Campos opcionais para referência
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'))
    entrega_id = db.Column(db.Integer, db.ForeignKey('entregas.id'))
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'))
    
    # Relacionamentos
    atividade = db.relationship('Atividade', backref='notificacoes')
    entrega = db.relationship('Entrega', backref='notificacoes')
    grupo = db.relationship('Grupo', backref='notificacoes')
    
    def to_dict(self):
        return {
            'id': self.id,
            'usuario_id': self.usuario_id,
            'tipo_usuario': self.tipo_usuario,
            'titulo': self.titulo,
            'mensagem': self.mensagem,
            'tipo_notificacao': self.tipo_notificacao,
            'lida': self.lida,
            'data_criacao': self.data_criacao.isoformat() if self.data_criacao else None,
            'data_leitura': self.data_leitura.isoformat() if self.data_leitura else None,
            'atividade_id': self.atividade_id,
            'entrega_id': self.entrega_id,
            'grupo_id': self.grupo_id
        }
    
    def marcar_como_lida(self):
        """
        Marca a notificação como lida
        """
        self.lida = True
        self.data_leitura = datetime.utcnow()
    
    def __repr__(self):
        return f'<Notificacao {self.id}: {self.titulo}>'
