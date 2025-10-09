from flask import Blueprint, request, jsonify, session
from datetime import datetime
from src.models.entrega import Entrega, db
from src.models.atividade import Atividade
from src.models.aluno import Aluno

entrega_bp = Blueprint('entrega', __name__)

@entrega_bp.route('/', methods=['GET'])
def get_entregas():
    try:
        aluno_id = request.args.get('aluno_id')
        atividade_id = request.args.get('atividade_id')
        
        query = Entrega.query
        
        if aluno_id:
            query = query.filter_by(aluno_id=aluno_id)
        if atividade_id:
            query = query.filter_by(atividade_id=atividade_id)
        
        entregas = query.all()
        
        # Incluir dados do aluno e atividade
        result = []
        for entrega in entregas:
            entrega_dict = entrega.to_dict()
            entrega_dict['aluno'] = entrega.aluno.to_dict() if entrega.aluno else None
            entrega_dict['atividade'] = entrega.atividade.to_dict() if entrega.atividade else None
            result.append(entrega_dict)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@entrega_bp.route('/<int:entrega_id>', methods=['GET'])
def get_entrega(entrega_id):
    try:
        entrega = Entrega.query.get_or_404(entrega_id)
        entrega_dict = entrega.to_dict()
        entrega_dict['aluno'] = entrega.aluno.to_dict() if entrega.aluno else None
        entrega_dict['atividade'] = entrega.atividade.to_dict() if entrega.atividade else None
        return jsonify(entrega_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@entrega_bp.route('/', methods=['POST'])
def create_entrega():
    try:
        data = request.get_json()
        aluno_id = data.get('aluno_id')
        atividade_id = data.get('atividade_id')
        entregue = data.get('entregue', False)
        justificativa = data.get('justificativa', '')
        funcao_responsabilidade = data.get('funcao_responsabilidade', '')
        
        if not all([aluno_id, atividade_id]):
            return jsonify({'error': 'Aluno e atividade são obrigatórios'}), 400
        
        # Verificar se já existe entrega para este aluno/atividade
        entrega_existente = Entrega.query.filter_by(
            aluno_id=aluno_id, 
            atividade_id=atividade_id
        ).first()
        
        if entrega_existente:
            return jsonify({'error': 'Entrega já existe para este aluno/atividade'}), 400
        
        # Verificar se a atividade ainda está no prazo
        atividade = Atividade.query.get(atividade_id)
        if not atividade:
            return jsonify({'error': 'Atividade não encontrada'}), 404
        
        status = 'entregue' if entregue else 'pendente'
        if entregue and datetime.utcnow() > atividade.prazo_entrega:
            status = 'atrasado'
        
        nova_entrega = Entrega(
            aluno_id=aluno_id,
            atividade_id=atividade_id,
            entregue=entregue,
            justificativa=justificativa,
            funcao_responsabilidade=funcao_responsabilidade,
            status=status
        )
        
        db.session.add(nova_entrega)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Entrega criada com sucesso',
            'entrega': nova_entrega.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@entrega_bp.route('/<int:entrega_id>', methods=['PUT'])
def update_entrega(entrega_id):
    try:
        entrega = Entrega.query.get_or_404(entrega_id)
        data = request.get_json()
        
        if 'entregue' in data:
            entrega.entregue = data['entregue']
            
            # Atualizar status baseado na entrega e prazo
            if data['entregue']:
                atividade = Atividade.query.get(entrega.atividade_id)
                if datetime.utcnow() > atividade.prazo_entrega:
                    entrega.status = 'atrasado'
                else:
                    entrega.status = 'entregue'
            else:
                entrega.status = 'pendente'
        
        if 'justificativa' in data:
            entrega.justificativa = data['justificativa']
        if 'funcao_responsabilidade' in data:
            entrega.funcao_responsabilidade = data['funcao_responsabilidade']
        if 'status' in data:
            entrega.status = data['status']
        
        entrega.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Entrega atualizada com sucesso',
            'entrega': entrega.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@entrega_bp.route('/<int:entrega_id>', methods=['DELETE'])
def delete_entrega(entrega_id):
    try:
        entrega = Entrega.query.get_or_404(entrega_id)
        db.session.delete(entrega)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Entrega excluída com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@entrega_bp.route('/aluno/<int:aluno_id>', methods=['GET'])
def get_entregas_aluno(aluno_id):
    try:
        entregas = Entrega.query.filter_by(aluno_id=aluno_id).all()
        
        result = []
        for entrega in entregas:
            entrega_dict = entrega.to_dict()
            entrega_dict['atividade'] = entrega.atividade.to_dict() if entrega.atividade else None
            result.append(entrega_dict)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Importar decoradores de autenticação
from src.utils.auth_decorators import professor_required, get_current_user_id

@entrega_bp.route('/<int:entrega_id>/avaliar', methods=['PUT'])
@professor_required
def avaliar_entrega(entrega_id):
    """
    Rota para professor avaliar uma entrega
    Corpo esperado:
    {
        "feedback": "Texto do feedback",
        "nota": 9.5,
        "status": "revisado"
    }
    """
    try:
        entrega = Entrega.query.get_or_404(entrega_id)
        data = request.get_json()
        
        # Validar dados obrigatórios
        if 'feedback' not in data and 'nota' not in data:
            return jsonify({'error': 'Feedback ou nota são obrigatórios para avaliação'}), 400
        
        # Validar nota se fornecida
        if 'nota' in data:
            nota = data['nota']
            if not isinstance(nota, (int, float)) or nota < 0 or nota > 10:
                return jsonify({'error': 'Nota deve ser um número entre 0 e 10'}), 400
            entrega.nota = float(nota)
        
        # Atualizar campos de avaliação
        if 'feedback' in data:
            entrega.feedback = data['feedback']
        
        if 'status' in data:
            status_validos = ['pendente', 'entregue', 'atrasado', 'em_analise', 'revisado']
            if data['status'] not in status_validos:
                return jsonify({'error': f'Status deve ser um dos seguintes: {", ".join(status_validos)}'}), 400
            entrega.status = data['status']
        else:
            # Se não especificado, marcar como revisado
            entrega.status = 'revisado'
        
        # Registrar quem avaliou e quando
        entrega.avaliado_por = get_current_user_id()
        entrega.data_avaliacao = datetime.utcnow()
        entrega.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Enviar notificação sobre avaliação concluída
        try:
            from src.utils.notificacao_utils import notificar_avaliacao_concluida
            notificar_avaliacao_concluida(entrega)
        except Exception as e:
            print(f"Erro ao enviar notificação: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Entrega avaliada com sucesso',
            'entrega': entrega.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@entrega_bp.route('/estatisticas', methods=['GET'])
@professor_required
def get_estatisticas_entregas():
    """
    Rota para obter estatísticas de entregas para o dashboard do professor
    """
    try:
        # Total de entregas
        total_entregas = Entrega.query.count()
        
        # Entregas por status
        entregas_pendentes = Entrega.query.filter_by(status='pendente').count()
        entregas_entregues = Entrega.query.filter_by(status='entregue').count()
        entregas_atrasadas = Entrega.query.filter_by(status='atrasado').count()
        entregas_revisadas = Entrega.query.filter_by(status='revisado').count()
        
        # Nota média das entregas avaliadas
        from sqlalchemy import func
        nota_media = db.session.query(func.avg(Entrega.nota)).filter(Entrega.nota.isnot(None)).scalar()
        nota_media = round(float(nota_media), 2) if nota_media else 0
        
        # Entregas avaliadas vs não avaliadas
        entregas_avaliadas = Entrega.query.filter(Entrega.nota.isnot(None)).count()
        entregas_nao_avaliadas = total_entregas - entregas_avaliadas
        
        return jsonify({
            'total_entregas': total_entregas,
            'entregas_por_status': {
                'pendente': entregas_pendentes,
                'entregue': entregas_entregues,
                'atrasado': entregas_atrasadas,
                'revisado': entregas_revisadas
            },
            'nota_media': nota_media,
            'entregas_avaliadas': entregas_avaliadas,
            'entregas_nao_avaliadas': entregas_nao_avaliadas,
            'taxa_avaliacao': round((entregas_avaliadas / total_entregas * 100), 2) if total_entregas > 0 else 0
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Importar utilitários de upload
from src.utils.file_upload import save_uploaded_file, delete_uploaded_file
from src.utils.auth_decorators import login_required

@entrega_bp.route('/upload', methods=['POST'])
@login_required
def upload_arquivo_entrega():
    """
    Endpoint para upload de arquivos em entregas
    Aceita multipart/form-data com os campos:
    - file: arquivo a ser enviado
    - entrega_id: ID da entrega
    """
    try:
        # Verificar se arquivo foi enviado
        if 'file' not in request.files:
            return jsonify({'error': 'Nenhum arquivo enviado'}), 400
        
        file = request.files['file']
        entrega_id = request.form.get('entrega_id')
        
        if not entrega_id:
            return jsonify({'error': 'ID da entrega é obrigatório'}), 400
        
        # Buscar entrega
        entrega = Entrega.query.get_or_404(entrega_id)
        
        # Verificar se o usuário pode fazer upload para esta entrega
        user_id = get_current_user_id()
        user_type = session.get('user_type')
        
        # Aluno só pode fazer upload em suas próprias entregas
        if user_type == 'aluno' and entrega.aluno_id != user_id:
            return jsonify({'error': 'Você só pode fazer upload em suas próprias entregas'}), 403
        
        # Verificar se a atividade permite upload
        atividade = entrega.atividade
        if atividade.tipo not in ['upload', 'individual', 'grupo']:
            return jsonify({'error': 'Esta atividade não permite upload de arquivos'}), 400
        
        # Remover arquivo anterior se existir
        if entrega.arquivo_url:
            delete_uploaded_file(entrega.arquivo_url)
        
        # Salvar novo arquivo
        upload_result = save_uploaded_file(file, subfolder='entregas')
        
        if not upload_result['success']:
            return jsonify({'error': upload_result['error']}), 400
        
        # Atualizar entrega
        entrega.arquivo_url = upload_result['url']
        entrega.entregue = True
        entrega.status = 'entregue'
        entrega.data_entrega = datetime.utcnow()
        entrega.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        # Enviar notificação sobre entrega realizada
        try:
            from src.utils.notificacao_utils import notificar_entrega_realizada
            notificar_entrega_realizada(entrega)
        except Exception as e:
            print(f"Erro ao enviar notificação: {e}")
        
        return jsonify({
            'success': True,
            'message': 'Arquivo enviado com sucesso',
            'arquivo_url': upload_result['url'],
            'filename': upload_result['filename'],
            'original_filename': upload_result['original_filename'],
            'entrega': entrega.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@entrega_bp.route('/<int:entrega_id>/remover-arquivo', methods=['DELETE'])
@login_required
def remover_arquivo_entrega(entrega_id):
    """
    Remove o arquivo de uma entrega
    """
    try:
        entrega = Entrega.query.get_or_404(entrega_id)
        
        # Verificar permissões
        user_id = get_current_user_id()
        user_type = session.get('user_type')
        
        # Aluno só pode remover arquivo de suas próprias entregas
        if user_type == 'aluno' and entrega.aluno_id != user_id:
            return jsonify({'error': 'Você só pode remover arquivos de suas próprias entregas'}), 403
        
        if not entrega.arquivo_url:
            return jsonify({'error': 'Esta entrega não possui arquivo'}), 400
        
        # Remover arquivo do sistema
        if delete_uploaded_file(entrega.arquivo_url):
            entrega.arquivo_url = None
            entrega.entregue = False
            entrega.status = 'pendente'
            entrega.updated_at = datetime.utcnow()
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Arquivo removido com sucesso',
                'entrega': entrega.to_dict()
            })
        else:
            return jsonify({'error': 'Erro ao remover arquivo do sistema'}), 500
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
