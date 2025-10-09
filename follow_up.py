# backend/src/routes/follow_up.py

from flask import Blueprint, request, jsonify, current_app, send_file
from src.database_config import db
from src.models.follow_up import FollowUp
from src.utils.auth_decorators import login_required, professor_required, get_current_user_id, is_professor
from datetime import datetime
import csv, io

follow_up_bp = Blueprint('follow_up', __name__)

# ---------- Aluno: criar FollowUp ----------
@follow_up_bp.route('/api/followups', methods=['POST'])
@login_required
def create_followup():
    user_id = get_current_user_id()

    data = request.json or {}
    # campos esperados: atividade_id (opcional), atividade_texto, data_realizacao, funcao, realizado (bool), justificativa
    atividade_id = data.get('atividade_id')
    atividade_texto = data.get('atividade_texto')
    data_real = data.get('data_realizacao')
    funcao = data.get('funcao')
    realizado = data.get('realizado', False)
    justificativa = data.get('justificativa')

    # validações
    if not data_real:
        return jsonify({"error": "Campo 'data_realizacao' é obrigatório"}), 400

    try:
        # aceita YYYY-MM-DD
        data_real_dt = datetime.strptime(data_real, '%Y-%m-%d').date()
    except Exception:
        return jsonify({"error": "Formato de data inválido. Use YYYY-MM-DD"}), 400

    # justificativa obrigatória se não realizado
    if not realizado and (not justificativa or justificativa.strip() == ""):
        return jsonify({"error": "Justificativa obrigatória quando realizado = false"}), 400

    # truncamentos simples (conformidade com modelos)
    if atividade_texto:
        atividade_texto = atividade_texto[:1000]
    if funcao:
        funcao = funcao[:1000]
    if justificativa:
        justificativa = justificativa[:1000]

    followup = FollowUp(
        aluno_id=int(user_id),
        atividade_id=int(atividade_id) if atividade_id else None,
        atividade_texto=atividade_texto,
        data_realizacao=data_real_dt,
        funcao=funcao,
        realizado=bool(realizado),
        justificativa=justificativa,
        created_by=int(user_id)
    )

    db.session.add(followup)
    db.session.commit()

    # Hook para notificação do professor (implementar conforme infra)
    try:
        # current_app.logger.info("Notificar professor - followup criado")
        pass
    except Exception:
        pass

    return jsonify({"message": "FollowUp criado com sucesso", "followup": followup.to_dict()}), 201


# ---------- Aluno: listar meus followups (histórico) ----------
@follow_up_bp.route('/api/followups/me', methods=['GET'])
@login_required
def list_my_followups():
    user_id = get_current_user_id()

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 20))
    query = FollowUp.query.filter_by(aluno_id=int(user_id)).order_by(FollowUp.data_realizacao.desc())
    pag = query.paginate(page=page, per_page=per_page, error_out=False)
    items = [f.to_dict() for f in pag.items]
    return jsonify({"items": items, "total": pag.total, "page": pag.page, "per_page": pag.per_page})


# ---------- Professor/Admin: listar com filtros ----------
@follow_up_bp.route('/api/admin/followups', methods=['GET'])
@professor_required
def admin_list_followups():

    aluno_id = request.args.get('aluno_id')
    atividade_id = request.args.get('atividade_id')
    realizado = request.args.get('realizado')  # 'true'|'false' ou None
    date_from = request.args.get('date_from')  # YYYY-MM-DD
    date_to = request.args.get('date_to')

    query = FollowUp.query

    if aluno_id:
        query = query.filter_by(aluno_id=int(aluno_id))
    if atividade_id:
        query = query.filter_by(atividade_id=int(atividade_id))
    if realizado is not None:
        if realizado.lower() in ('true', '1', 'sim', 's'):
            query = query.filter_by(realizado=True)
        elif realizado.lower() in ('false', '0', 'nao', 'não', 'n'):
            query = query.filter_by(realizado=False)
    if date_from:
        try:
            df = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(FollowUp.data_realizacao >= df)
        except:
            pass
    if date_to:
        try:
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(FollowUp.data_realizacao <= dt)
        except:
            pass

    # pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    pag = query.order_by(FollowUp.data_realizacao.desc()).paginate(page=page, per_page=per_page, error_out=False)
    items = [f.to_dict() for f in pag.items]
    return jsonify({"items": items, "total": pag.total, "page": pag.page, "per_page": pag.per_page})


# ---------- Professor: apagar followup ----------
@follow_up_bp.route('/api/admin/followups/<int:id>', methods=['DELETE'])
@professor_required
def admin_delete_followup(id):

    f = FollowUp.query.get(id)
    if not f:
        return jsonify({"error": "FollowUp não encontrado"}), 404

    db.session.delete(f)
    db.session.commit()
    return jsonify({"message": "FollowUp removido"}), 200


# ---------- Professor: marcar revisado ----------
@follow_up_bp.route('/api/admin/followups/<int:id>/revisar', methods=['PUT'])
@professor_required
def admin_mark_reviewed(id):

    f = FollowUp.query.get(id)
    if not f:
        return jsonify({"error": "FollowUp não encontrado"}), 404

    f.revisado = True
    db.session.commit()
    return jsonify({"message": "FollowUp marcado como revisado", "followup": f.to_dict()}), 200


# ---------- Export CSV (professor) ----------
@follow_up_bp.route('/api/admin/followups/export', methods=['GET'])
@professor_required
def admin_export_csv():

    # reuse admin_list filters logic quickly (could refactor)
    aluno_id = request.args.get('aluno_id')
    atividade_id = request.args.get('atividade_id')
    realizado = request.args.get('realizado')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    query = FollowUp.query
    if aluno_id:
        query = query.filter_by(aluno_id=int(aluno_id))
    if atividade_id:
        query = query.filter_by(atividade_id=int(atividade_id))
    if realizado is not None:
        if realizado.lower() in ('true', '1', 'sim', 's'):
            query = query.filter_by(realizado=True)
        elif realizado.lower() in ('false', '0', 'nao', 'não', 'n'):
            query = query.filter_by(realizado=False)
    if date_from:
        try:
            df = datetime.strptime(date_from, '%Y-%m-%d').date()
            query = query.filter(FollowUp.data_realizacao >= df)
        except:
            pass
    if date_to:
        try:
            dt = datetime.strptime(date_to, '%Y-%m-%d').date()
            query = query.filter(FollowUp.data_realizacao <= dt)
        except:
            pass

    items = query.order_by(FollowUp.data_realizacao.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    header = ['id','aluno_id','aluno_nome','atividade_id','atividade_texto','data_realizacao','funcao','realizado','justificativa','revisado','created_at']
    writer.writerow(header)
    for f in items:
        writer.writerow([
            f.id,
            f.aluno_id,
            getattr(f.aluno, 'nome', ''),
            f.atividade_id,
            f.atividade_texto or '',
            f.data_realizacao.isoformat() if f.data_realizacao else '',
            f.funcao or '',
            'Sim' if f.realizado else 'Não',
            f.justificativa or '',
            'Sim' if f.revisado else 'Não',
            f.created_at.isoformat() if f.created_at else ''
        ])
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode('utf-8')), mimetype='text/csv', as_attachment=True, download_name='followups.csv')
