import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.Integer, primary_key = True)
    horario_entrada = db.Column(db.Time, nullable=False)
    horario_salida = db.Column(db.Time, nullable=False)
    registros = db.relationship("Registro")
    
class Registro(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.DateTime, nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    es_entrada = db.Column(db.Boolean, nullable = False, default = True)
    desfase = db.Column(db.Time, nullable= False)