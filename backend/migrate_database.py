"""
Script para migrar o banco de dados e adicionar colunas faltantes
"""
import sqlite3
import os
import sys

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def migrate_database():
    """Adiciona colunas faltantes ao banco de dados"""
    
    # Caminho do banco de dados
    db_path = os.path.join(os.path.dirname(__file__), 'src', 'database', 'app.db')
    
    # Criar diretório se não existir
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Conectar ao banco
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Verificar se a tabela alunos existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='alunos'")
        if not cursor.fetchone():
            print("Tabela 'alunos' não existe. Criando estrutura completa...")
            
            # Criar tabela alunos com todas as colunas
            cursor.execute("""
                CREATE TABLE alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome VARCHAR(100) NOT NULL,
                    email VARCHAR(120) UNIQUE NOT NULL,
                    turma VARCHAR(50) NOT NULL,
                    status VARCHAR(20) DEFAULT 'ativo',
                    senha VARCHAR(255) NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            print("Tabela 'alunos' criada com sucesso!")
        else:
            # Verificar se a coluna status existe
            cursor.execute("PRAGMA table_info(alunos)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'status' not in columns:
                print("Adicionando coluna 'status' à tabela alunos...")
                cursor.execute("ALTER TABLE alunos ADD COLUMN status VARCHAR(20) DEFAULT 'ativo'")
                print("Coluna 'status' adicionada com sucesso!")
            else:
                print("Coluna 'status' já existe.")
        
        # Atualizar todos os registros existentes para ter status 'ativo'
        cursor.execute("UPDATE alunos SET status = 'ativo' WHERE status IS NULL OR status = ''")
        
        conn.commit()
        print("Migração concluída com sucesso!")
        
    except Exception as e:
        print(f"Erro durante a migração: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    migrate_database()
