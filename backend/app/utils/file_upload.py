"""
Utilitário para upload e gerenciamento de arquivos
"""
import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_file(file):
    """
    Salva um arquivo no sistema local com nome único.
    Retorna a URL/caminho do arquivo salvo.
    
    Em produção, esta função pode ser adaptada para usar S3.
    """
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        raise ValueError(f"Tipo de arquivo não permitido: {file.filename}")
    
    # Gerar nome único
    original_filename = secure_filename(file.filename)
    extension = original_filename.rsplit('.', 1)[1].lower()
    unique_filename = f"{uuid.uuid4().hex}.{extension}"
    
    # Salvar arquivo
    upload_folder = current_app.config['UPLOAD_FOLDER']
    filepath = os.path.join(upload_folder, unique_filename)
    file.save(filepath)
    
    # Retornar URL relativa (em produção seria URL do S3)
    return f"/uploads/{unique_filename}"

def save_multiple_files(files):
    """
    Salva múltiplos arquivos e retorna lista de URLs.
    """
    urls = []
    for file in files:
        try:
            url = save_file(file)
            if url:
                urls.append(url)
        except ValueError as e:
            # Log do erro, mas continua processando outros arquivos
            print(f"Erro ao salvar arquivo: {e}")
    return urls

def delete_file(file_url):
    """
    Remove um arquivo do sistema local.
    Em produção, adaptar para S3.
    """
    try:
        # Extrair nome do arquivo da URL
        filename = file_url.split('/')[-1]
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
    except Exception as e:
        print(f"Erro ao deletar arquivo: {e}")
    return False

