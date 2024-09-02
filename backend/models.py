from . import db  # Importa o objeto db

class Consulta(db.Model):
    __tablename__ = 'consultas'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), nullable=False)
    idade_grupo = db.Column(db.String(20), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    total = db.Column(db.Float, nullable=False)
