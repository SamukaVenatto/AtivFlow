"""
Utilitários da aplicação
"""
from app.utils.auth import login_required, professor_required, admin_required, get_current_user
from app.utils.email_generator import gerar_email_aluno
from app.utils.file_upload import save_file, save_multiple_files, delete_file, allowed_file
from app.utils.notifications import (
    criar_notificacao, 
    criar_notificacao_global,
    notificar_turma,
    notificar_nova_atividade,
    notificar_entrega_recebida,
    notificar_avaliacao_concluida,
    notificar_prazo_proximo,
    verificar_prazos_proximos,
    limpar_notificacoes_antigas
)

__all__ = [
    'login_required',
    'professor_required',
    'admin_required',
    'get_current_user',
    'gerar_email_aluno',
    'save_file',
    'save_multiple_files',
    'delete_file',
    'allowed_file',
    'criar_notificacao',
    'criar_notificacao_global',
    'notificar_turma',
    'notificar_nova_atividade',
    'notificar_entrega_recebida',
    'notificar_avaliacao_concluida',
    'notificar_prazo_proximo',
    'verificar_prazos_proximos',
    'limpar_notificacoes_antigas'
]

