"""
Script para popular o banco de dados com dados de exemplo
Turma 321530 com 12 alunos e 2 professores
"""
import sys
import os
from datetime import datetime, timedelta

# Adicionar diretório pai ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models.usuario import Usuario
from app.models.atividade import Atividade
from app.models.grupo import Grupo, GrupoMembro
from app.models.questao import Questao

def seed_database():
    """Popula o banco de dados com dados de exemplo"""
    app = create_app('development')
    
    with app.app_context():
        print("Limpando banco de dados...")
        db.drop_all()
        db.create_all()
        
        print("Criando professores...")
        # Professor 1 - Responsável
        prof1 = Usuario(
            nome_completo='Maria Silva Santos',
            email='maria.santos@senac.edu.br',
            tipo='professor',
            curso='Administração',
            turma='321530',
            status='ativo'
        )
        prof1.set_password('Prof@123')
        db.session.add(prof1)
        
        # Professor 2
        prof2 = Usuario(
            nome_completo='João Paulo Oliveira',
            email='joao.oliveira@senac.edu.br',
            tipo='professor',
            curso='Administração',
            turma='321530',
            status='ativo'
        )
        prof2.set_password('Prof@123')
        db.session.add(prof2)
        
        db.session.commit()
        
        print("Criando 12 alunos da turma 321530...")
        # Lista de alunos fictícios
        alunos_data = [
            'Samuel Ribeiro',
            'Ana Carolina Souza',
            'Pedro Henrique Lima',
            'Juliana Costa Santos',
            'Lucas Fernandes',
            'Mariana Alves',
            'Rafael Pereira',
            'Beatriz Rodrigues',
            'Gabriel Martins',
            'Larissa Oliveira',
            'Felipe Santos',
            'Camila Ferreira'
        ]
        
        alunos = []
        for nome in alunos_data:
            from app.utils.email_generator import gerar_email_aluno
            
            email = gerar_email_aluno(nome, 'Administração', '321530')
            
            aluno = Usuario(
                nome_completo=nome,
                email=email,
                tipo='aluno',
                curso='Administração',
                turma='321530',
                status='ativo'
            )
            aluno.set_password('Aluno@123')
            db.session.add(aluno)
            alunos.append(aluno)
        
        db.session.commit()
        
        print("Criando 3 atividades...")
        # Atividade 1 - Individual
        ativ1 = Atividade(
            titulo='Trabalho Individual - Planejamento Estratégico',
            descricao='Desenvolver um plano estratégico para uma empresa fictícia, incluindo análise SWOT, missão, visão e valores.',
            tipo='individual',
            prazo=datetime.utcnow() + timedelta(days=15),
            criado_por=prof1.id,
            turma='321530',
            ativo=True
        )
        ativ1.set_config({
            'max_arquivos': 2,
            'tamanho_max_mb': 10,
            'permitir_reenvio': False
        })
        db.session.add(ativ1)
        
        # Atividade 2 - Grupo
        ativ2 = Atividade(
            titulo='Projeto em Grupo - Estudo de Caso',
            descricao='Análise de caso real de uma empresa do mercado, com apresentação de soluções e estratégias de melhoria.',
            tipo='grupo',
            prazo=datetime.utcnow() + timedelta(days=30),
            criado_por=prof1.id,
            turma='321530',
            ativo=True
        )
        ativ2.set_config({
            'max_arquivos': 5,
            'tamanho_max_mb': 20,
            'min_integrantes': 3,
            'max_integrantes': 5
        })
        db.session.add(ativ2)
        
        # Atividade 3 - Múltipla Escolha
        ativ3 = Atividade(
            titulo='Avaliação - Fundamentos de Administração',
            descricao='Avaliação sobre conceitos fundamentais de administração e gestão empresarial.',
            tipo='multipla_escolha',
            prazo=datetime.utcnow() + timedelta(days=7),
            criado_por=prof2.id,
            turma='321530',
            ativo=True
        )
        ativ3.set_config({
            'correcao_automatica': True,
            'exibir_resultado_imediato': True
        })
        db.session.add(ativ3)
        
        db.session.commit()
        
        print("Criando questões para atividade de múltipla escolha...")
        # Questão 1
        q1 = Questao(
            atividade_id=ativ3.id,
            enunciado='O que é planejamento estratégico?',
            tipo='single',
            pontuacao=2.0,
            ordem=1
        )
        q1.set_alternativas([
            'Um processo de curto prazo focado em operações diárias',
            'Um processo de longo prazo que define objetivos e estratégias organizacionais',
            'Uma ferramenta exclusiva para o setor financeiro',
            'Um método de controle de estoque'
        ])
        q1.set_resposta_correta(1)  # Índice da resposta correta
        db.session.add(q1)
        
        # Questão 2
        q2 = Questao(
            atividade_id=ativ3.id,
            enunciado='Quais são as funções básicas da administração?',
            tipo='multiple',
            pontuacao=3.0,
            ordem=2
        )
        q2.set_alternativas([
            'Planejar',
            'Organizar',
            'Vender',
            'Dirigir',
            'Controlar'
        ])
        q2.set_resposta_correta([0, 1, 3, 4])  # Índices das respostas corretas
        db.session.add(q2)
        
        # Questão 3
        q3 = Questao(
            atividade_id=ativ3.id,
            enunciado='O que significa a sigla SWOT?',
            tipo='single',
            pontuacao=2.0,
            ordem=3
        )
        q3.set_alternativas([
            'Strengths, Weaknesses, Opportunities, Threats',
            'Sales, Work, Operations, Technology',
            'Strategy, Workflow, Objectives, Tasks',
            'Systems, Workers, Organization, Training'
        ])
        q3.set_resposta_correta(0)
        db.session.add(q3)
        
        db.session.commit()
        
        print("Criando 2 grupos para atividade em grupo...")
        # Grupo 1
        grupo1 = Grupo(
            nome='Grupo Alpha',
            atividade_id=ativ2.id,
            lider_id=alunos[0].id,  # Samuel como líder
            status='ativo',
            observacoes='Grupo focado em análise de empresas de tecnologia'
        )
        db.session.add(grupo1)
        
        # Grupo 2
        grupo2 = Grupo(
            nome='Grupo Beta',
            atividade_id=ativ2.id,
            lider_id=alunos[6].id,  # Rafael como líder
            status='ativo',
            observacoes='Grupo focado em análise de empresas de varejo'
        )
        db.session.add(grupo2)
        
        db.session.commit()
        
        print("Adicionando membros aos grupos...")
        # Membros do Grupo 1
        for i in range(5):  # Primeiros 5 alunos
            membro = GrupoMembro(
                grupo_id=grupo1.id,
                aluno_id=alunos[i].id,
                papel='Membro' if i > 0 else 'Líder',
                status_membro='ativo'
            )
            db.session.add(membro)
        
        # Membros do Grupo 2
        for i in range(6, 11):  # Alunos 7 a 11
            membro = GrupoMembro(
                grupo_id=grupo2.id,
                aluno_id=alunos[i].id,
                papel='Membro' if i > 6 else 'Líder',
                status_membro='ativo'
            )
            db.session.add(membro)
        
        db.session.commit()
        
        print("\n" + "="*50)
        print("SEED CONCLUÍDO COM SUCESSO!")
        print("="*50)
        print("\nCredenciais de acesso:")
        print("\nProfessores:")
        print("  Email: maria.santos@senac.edu.br")
        print("  Senha: Prof@123")
        print("\n  Email: joao.oliveira@senac.edu.br")
        print("  Senha: Prof@123")
        print("\nAlunos (todos com senha: Aluno@123):")
        for aluno in alunos[:3]:  # Mostrar apenas 3 exemplos
            print(f"  Email: {aluno.email}")
        print("  ... (e mais 9 alunos)")
        print("\nTurma: 321530")
        print("Curso: Administração")
        print("\nAtividades criadas: 3 (1 individual, 1 grupo, 1 múltipla escolha)")
        print("Grupos criados: 2 (com 5 membros cada)")
        print("="*50)

if __name__ == '__main__':
    seed_database()

