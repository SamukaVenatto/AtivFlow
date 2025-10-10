# backend/src/models/__init__.py

from flask_sqlalchemy import SQLAlchemy

# 1. Cria a instância ÚNICA do banco de dados
db = SQLAlchemy()

# 2. Importa todas as suas classes para que o SQLAlchemy as reconheça
# O '.' antes do nome do arquivo significa "da mesma pasta"
from .user import User
from .aluno import Aluno
from .professor import Professor
from .atividade import Atividade
from .entrega import Entrega
from .follow_up import FollowUp
from .grupo import Grupo, GrupoIntegrante
from .questao import Questao, RespostaAluno
from .notificacao import Notificacao

