import logging
from flask import Flask  # Importa o Flask
from flask_sqlalchemy import SQLAlchemy  # Importa o SQLAlchemy
from flask_cors import CORS  # Importa o CORS

# Inicializa a instância do SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)  # Habilita o CORS na aplicação

    # Configurações do banco de dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://admin:admin123@postgres-db:5432/agua_intake'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o SQLAlchemy com a aplicação Flask
    db.init_app(app)

    # Importa o modelo Consulta para garantir que está registrado no SQLAlchemy
    from .models import Consulta  

    # Cria as tabelas no banco de dados, se elas não existirem
    with app.app_context():
        try:
            logging.info("Tentando criar tabelas...")
            db.create_all()
            logging.info("Tabelas criadas com sucesso!")
        except Exception as e:
            logging.error(f"Erro ao criar tabelas: {e}")

    # Registra o blueprint das rotas
    from .routes import main
    app.register_blueprint(main)

    return app
