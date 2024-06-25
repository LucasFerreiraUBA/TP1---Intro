import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Empleado(db.Model):
    __tablename__ = 'empleados'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    apellido = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.String(255), unique=True, nullable=False)
    horario_entrada = db.Column(db.Time, nullable=False)
    horario_salida = db.Column(db.Time, nullable=False)
    registros = db.relationship("Registro")
    
    def __init__(self, nombre, apellido, dni, horario_entrada, horario_salida):
        self.nombre = nombre
        self.apellido = apellido
        self.dni = dni
        self.horario_entrada = horario_entrada
        self.horario_salida = horario_salida
    
    
    
class Registro(db.Model):
    __tablename__ = 'registros'
    id = db.Column(db.Integer, primary_key=True)
    horario = db.Column(db.DateTime, nullable=False)
    empleado_id = db.Column(db.Integer, db.ForeignKey('empleados.id'))
    es_entrada = db.Column(db.Boolean, nullable = False, default = True)
    desfase = db.Column(db.Interval, nullable= False)
    
    def __init__(self, horario, empleado_id, es_entrada, desfase):
        self.horario = horario
        self.desfase = desfase
        self.empleado_id = empleado_id
        self.es_entrada = es_entrada