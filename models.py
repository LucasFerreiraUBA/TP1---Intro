import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Employee(db.Model):
    __tablename__ = 'employees'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    dni = db.Column(db.String(255), unique=True, nullable=False)
    check_in_time = db.Column(db.Time, nullable=False)
    check_out_time = db.Column(db.Time, nullable=False)
    registers = db.relationship("Register")

    def __init__(self, first_name, last_name, dni, check_in_time, check_out_time):
        self.first_name = first_name
        self.last_name = last_name
        self.dni = dni
        self.check_in_time = check_in_time
        self.check_out_time = check_out_time

    def toDict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'dni': self.dni,
            'check_in_time': self.check_in_time.strftime('%H:%M:%S'),
            'check_out_time': self.check_out_time.strftime('%H:%M:%S'),
        }


class Register(db.Model):
    __tablename__ = 'registers'
    id = db.Column(db.Integer, primary_key=True)
    check_timestamp = db.Column(db.DateTime, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.id'))
    is_check_in = db.Column(db.Boolean, nullable=False, default=True)
    deviation_seconds = db.Column(db.Integer, nullable=False)

    def __init__(self, check_timestamp, employee_id, is_check_in, deviation_seconds):
        self.check_timestamp = check_timestamp
        self.deviation_seconds = deviation_seconds
        self.employee_id = employee_id
        self.is_check_in = is_check_in
        
    def toDict(self):
        return {
            'is_check_in':self.is_check_in,
            'check_timestamp':self.check_timestamp.isoformat(),
            'deviation_seconds':self.deviation_seconds,
            'id':self.id
        }

