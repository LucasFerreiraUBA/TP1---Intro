from flask import Blueprint, jsonify, request
from models import Register, Employee, db
from datetime import datetime, timedelta
import auxiliaries as aux

registers = Blueprint('registers', __name__)

# Constantes
QUERY_LIMIT = 100


@registers.route('/api/v1/registers', methods=['GET'])
def get_registers():
    '''
    Se obtinen todos los registros. Si no se espicifico mediante un param@limit, sera limitado por un valor default.
    '''
    try:
        query_limit = request.args.get('limit')
        
        if not query_limit:
            query_limit = QUERY_LIMIT
        
        registers_list = db.session.query(Register).limit(query_limit)

        registers_data = []
        for register in registers_list:
            employee = db.session.query(Employee).get(register.employee_id)

            register_data = {
                'id': register.id,
                'timestamp': register.check_timestamp.isoformat(),
                'employee': employee.toDict(),
                'is_check_in': register.is_check_in,
                'deviation_seconds': register.deviation_seconds,
            }
            registers_data.append(register_data)
        return jsonify(registers_data), 200
    except:
        return jsonify({'message': 'An unexpected error has occurred'}), 400


@registers.route('/api/v1/registers/<int:id>', methods=['GET'])
def get_register(id):
    '''
    Obtiene los detalles de un registro dado su @id 
    '''
    try:
        register = Register.query.get(id)
        employee = db.session.query(Employee).get(register.employee_id)

        if not employee:
            return jsonify({'message': 'Employee not found'})

        register_data = {
            'employee': employee.toDict(), 
            'is_check_in': register.is_check_in,
            'check_timestamp': register.check_timestamp.isoformat(),
            'deviation_seconds': register.deviation_seconds,
        }
        return jsonify(register_data), 200
    except:
        return jsonify({'message': 'Register not found'}), 400


@registers.route('/api/v1/registers', methods=['POST'])
def add_new_register():
    '''
    Agrega un nuevo registro con los datos que hay en el body.
    Si el registro ya existe, lo actualiza siempre y cuando:
    Si el registro es proximo al horario de entrada: Cuando no es posterior al vigente.
    Si el registro es  proximo al horario de salida: Cuando es posterior al vigente.
    '''
    try:
        timestamp = request.json.get('timestamp')
        employee_id = int(request.json.get('employee_id'))

        employee = db.session.query(Employee).get(employee_id)

        if employee is None:
            return jsonify({'message': 'Employee not found'}), 404

        check_datetime = datetime.fromisoformat(timestamp)
        (is_check_in, deviation_seconds) = aux.get_register_type(check_datetime, employee)

        register = db.session.query(Register).filter(
            Register.check_timestamp >= check_datetime.date(),
            Register.check_timestamp < check_datetime.date() + timedelta(days=1),
            Register.is_check_in == is_check_in,
            Register.employee_id == employee_id
        ).first()

        if register is None:
            new_register = Register(
                check_timestamp=check_datetime,
                employee_id=employee_id, 
                is_check_in=is_check_in,
                deviation_seconds=deviation_seconds,
            )
            db.session.add(new_register)
        else:
            register.check_timestamp = check_datetime,
            register.deviation_seconds = deviation_seconds

        db.session.commit()

        if not register:
            return jsonify({'success': 'New register added successfully'}), 201
        
        return jsonify({'success': 'The register was updated successfully'}), 201

    except Exception as error:
        print(error)
        return jsonify({'message': 'An unexpecter error has occurred'}), 400


@registers.route('/api/v1/registers/<int:id>', methods=['DELETE'])
def delete_register(id):
    '''
    Elimina un registro dado un @id
    '''
    try:
        register = db.session.query(Register).get(id)
        db.session.delete(register)
        db.session.commit()

        return jsonify({'success': 'Register deleted successfully'}), 201
    except:
        return jsonify({'message': 'An unexpecter error has occurred'}), 400


@registers.route('/api/v1/registers/<int:id>', methods=['PUT'])
def update_register(id):
    '''
    Actualiza los datos de un registro dado su @id con los datos del body.
    '''
    try:
        register = Register.query.get(id)

        if not register:
            return jsonify({'message': 'Register does not exist'}), 404

        check_time = datetime.fromisoformat(request.json.get('check_timestamp'))
        employee_id = int(request.json.get('employee_id'))
        is_check_in = bool(int(request.json.get('is_check_in')))

        register.check_timestamp = aux.replace_attr(register.check_timestamp, check_time)
        register.employee_id = aux.replace_attr(register.employee_id, employee_id)
        register.is_check_in = aux.replace_attr(register.is_check_in, is_check_in)
        
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({'message': 'Employee does not exist'}), 404

        register.deviation_seconds = aux.deviation(employee, register.check_timestamp, register.is_check_in)
        db.session.commit()

        return jsonify({'success': 'Register updated successfully'}), 201
    except:
        return jsonify({'message': 'Some error has occurred'}), 400
