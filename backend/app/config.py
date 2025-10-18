"""
Configurações do sistema AtivFlow
"""
import os
from datetime import timedelta

class Config:
    """Configuração base"""
    # Chave secreta para sessões e tokens
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Banco de dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ativflow.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Sessão
    SESSION_TYPE = 'filesystem'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    
    # Upload de arquivos
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'pptx', 'xlsx', 'jpg', 'jpeg', 'png', 'zip'}
    
    # Storage provider (local ou s3)
    STORAGE_PROVIDER = os.environ.get('STORAGE_PROVIDER', 'local')
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    AWS_S3_BUCKET = os.environ.get('AWS_S3_BUCKET')
    AWS_S3_REGION = os.environ.get('AWS_S3_REGION', 'us-east-1')
    
    # CORS
    FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
    
    # Rate limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URL = 'memory://'
    
    # Debug
    DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    # Timezone
    TIMEZONE = 'UTC'
    
    # Notificações - limpeza automática
    NOTIFICATION_CLEANUP_DAYS = 30

class DevelopmentConfig(Config):
    """Configuração de desenvolvimento"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///ativflow.db')

class ProductionConfig(Config):
    """Configuração de produção"""
    DEBUG = False
    SESSION_COOKIE_SECURE = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

