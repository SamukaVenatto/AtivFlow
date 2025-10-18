"""
Utilitário para geração de e-mail de aluno conforme regras do SENAC
"""
import unicodedata
import re

# Mapeamento de siglas por curso
CURSO_SIGLAS = {
    'Administração': 'adm',
    'Farmácia': 'farma',
    'Segurança do Trabalho': 'tst',
    'Logística': 'log'
}

def remover_acentos(texto):
    """Remove acentos e caracteres especiais de uma string"""
    # Normaliza para NFD (decompõe caracteres acentuados)
    nfd = unicodedata.normalize('NFD', texto)
    # Remove marcas diacríticas
    sem_acentos = ''.join(char for char in nfd if unicodedata.category(char) != 'Mn')
    return sem_acentos

def gerar_email_aluno(nome_completo, curso, turma):
    """
    Gera o e-mail do aluno conforme as regras:
    - Remover acentos e caracteres especiais
    - Substituir espaços por pontos
    - Tudo em minúsculas
    - Formato: nome.sobrenome@<sigla><turma>.com
    
    Exemplo: Samuel Ribeiro, Administração, 321350 -> samuel.ribeiro@adm321350.com
    """
    # Remover acentos
    nome_sem_acentos = remover_acentos(nome_completo)
    
    # Remover caracteres especiais (manter apenas letras e espaços)
    nome_limpo = re.sub(r'[^a-zA-Z\s]', '', nome_sem_acentos)
    
    # Substituir espaços por pontos e converter para minúsculas
    nome_email = nome_limpo.strip().replace(' ', '.').lower()
    
    # Obter sigla do curso
    sigla = CURSO_SIGLAS.get(curso, 'senac')  # Default 'senac' se curso não encontrado
    
    # Montar e-mail
    email = f"{nome_email}@{sigla}{turma}.com"
    
    return email

