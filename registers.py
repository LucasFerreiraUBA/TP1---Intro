from flask import Blueprint, jsonify, request
from models import Register, Employee, db
from datetime import time, datetime, timedelta

registers = Blueprint('registers', __name__)

# Constantes
QUERY_LIMIT = 100

@registers.route('/api/v1/registers', methods=['GET'])
def get_registers(): #OK
    try:
        registers = Register.query.all()
        registers_data = []
        for register in registers:
            employee = db.session.query(Employee).get(register.employee_id)

            register_data = {
                'id': register.id,
                'horario': register.horario.isoformat(),
                'employee': {
                    'nombre': employee.nombre,
                    'apellido': employee.apellido,
                    'check_in_time': employee.check_in_time.strftime('%H:%M:%S'),
                    'check_out_time': employee.check_out_time.strftime('%H:%M:%S')
                },
                'is_check_in': register.is_check_in,
                'deviation_seconds': register.deviation_seconds,
            }
            registers_data.append(register_data)
        return jsonify(registers_data), 200
    except:
        return jsonify({"message": "An unexpecter error has occurred"}), 400

@registers.route('/api/v1/registers/<int:id>', methods=['GET'])
def get_register(id): #OK
    try:
        register = Register.query.get(id)

        employee = db.session.query(Employee).get(register.employee_id)

        if employee == None:
            return jsonify({'message':'Employee not found'})

        register_data = {
            'employee': {
                'id': employee.id,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'dni': employee.dni,
                },
            'is_check_in': register.is_check_in,
            'check_timestamp': register.horario.isoformat(),
            'deviation_seconds': register.deviation_seconds,
        }
        return jsonify(register_data), 200
    except:
        return jsonify({"message": "Register not found"}), 400


@registers.route('/api/v1/registers', methods=['POST'])
def add_new_register():#OK
    try:
        timestamp = request.json.get("timestamp")
        employee_id = int(request.json.get("employee_id"))

        employee = db.session.query(Employee).get(employee_id)

        if employee is None:
            return jsonify({'message': "Employee not found"}), 404

        check_datetime = datetime.fromisoformat(timestamp)
        (is_check_in, devation_seconds) = get_register_type(check_datetime, employee)

        register = db.session.query(Register).filter(Register.horario >= check_datetime.date(), Register.horario < check_datetime.date() + timedelta(days=1), Register.is_check_in == is_check_in,Register.employee_id == employee_id).first()

        if register == None:
            nuevo_registro = Register(
            horario=check_datetime, employee_id=employee_id, is_check_in=is_check_in, deviation_seconds=devation_seconds)
            db.session.add(nuevo_registro)
        else:
            register.check_timestamp = check_datetime,
            register.deviation_seconds = devation_seconds

        db.session.commit()

        if register == None:
            return jsonify({"message": "New register added successfully"}), 201
        else:
            return jsonify({"message": "The register was updated succesfully"}), 201
    
    except Exception as error:
       return jsonify({'message': "An unexpecter error has occurred"}), 400


@registers.route('/api/v1/registers/<int:id>', methods=['DELETE'])
def delete_register(id): #OK
    try:
        register = db.session.query(Register).get(id)
        db.session.delete(register)
        db.session.commit()

        return jsonify({"success": "Register deleted successfully"}, 201)
    except:
        return jsonify({"message": "An unexpecter error has occurred"}, 400)


@registers.route('/api/v1/registers/<int:id>', methods=['PUT'])
def update_register(id):#Falta implementar.
    try:
        register = Register.query.get(id)

        if register == None:
            return jsonify({'message':'employee does not exist'}),404
        register.horario = request.json.get("horario")
        register.employee_id = request.json.get("employee_id")
        register.is_check_in = request.json.get("is_check_in")

        db.session.commit()

        return jsonify({"message": 'Register updated successfully'}), 201
    except:
        return jsonify({"message": "Some error has ocurred"}), 400


def get_register_type(check_timestamp : datetime, employee: Employee):
    #Dado una hora de fichaje, y un employee devuelve si es una entrada y la diferencia en segundos
    right_check_in_datetime = datetime.combine(check_timestamp.date(), employee.check_in_time)
    right_check_out_datetime = datetime.combine(check_timestamp.date(), employee.check_out_time)
        
    delta_check_in = check_timestamp.timestamp() - right_check_in_datetime.timestamp()
    delta_check_out = check_timestamp.timestamp() - right_check_in_datetime.timestamp()

    is_check_in = abs(delta_check_in) < abs(delta_check_out)

    deviation_seconds = delta_check_out
    if(is_check_in):
        deviation_seconds = delta_check_in

    return (is_check_in, deviation_seconds)
