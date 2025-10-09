from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.grupo import Grupo, GrupoIntegrante, db
from src.models.aluno import Aluno

grupo_bp = Blueprint('grupo', __name__)

@grupo_bp.route('/', methods=['GET'])
def get_grupos():
    try:
        grupos = Grupo.query.all()
        result = []
        for grupo in grupos:
            grupo_dict = grupo.to_dict()
            grupo_dict['lider'] = grupo.lider.to_dict() if grupo.lider else None
            
            # Incluir dados completos dos integrantes
            integrantes_completos = []
            for integrante in grupo.integrantes:
                integrante_dict = integrante.to_dict()
                integrante_dict['aluno'] = integrante.aluno.to_dict() if integrante.aluno else None
                integrantes_completos.append(integrante_dict)
            
            grupo_dict['integrantes'] = integrantes_completos
            result.append(grupo_dict)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grupo_bp.route('/<int:grupo_id>', methods=['GET'])
def get_grupo(grupo_id):
    try:
        grupo = Grupo.query.get_or_404(grupo_id)
        grupo_dict = grupo.to_dict()
        grupo_dict['lider'] = grupo.lider.to_dict() if grupo.lider else None
        
        # Incluir dados completos dos integrantes
        integrantes_completos = []
        for integrante in grupo.integrantes:
            integrante_dict = integrante.to_dict()
            integrante_dict['aluno'] = integrante.aluno.to_dict() if integrante.aluno else None
            integrantes_completos.append(integrante_dict)
        
        grupo_dict['integrantes'] = integrantes_completos
        return jsonify(grupo_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@grupo_bp.route('/', methods=['POST'])
def create_grupo():
    try:
        data = request.get_json()
        nome_grupo = data.get('nome_grupo')
        tema_projeto = data.get('tema_projeto')
        prazo_entrega = data.get('prazo_entrega')
        lider_id = data.get('lider_id')
        integrantes = data.get('integrantes', [])  # Lista de {aluno_id, funcao}
        
        if not all([nome_grupo, tema_projeto, prazo_entrega, lider_id]):
            return jsonify({'error': 'Todos os campos obrigatórios devem ser preenchidos'}), 400
        
        # Converter string de data para datetime
        try:
            prazo_dt = datetime.fromisoformat(prazo_entrega.replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Formato de data inválido'}), 400
        
        # Verificar se o líder existe
        lider = Aluno.query.get(lider_id)
        if not lider:
            return jsonify({'error': 'Líder não encontrado'}), 404
        
        novo_grupo = Grupo(
            nome_grupo=nome_grupo,
            tema_projeto=tema_projeto,
            prazo_entrega=prazo_dt,
            lider_id=lider_id
        )
        
        db.session.add(novo_grupo)
        db.session.flush()  # Para obter o ID do grupo
        
        # Adicionar integrantes
        for integrante_data in integrantes:
            aluno_id = integrante_data.get('aluno_id')
            funcao = integrante_data.get('funcao', '')
            
            if aluno_id:
                # Verificar se o aluno existe
                aluno = Aluno.query.get(aluno_id)
                if aluno:
                    integrante = GrupoIntegrante(
                        grupo_id=novo_grupo.id,
                        aluno_id=aluno_id,
                        funcao=funcao
                    )
                    db.session.add(integrante)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Grupo criado com sucesso',
            'grupo': novo_grupo.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grupo_bp.route('/<int:grupo_id>', methods=['PUT'])
def update_grupo(grupo_id):
    try:
        grupo = Grupo.query.get_or_404(grupo_id)
        data = request.get_json()
        
        if 'nome_grupo' in data:
            grupo.nome_grupo = data['nome_grupo']
        if 'tema_projeto' in data:
            grupo.tema_projeto = data['tema_projeto']
        if 'prazo_entrega' in data:
            try:
                grupo.prazo_entrega = datetime.fromisoformat(data['prazo_entrega'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Formato de data inválido'}), 400
        if 'lider_id' in data:
            # Verificar se o novo líder existe
            lider = Aluno.query.get(data['lider_id'])
            if not lider:
                return jsonify({'error': 'Líder não encontrado'}), 404
            grupo.lider_id = data['lider_id']
        if 'status' in data:
            grupo.status = data['status']
        
        # Atualizar integrantes se fornecido
        if 'integrantes' in data:
            # Remover integrantes existentes
            GrupoIntegrante.query.filter_by(grupo_id=grupo_id).delete()
            
            # Adicionar novos integrantes
            for integrante_data in data['integrantes']:
                aluno_id = integrante_data.get('aluno_id')
                funcao = integrante_data.get('funcao', '')
                
                if aluno_id:
                    aluno = Aluno.query.get(aluno_id)
                    if aluno:
                        integrante = GrupoIntegrante(
                            grupo_id=grupo_id,
                            aluno_id=aluno_id,
                            funcao=funcao
                        )
                        db.session.add(integrante)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Grupo atualizado com sucesso',
            'grupo': grupo.to_dict()
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grupo_bp.route('/<int:grupo_id>', methods=['DELETE'])
def delete_grupo(grupo_id):
    try:
        grupo = Grupo.query.get_or_404(grupo_id)
        
        # Remover integrantes primeiro
        GrupoIntegrante.query.filter_by(grupo_id=grupo_id).delete()
        
        # Remover grupo
        db.session.delete(grupo)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Grupo excluído com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grupo_bp.route('/<int:grupo_id>/integrantes', methods=['POST'])
def add_integrante(grupo_id):
    try:
        grupo = Grupo.query.get_or_404(grupo_id)
        data = request.get_json()
        aluno_id = data.get('aluno_id')
        funcao = data.get('funcao', '')
        
        if not aluno_id:
            return jsonify({'error': 'ID do aluno é obrigatório'}), 400
        
        # Verificar se o aluno existe
        aluno = Aluno.query.get(aluno_id)
        if not aluno:
            return jsonify({'error': 'Aluno não encontrado'}), 404
        
        # Verificar se já é integrante
        integrante_existente = GrupoIntegrante.query.filter_by(
            grupo_id=grupo_id, 
            aluno_id=aluno_id
        ).first()
        
        if integrante_existente:
            return jsonify({'error': 'Aluno já é integrante deste grupo'}), 400
        
        novo_integrante = GrupoIntegrante(
            grupo_id=grupo_id,
            aluno_id=aluno_id,
            funcao=funcao
        )
        
        db.session.add(novo_integrante)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Integrante adicionado com sucesso',
            'integrante': novo_integrante.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@grupo_bp.route('/<int:grupo_id>/integrantes/<int:integrante_id>', methods=['DELETE'])
def remove_integrante(grupo_id, integrante_id):
    try:
        integrante = GrupoIntegrante.query.filter_by(
            id=integrante_id, 
            grupo_id=grupo_id
        ).first_or_404()
        
        db.session.delete(integrante)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Integrante removido com sucesso'
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
