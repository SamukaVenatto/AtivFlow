"""
Importação de todas as rotas
"""
from app.routes import auth, usuarios, atividades, entregas, grupos, questoes, followups, notificacoes, relatorios

__all__ = [
    'auth',
    'usuarios',
    'atividades',
    'entregas',
    'grupos',
    'questoes',
    'followups',
    'notificacoes',
    'relatorios'
]

