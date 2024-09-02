import time
import logging
from flask import Blueprint, request, jsonify
from .models import Consulta, db

main = Blueprint("main", __name__)

logging.basicConfig(level=logging.DEBUG)

@main.route('/', methods=['GET'])
def home():
    return "Backend online!", 200

@main.route('/calcular', methods=['POST'])
def calcular():
    start_time = time.time()

    try:
        data = request.json
        nome = data.get('nome')
        idade_grupo = data.get('idade_grupo')
        peso = data.get('peso', 0)

        if not nome:
            return jsonify({'error': 'Nome é obrigatório'}), 400
        if peso <= 0:
            return jsonify({'error': 'Peso deve ser maior que 0'}), 400

        # Cálculo do total de água recomendado
        if idade_grupo == 'adulto':
            total = peso * 35
        elif idade_grupo == 'crianca':
            total = peso * 50
        elif idade_grupo == 'gravida':
            total = peso * 35 + 300
        else:
            return jsonify({'error': 'Grupo de Idade Inválido'}), 400

        # Criação de uma nova consulta e salvamento no banco de dados
        nova_consulta = Consulta(nome=nome, idade_grupo=idade_grupo, peso=peso, total=total)
        db.session.add(nova_consulta)
        db.session.commit()

        response = jsonify({'total': total})
        logging.debug(f"Requisição processada em {time.time() - start_time:.2f} segundos")
        return response

    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {type(e).__name__}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Erro ao processar a requisição'}), 500

    finally:
        db.session.remove()  # Garante que a sessão seja finalizada corretamente

@main.route('/consultas/<nome>', methods=['GET'])
def consultar_resultados(nome):
    try:
        # Busca todas as consultas pelo nome fornecido
        consultas = Consulta.query.filter_by(nome=nome).all()

        # Verifica se alguma consulta foi encontrada
        if not consultas:
            return jsonify({'error': 'Nenhum resultado encontrado para o nome fornecido.'}), 404

        # Cria uma lista com os dados das consultas
        resultados = [
            {
                'nome': consulta.nome,
                'idade_grupo': consulta.idade_grupo,
                'peso': consulta.peso,
                'total': consulta.total
            }
            for consulta in consultas
        ]

        return jsonify(resultados), 200

    except Exception as e:
        logging.error(f"Erro ao consultar resultados: {type(e).__name__}: {e}")
        return jsonify({'error': 'Erro ao consultar resultados'}), 500

    finally:
        db.session.remove()  # Garante que a sessão seja finalizada corretamente
