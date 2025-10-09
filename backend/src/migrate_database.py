"""
Script para migrar o banco de dados e adicionar colunas faltantes
"""
import sqlite3
import os
from src.main import app, db
from src.models.aluno import Aluno

def migrate_database():
    """Adiciona colunas faltantes ao banco de dados"""
    
    # Caminho do banco de dados
    db_path = os.path.join(os.path.dirname(__file__), 'database', 'app.db')
    
    # Conectar ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar se a coluna status existe
        cursor.execute("PRAGMA table_info(alunos)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'status' not in columns:
            print("Adicionando coluna 'status' à tabela alunos...")
            cursor.execute("ALTER TABLE alunos ADD COLUMN status VARCHAR(20) DEFAULT 'ativo'")
            print("Coluna 'status' adicionada com sucesso!")
        else:
            print("Coluna 'status' já existe.")
            
        # Verificar se a coluna senha_definida existe (caso seja necessária)
        if 'senha_definida' not in columns:
            print("Adicionando coluna 'senha_definida' à tabela alunos...")
            cursor.execute("ALTER TABLE alunos ADD COLUMN senha_definida BOOLEAN DEFAULT 1")
            print("Coluna 'senha_definida' adicionada com sucesso!")
        else:
            print("Coluna 'senha_definida' já existe.")
        
        # Atualizar todos os registros existentes para ter status 'ativo'
        cursor.execute("UPDATE alunos SET status = 'ativo' WHERE status IS NULL")
        
        conn.commit()
        print("Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a migração: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    with app.app_context():
        migrate_database()
