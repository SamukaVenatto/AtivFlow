from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from src.models.aluno import Aluno, db
from src.models.atividade import Atividade
from src.models.entrega import Entrega
from src.models.grupo import Grupo, GrupoIntegrante

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/stats', methods=['GET'])
def get_dashboard_stats():
    try:
        # Estatísticas gerais
        total_alunos = Aluno.query.filter_by(status='ativo').count()
        total_atividades = Atividade.query.filter_by(status='ativa').count()
        total_grupos = Grupo.query.count()
        
        # Estatísticas de entregas
        total_entregas = Entrega.query.count()
        entregas_entregues = Entrega.query.filter_by(entregue=True).count()
        entregas_pendentes = Entrega.query.filter_by(entregue=False).count()
        entregas_atrasadas = Entrega.query.filter_by(status='atrasado').count()
        
        # Taxa de entrega
        taxa_entrega = (entregas_entregues / total_entregas * 100) if total_entregas > 0 else 0
        
        return jsonify({
            'total_alunos': total_alunos,
            'total_atividades': total_atividades,
            'total_grupos': total_grupos,
            'total_entregas': total_entregas,
            'entregas_entregues': entregas_entregues,
            'entregas_pendentes': entregas_pendentes,
            'entregas_atrasadas': entregas_atrasadas,
            'taxa_entrega': round(taxa_entrega, 2)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/entregas-por-status', methods=['GET'])
def get_entregas_por_status():
    try:
        stats = db.session.query(
            Entrega.status,
            func.count(Entrega.id).label('count')
        ).group_by(Entrega.status).all()
        
        result = [{'status': stat.status, 'count': stat.count} for stat in stats]
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/entregas-por-aluno', methods=['GET'])
def get_entregas_por_aluno():
    try:
        stats = db.session.query(
            Aluno.nome,
            func.count(Entrega.id).label('total_entregas'),
            func.sum(func.case([(Entrega.entregue == True, 1)], else_=0)).label('entregues'),
            func.sum(func.case([(Entrega.status == 'atrasado', 1)], else_=0)).label('atrasadas')
        ).outerjoin(Entrega).group_by(Aluno.id, Aluno.nome).all()
        
        result = []
        for stat in stats:
            result.append({
                'nome': stat.nome,
                'total_entregas': stat.total_entregas or 0,
                'entregues': stat.entregues or 0,
                'atrasadas': stat.atrasadas or 0
            })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/atividades-proximas', methods=['GET'])
def get_atividades_proximas():
    try:
        # Atividades com prazo nos próximos 7 dias
        data_limite = datetime.utcnow() + timedelta(days=7)
        
        atividades = Atividade.query.filter(
            and_(
                Atividade.status == 'ativa',
                Atividade.prazo_entrega <= data_limite,
                Atividade.prazo_entrega >= datetime.utcnow()
            )
        ).order_by(Atividade.prazo_entrega).all()
        
        result = []
        for atividade in atividades:
            # Contar entregas para esta atividade
            total_entregas = Entrega.query.filter_by(atividade_id=atividade.id).count()
            entregas_feitas = Entrega.query.filter_by(atividade_id=atividade.id, entregue=True).count()
            
            atividade_dict = atividade.to_dict()
            atividade_dict['total_entregas'] = total_entregas
            atividade_dict['entregas_feitas'] = entregas_feitas
            atividade_dict['dias_restantes'] = (atividade.prazo_entrega - datetime.utcnow()).days
            
            result.append(atividade_dict)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/grupos-status', methods=['GET'])
def get_grupos_status():
    try:
        stats = db.session.query(
            Grupo.status,
            func.count(Grupo.id).label('count')
        ).group_by(Grupo.status).all()
        
        result = [{'status': stat.status, 'count': stat.count} for stat in stats]
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/aluno/<int:aluno_id>/stats', methods=['GET'])
def get_aluno_stats(aluno_id):
    try:
        aluno = Aluno.query.get_or_404(aluno_id)
        
        # Estatísticas do aluno
        total_entregas = Entrega.query.filter_by(aluno_id=aluno_id).count()
        entregas_entregues = Entrega.query.filter_by(aluno_id=aluno_id, entregue=True).count()
        entregas_pendentes = Entrega.query.filter_by(aluno_id=aluno_id, entregue=False).count()
        entregas_atrasadas = Entrega.query.filter_by(aluno_id=aluno_id, status='atrasado').count()
        
        # Grupos do aluno
        grupos_como_integrante = GrupoIntegrante.query.filter_by(aluno_id=aluno_id).count()
        grupos_como_lider = Grupo.query.filter_by(lider_id=aluno_id).count()
        
        # Atividades próximas do prazo
        data_limite = datetime.utcnow() + timedelta(days=7)
        atividades_proximas = db.session.query(Atividade).join(Entrega).filter(
            and_(
                Entrega.aluno_id == aluno_id,
                Entrega.entregue == False,
                Atividade.prazo_entrega <= data_limite,
                Atividade.prazo_entrega >= datetime.utcnow()
            )
        ).count()
        
        return jsonify({
            'aluno': aluno.to_dict(),
            'total_entregas': total_entregas,
            'entregas_entregues': entregas_entregues,
            'entregas_pendentes': entregas_pendentes,
            'entregas_atrasadas': entregas_atrasadas,
            'grupos_como_integrante': grupos_como_integrante,
            'grupos_como_lider': grupos_como_lider,
            'atividades_proximas': atividades_proximas
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@dashboard_bp.route('/relatorio/entregas', methods=['GET'])
def get_relatorio_entregas():
    try:
        # Parâmetros de filtro
        aluno_id = request.args.get('aluno_id')
        atividade_id = request.args.get('atividade_id')
        status = request.args.get('status')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')
        
        query = db.session.query(Entrega).join(Aluno).join(Atividade)
        
        if aluno_id:
            query = query.filter(Entrega.aluno_id == aluno_id)
        if atividade_id:
            query = query.filter(Entrega.atividade_id == atividade_id)
        if status:
            query = query.filter(Entrega.status == status)
        if data_inicio:
            data_inicio_dt = datetime.fromisoformat(data_inicio)
            query = query.filter(Entrega.created_at >= data_inicio_dt)
        if data_fim:
            data_fim_dt = datetime.fromisoformat(data_fim)
            query = query.filter(Entrega.created_at <= data_fim_dt)
        
        entregas = query.all()
        
        result = []
        for entrega in entregas:
            entrega_dict = entrega.to_dict()
            entrega_dict['aluno'] = entrega.aluno.to_dict()
            entrega_dict['atividade'] = entrega.atividade.to_dict()
            result.append(entrega_dict)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
