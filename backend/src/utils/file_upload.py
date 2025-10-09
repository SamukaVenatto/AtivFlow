"""
Utilitários para upload de arquivos
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

# Extensões permitidas
ALLOWED_EXTENSIONS = {
    'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
    'xls', 'xlsx', 'ppt', 'pptx', 'zip', 'rar', '7z', 'mp4', 
    'avi', 'mov', 'mp3', 'wav'
}

def allowed_file(filename):
    """
    Verifica se a extensão do arquivo é permitida
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
    """
    Obtém a extensão do arquivo
    """
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_unique_filename(original_filename):
    """
    Gera um nome único para o arquivo mantendo a extensão original
    """
    extension = get_file_extension(original_filename)
    unique_id = str(uuid.uuid4())
    return f"{unique_id}.{extension}" if extension else unique_id

def get_upload_path():
    """
    Retorna o caminho do diretório de uploads
    """
    return os.path.join(current_app.root_path, 'static', 'uploads')

def save_uploaded_file(file, subfolder=None):
    """
    Salva um arquivo enviado e retorna a URL pública
    
    Args:
        file: Arquivo do request
        subfolder: Subpasta opcional (ex: 'entregas', 'atividades')
    
    Returns:
        dict: {'success': bool, 'url': str, 'filename': str, 'error': str}
    """
    try:
        if not file or file.filename == '':
            return {'success': False, 'error': 'Nenhum arquivo selecionado'}
        
        if not allowed_file(file.filename):
            return {'success': False, 'error': 'Tipo de arquivo não permitido'}
        
        # Gerar nome único
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        
        # Definir caminho de salvamento
        upload_path = get_upload_path()
        if subfolder:
            upload_path = os.path.join(upload_path, subfolder)
            os.makedirs(upload_path, exist_ok=True)
        
        file_path = os.path.join(upload_path, unique_filename)
        
        # Salvar arquivo
        file.save(file_path)
        
        # Gerar URL pública
        if subfolder:
            public_url = f"/static/uploads/{subfolder}/{unique_filename}"
        else:
            public_url = f"/static/uploads/{unique_filename}"
        
        return {
            'success': True,
            'url': public_url,
            'filename': unique_filename,
            'original_filename': original_filename
        }
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

def delete_uploaded_file(file_url):
    """
    Remove um arquivo do sistema de arquivos
    
    Args:
        file_url: URL do arquivo (ex: /static/uploads/arquivo.pdf)
    
    Returns:
        bool: True se removido com sucesso
    """
    try:
        if not file_url or not file_url.startswith('/static/uploads/'):
            return False
        
        # Converter URL para caminho do sistema
        relative_path = file_url.replace('/static/', '')
        file_path = os.path.join(current_app.root_path, 'static', relative_path.replace('uploads/', 'uploads/'))
        
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        
        return False
        
    except Exception:
        return False
