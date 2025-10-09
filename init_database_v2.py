#!/usr/bin/env python3
"""
Script de inicialização do banco de dados AtivFlow v2.0
Inclui todas as novas funcionalidades implementadas
"""

import os
import sys
from datetime import datetime, timedelta

# Adicionar o diretório do projeto ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from werkzeug.security import generate_password_hash

def init_database_complete():
    """
    Inicializa o banco de dados com dados de exemplo completos
    """
    # Importar dentro da função para evitar conflitos
    from backend.src.database_config import db
    from backend.src.main import app
    
    # Importar todos os modelos
    from backend.src.models.professor import Professor
    from backend.src.models.aluno import Aluno
    from backend.src.models.atividade import Atividade
    from backend.src.models.entrega import Entrega
    from backend.src.models.grupo import Grupo, GrupoIntegrante
    from backend.src.models.follow_up import FollowUp
    from backend.src.models.questao import Questao, RespostaAluno
    from backend.src.models.notificacao import Notificacao
    
    with app.app_context():
        print("🔄 Recriando banco de dados...")
        db.drop_all()
        db.create_all()
        
        print("👨‍🏫 Criando professores...")
        # Criar professores
        professor1 = Professor(
            nome='Professor SENAC',
            email='professor@senac.com',
            senha=generate_password_hash('123456')
        )
        
        professor2 = Professor(
            nome='Maria Silva',
            email='maria.silva@senac.com',
            senha=generate_password_hash('123456')
        )
        
        db.session.add_all([professor1, professor2])
        db.session.flush()
        
        print("👨‍🎓 Criando alunos...")
        # Criar alunos
        alunos_data = [
            {"nome": "João Silva", "email": "joao@aluno.com", "turma": "321530"},
            {"nome": "Maria Souza", "email": "maria@aluna.com", "turma": "321530"},
            {"nome": "Pedro Santos", "email": "pedro@aluno.com", "turma": "321530"},
            {"nome": "Ana Costa", "email": "ana@aluna.com", "turma": "321530"},
            {"nome": "Carlos Lima", "email": "carlos@aluno.com", "turma": "321530"},
            {"nome": "Beatriz Oliveira", "email": "beatriz@aluna.com", "turma": "321530"},
            {"nome": "Rafael Pereira", "email": "rafael@aluno.com", "turma": "321530"},
            {"nome": "Juliana Ferreira", "email": "juliana@aluna.com", "turma": "321530"}
        ]
        
        alunos = []
        for aluno_data in alunos_data:
            aluno = Aluno(
                nome=aluno_data['nome'],
                email=aluno_data['email'],
                turma=aluno_data['turma'],
                status='ativo',
                senha=generate_password_hash('123456')
            )
            alunos.append(aluno)
        
        db.session.add_all(alunos)
        db.session.flush()
        
        print("📚 Criando atividades...")
        # Criar atividades de diferentes tipos
        atividades_data = [
            {
                'descricao': 'Projeto Final - Sistema Web',
                'tipo': 'grupo',
                'prazo': datetime.now() + timedelta(days=30)
            },
            {
                'descricao': 'Exercício de HTML/CSS',
                'tipo': 'individual',
                'prazo': datetime.now() + timedelta(days=7)
            },
            {
                'descricao': 'Upload de Portfólio',
                'tipo': 'upload',
                'prazo': datetime.now() + timedelta(days=14)
            },
            {
                'descricao': 'Quiz de JavaScript',
                'tipo': 'multipla_escolha',
                'prazo': datetime.now() + timedelta(days=5)
            },
            {
                'descricao': 'Relatório de Estágio',
                'tipo': 'individual',
                'prazo': datetime.now() + timedelta(days=21)
            }
        ]
        
        atividades = []
        for ativ_data in atividades_data:
            atividade = Atividade(
                descricao=ativ_data['descricao'],
                tipo=ativ_data['tipo'],
                prazo_entrega=ativ_data['prazo'],
                status='ativa'
            )
            atividades.append(atividade)
        
        db.session.add_all(atividades)
        db.session.flush()
        
        print("❓ Criando questões de múltipla escolha...")
        # Criar questões para a atividade de múltipla escolha
        quiz_atividade = next(a for a in atividades if a.tipo == 'multipla_escolha')
        
        questoes_data = [
            {
                'pergunta': 'Qual é a função do JavaScript em uma página web?',
                'opcoes': {
                    'A': 'Apenas estilizar elementos',
                    'B': 'Adicionar interatividade e dinamismo',
                    'C': 'Estruturar o conteúdo',
                    'D': 'Conectar com banco de dados'
                },
                'resposta_correta': 'B',
                'pontos': 2.0
            },
            {
                'pergunta': 'O que significa DOM em JavaScript?',
                'opcoes': {
                    'A': 'Document Object Model',
                    'B': 'Data Object Management',
                    'C': 'Dynamic Object Method',
                    'D': 'Database Object Model'
                },
                'resposta_correta': 'A',
                'pontos': 1.5
            },
            {
                'pergunta': 'Qual método é usado para selecionar um elemento por ID?',
                'opcoes': {
                    'A': 'getElementsByClass()',
                    'B': 'querySelector()',
                    'C': 'getElementById()',
                    'D': 'selectElement()'
                },
                'resposta_correta': 'C',
                'pontos': 1.0
            }
        ]
        
        questoes = []
        for i, questao_data in enumerate(questoes_data, 1):
            questao = Questao(
                atividade_id=quiz_atividade.id,
                pergunta=questao_data['pergunta'],
                resposta_correta=questao_data['resposta_correta'],
                pontos=questao_data['pontos'],
                ordem=i
            )
            questao.set_opcoes(questao_data['opcoes'])
            questoes.append(questao)
        
        db.session.add_all(questoes)
        db.session.flush()
        
        print("📝 Criando entregas automáticas...")
        # Criar entregas automáticas para atividades individuais e múltipla escolha
        for atividade in atividades:
            if atividade.tipo in ['individual', 'multipla_escolha']:
                for aluno in alunos:
                    entrega = Entrega(
                        aluno_id=aluno.id,
                        atividade_id=atividade.id,
                        entregue=False,
                        status='pendente'
                    )
                    db.session.add(entrega)
        
        db.session.flush()
        
        print("👥 Criando grupos...")
        # Criar grupos para atividade em grupo
        grupo_atividade = next(a for a in atividades if a.tipo == 'grupo')
        
        grupos_data = [
            {
                'nome': 'Equipe Alpha',
                'tema': 'E-commerce Responsivo',
                'lider_id': alunos[0].id,
                'integrantes': [alunos[0].id, alunos[1].id, alunos[2].id]
            },
            {
                'nome': 'Equipe Beta',
                'tema': 'Sistema de Gestão Escolar',
                'lider_id': alunos[3].id,
                'integrantes': [alunos[3].id, alunos[4].id, alunos[5].id]
            }
        ]
        
        for grupo_data in grupos_data:
            grupo = Grupo(
                nome_grupo=grupo_data['nome'],
                tema_projeto=grupo_data['tema'],
                prazo_entrega=grupo_atividade.prazo_entrega,
                lider_id=grupo_data['lider_id'],
                status='ativo'
            )
            db.session.add(grupo)
            db.session.flush()
            
            # Adicionar integrantes
            for i, aluno_id in enumerate(grupo_data['integrantes']):
                funcao = 'Líder' if i == 0 else f'Desenvolvedor {i}'
                integrante = GrupoIntegrante(
                    grupo_id=grupo.id,
                    aluno_id=aluno_id,
                    funcao=funcao
                )
                db.session.add(integrante)
        
        print("📊 Criando follow-ups de exemplo...")
        # Criar alguns follow-ups
        followups_data = [
            {
                'aluno_id': alunos[0].id,
                'atividade_texto': 'Estudei HTML e CSS básico',
                'data_realizacao': datetime.now().date(),
                'funcao': 'Estudos',
                'realizado': True
            },
            {
                'aluno_id': alunos[1].id,
                'atividade_texto': 'Pesquisei sobre JavaScript',
                'data_realizacao': datetime.now().date(),
                'funcao': 'Pesquisa',
                'realizado': True
            }
        ]
        
        for followup_data in followups_data:
            followup = FollowUp(
                aluno_id=followup_data['aluno_id'],
                atividade_texto=followup_data['atividade_texto'],
                data_realizacao=followup_data['data_realizacao'],
                funcao=followup_data['funcao'],
                realizado=followup_data['realizado'],
                created_by=followup_data['aluno_id']
            )
            db.session.add(followup)
        
        print("🔔 Criando notificações de exemplo...")
        # Criar notificações de exemplo
        notificacoes_data = [
            {
                'usuario_id': alunos[0].id,
                'tipo_usuario': 'aluno',
                'titulo': 'Nova Atividade Criada',
                'mensagem': 'A atividade "Quiz de JavaScript" foi criada',
                'tipo_notificacao': 'info'
            },
            {
                'usuario_id': professor1.id,
                'tipo_usuario': 'professor',
                'titulo': 'Entrega Realizada',
                'mensagem': 'João Silva realizou uma entrega',
                'tipo_notificacao': 'info'
            }
        ]
        
        for notif_data in notificacoes_data:
            notificacao = Notificacao(
                usuario_id=notif_data['usuario_id'],
                tipo_usuario=notif_data['tipo_usuario'],
                titulo=notif_data['titulo'],
                mensagem=notif_data['mensagem'],
                tipo_notificacao=notif_data['tipo_notificacao']
            )
            db.session.add(notificacao)
        
        print("💾 Salvando dados...")
        db.session.commit()
        
        print("✅ Banco de dados inicializado com sucesso!")
        print("\n📊 Resumo dos dados criados:")
        print(f"   👨‍🏫 Professores: {len([professor1, professor2])}")
        print(f"   👨‍🎓 Alunos: {len(alunos)}")
        print(f"   📚 Atividades: {len(atividades)}")
        print(f"   ❓ Questões: {len(questoes)}")
        print(f"   📝 Entregas: {Entrega.query.count()}")
        print(f"   👥 Grupos: {Grupo.query.count()}")
        print(f"   📊 Follow-ups: {len(followups_data)}")
        print(f"   🔔 Notificações: {len(notificacoes_data)}")
        
        print("\n🔑 Credenciais de acesso:")
        print("   Professor: professor@senac.com / 123456")
        print("   Alunos: [nome]@aluno.com / 123456")
        print("   Exemplo: joao@aluno.com / 123456")

if __name__ == '__main__':
    init_database_complete()
