"""
Script de migração do banco de dados para PostgreSQL
Executa as alterações necessárias nas tabelas existentes
"""

import os
import sys
from sqlalchemy import text

# Adicionar o diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.main import app
from src.database_config import db

def migrate_database():
    """Executa migrações necessárias no banco de dados"""
    with app.app_context():
        print("🔄 Iniciando migração do banco de dados...")
        
        try:
            # Verificar se as tabelas existem
            inspector = db.inspect(db.engine)
            existing_tables = inspector.get_table_names()
            
            print(f"📋 Tabelas existentes: {existing_tables}")
            
            # Adicionar colunas faltantes na tabela professores
            if 'professores' in existing_tables:
                print("⚙️ Atualizando tabela professores...")
                try:
                    db.session.execute(text("""
                        ALTER TABLE professores 
                        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """))
                    db.session.commit()
                    print("✅ Tabela professores atualizada")
                except Exception as e:
                    print(f"⚠️ Aviso ao atualizar professores: {e}")
                    db.session.rollback()
            
            # Adicionar colunas faltantes na tabela alunos
            if 'alunos' in existing_tables:
                print("⚙️ Atualizando tabela alunos...")
                try:
                    db.session.execute(text("""
                        ALTER TABLE alunos 
                        ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'ativo',
                        ADD COLUMN IF NOT EXISTS senha_definida BOOLEAN DEFAULT FALSE,
                        ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """))
                    db.session.commit()
                    print("✅ Tabela alunos atualizada")
                except Exception as e:
                    print(f"⚠️ Aviso ao atualizar alunos: {e}")
                    db.session.rollback()
            
            # Adicionar colunas faltantes na tabela atividades
            if 'atividades' in existing_tables:
                print("⚙️ Atualizando tabela atividades...")
                try:
                    db.session.execute(text("""
                        ALTER TABLE atividades 
                        ADD COLUMN IF NOT EXISTS titulo VARCHAR(200),
                        ADD COLUMN IF NOT EXISTS formato VARCHAR(50),
                        ADD COLUMN IF NOT EXISTS criterios_avaliacao TEXT,
                        ADD COLUMN IF NOT EXISTS professor_id INTEGER REFERENCES professores(id),
                        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """))
                    db.session.commit()
                    print("✅ Tabela atividades atualizada")
                except Exception as e:
                    print(f"⚠️ Aviso ao atualizar atividades: {e}")
                    db.session.rollback()
            
            # Adicionar colunas faltantes na tabela entregas
            if 'entregas' in existing_tables:
                print("⚙️ Atualizando tabela entregas...")
                try:
                    db.session.execute(text("""
                        ALTER TABLE entregas 
                        ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    """))
                    db.session.commit()
                    print("✅ Tabela entregas atualizada")
                except Exception as e:
                    print(f"⚠️ Aviso ao atualizar entregas: {e}")
                    db.session.rollback()
            
            print("\n✅ Migração concluída com sucesso!")
            print("📊 Estrutura do banco de dados atualizada")
            
        except Exception as e:
            print(f"\n❌ Erro durante a migração: {e}")
            db.session.rollback()
            raise

def create_all_tables():
    """Cria todas as tabelas do zero (para banco novo)"""
    with app.app_context():
        print("🔨 Criando todas as tabelas...")
        try:
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao criar tabelas: {e}")
            raise

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Migração do banco de dados AtivFlow')
    parser.add_argument('--create', action='store_true', help='Criar todas as tabelas do zero')
    parser.add_argument('--migrate', action='store_true', help='Migrar banco existente')
    
    args = parser.parse_args()
    
    if args.create:
        create_all_tables()
    elif args.migrate:
        migrate_database()
    else:
        print("Use --create para criar tabelas ou --migrate para migrar banco existente")
        print("Exemplo: python migrate_db.py --migrate")
