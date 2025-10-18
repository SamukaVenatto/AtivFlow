"""
Modelo de Entrega
"""
from datetime import datetime
from app import db
import json

class Entrega(db.Model):
    """
    Modelo de entrega de atividade.
    Pode ser individual (aluno_id) ou em grupo (grupo_id).
    """
    __tablename__ = 'entregas'
    
    id = db.Column(db.Integer, primary_key=True)
    atividade_id = db.Column(db.Integer, db.ForeignKey('atividades.id'), nullable=False, index=True)
    aluno_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), index=True)
    grupo_id = db.Column(db.Integer, db.ForeignKey('grupos.id'), index=True)
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(30), default='entregue')  # entregue, pendente, rejeitado, avaliado, atrasada
    arquivo_urls = db.Column(db.Text)  # JSON array com URLs dos arquivos
    observacoes = db.Column(db.Text)
    nota = db.Column(db.Numeric(5, 2))
    avaliado_por = db.Column(db.Integer, db.ForeignKey('usuarios.id'))
    data_avaliacao = db.Column(db.DateTime)
    
    # Campos para fluxo do líder
    destino_grupo = db.Column(db.Boolean, default=False)  # Se é entrega para o líder
    encaminhado_para = db.Column(db.Integer, db.ForeignKey('usuarios.id'))  # ID do líder
    consolidada = db.Column(db.Boolean, default=False)  # Se foi consolidada pelo líder
    
    # Relacionamentos
    avaliacoes = db.relationship('Avaliacao', backref='entrega', lazy='dynamic', cascade='all, delete-orphan')
    avaliador = db.relationship('Usuario', foreign_keys=[avaliado_por], backref='entregas_avaliadas')
    lider = db.relationship('Usuario', foreign_keys=[encaminhado_para], backref='entregas_recebidas')
    
    def get_arquivos(self):
        """Retorna lista de URLs de arquivos"""
        if self.arquivo_urls:
            try:
                return json.loads(self.arquivo_urls)
            except:
                return []
        return []
    
    def set_arquivos(self, urls_list):
        """Define lista de URLs de arquivos"""
        self.arquivo_urls = json.dumps(urls_list)
    
    def to_dict(self):
        """Serializa a entrega para JSON"""
        return {
            'id': self.id,
            'atividade_id': self.atividade_id,
            'aluno_id': self.aluno_id,
            'grupo_id': self.grupo_id,
            'data_envio': self.data_envio.isoformat() if self.data_envio else None,
            'status': self.status,
            'arquivos': self.get_arquivos(),
            'observacoes': self.observacoes,
            'nota': float(self.nota) if self.nota else None,
            'avaliado_por': self.avaliado_por,
            'data_avaliacao': self.data_avaliacao.isoformat() if self.data_avaliacao else None,
            'destino_grupo': self.destino_grupo,
            'encaminhado_para': self.encaminhado_para,
            'consolidada': self.consolidada
        }
    
    def __repr__(self):
        return f'<Entrega id={self.id} atividade_id={self.atividade_id}>'

