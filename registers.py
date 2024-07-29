from flask import Blueprint, jsonify, request
from models import Register, Employee, db
from datetime import datetime, timedelta
from sqlalchemy import or_, and_

registers = Blueprint('registers', __name__)

# Constantes
QUERY_LIMIT = 100


@registers.route('/api/v1/registers', methods=['GET'])
def get_registers():
    #Se obtinen todos los registros. Si no se espicifico mediante un param@limit, sera limitado por un valor default.
    try:
        query_limit = request.args.get('limit', QUERY_LIMIT)
        
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
    #Obtiene los detalles de un registro dado si @id 
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
    #Agrega un nuevo registro con los datos que hay en el body.
    #Si el registro ya existe, lo actualiza siempre y cuando:
    #   Si el registro es proximo al horario de entrada: Cuando no es posterior al vigente.
    #   Si el registro es  proximo al horario de salida: Cuando es posterior al vigente.
    try:
        timestamp = request.json.get('timestamp')
        employee_id = int(request.json.get('employee_id'))

        employee = db.session.query(Employee).get(employee_id)

        if employee is None:
            return jsonify({'message': 'Employee not found'}), 404

        check_datetime = datetime.fromisoformat(timestamp)
        (is_check_in, deviation_seconds) = get_register_type(check_datetime, employee)

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
    #Elimina un registro dado un @id
    try:
        register = db.session.query(Register).get(id)
        db.session.delete(register)
        db.session.commit()

        return jsonify({'success': 'Register deleted successfully'}), 201
    except:
        return jsonify({'message': 'An unexpecter error has occurred'}), 400


@registers.route('/api/v1/registers/<int:id>', methods=['PUT'])
def update_register(id):
    #Actualiza los datos de un registro dado su @id con los datos del body.
    try:
        register = Register.query.get(id)

        if not register:
            return jsonify({'message': 'Register does not exist'}), 404

        check_time = datetime.fromisoformat(request.json.get('check_timestamp'))
        employee_id = int(request.json.get('employee_id'))
        is_check_in = bool(int(request.json.get('is_check_in')))

        register.check_timestamp = replace_attr(register.check_timestamp, check_time)
        register.employee_id = replace_attr(register.employee_id, employee_id)
        register.is_check_in = replace_attr(register.is_check_in, is_check_in)
        
        employee = Employee.query.get(employee_id)

        if not employee:
            return jsonify({'message': 'Employee does not exist'}), 404

        register.deviation_seconds = deviation(employee, register.check_timestamp, register.is_check_in)
        db.session.commit()

        return jsonify({'success': 'Register updated successfully'}), 201
    except:
        return jsonify({'message': 'Some error has occurred'}), 400

@registers.route('/api/v1/registers/unpunctual', methods=['GET'])
def get_employee_unpunctual_registers():
    #Dada una toleancia de entrada y salida, devuelve los registros inpuntuales.
    try:
        query_limit = request.args.get('limit', QUERY_LIMIT, int)
        
        entering_tolerancy = request.args.get('tolerancy_in', 0, int)
        leaving_tolerancy = request.args.get('tolerancy_out', 0, int)
  
        entering_tolerancy_seconds = entering_tolerancy * 60
        leaving_tolerancy_seconds = leaving_tolerancy * 60

        register_list = db.session.query(Register).filter(
            or_(
            and_(Register.is_check_in == True, Register.deviation_seconds > entering_tolerancy_seconds),
            and_(Register.is_check_in == False, Register.deviation_seconds < leaving_tolerancy_seconds)
            )).order_by(Register.check_timestamp.desc()).limit(query_limit).all()

        registers_data = []
      
        for register in register_list:
            employee = db.session.query(Employee).get(register.employee_id)
            register_data = {
                'id': register.id,
                'timestamp': register.check_timestamp.isoformat(),
                'employee': employee.toDict(),
                'is_check_in': register.is_check_in,
                'deviation_seconds': register.deviation_seconds,
            }
            registers_data.append(register_data)


        return jsonify(registers_data), 201
    except Exception as error:
        print(error)
        return jsonify({'error':'An unexpected error had occurred'}), 400

def get_register_type(check_timestamp: datetime, employee: Employee):
    # Dado una hora de fichaje, y un employee devuelve si es una entrada y la diferencia en segundos

    right_check_in_datetime = datetime.combine(check_timestamp.date(), employee.check_in_time)
    right_check_out_datetime = datetime.combine(check_timestamp.date(), employee.check_out_time)

    delta_check_in = check_timestamp.timestamp() - right_check_in_datetime.timestamp()
    delta_check_out = check_timestamp.timestamp() - right_check_out_datetime.timestamp()

    is_check_in = abs(delta_check_in) < abs(delta_check_out)

    deviation_seconds = delta_check_in if is_check_in else delta_check_out
    return is_check_in, deviation_seconds

def replace_attr(current, new):
    if new == None:
        return current
    return new

def deviation(employee: Employee, check_timestamp: datetime, is_check_in: bool):

    right_check_in_datetime = datetime.combine(check_timestamp.date(), employee.check_in_time)
    right_check_out_datetime = datetime.combine(check_timestamp.date(), employee.check_out_time)

    delta_check_in = check_timestamp.timestamp() - right_check_in_datetime.timestamp()
    delta_check_out = check_timestamp.timestamp() - right_check_out_datetime.timestamp()

    return delta_check_in if is_check_in else delta_check_out