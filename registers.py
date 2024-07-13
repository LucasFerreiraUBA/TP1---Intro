from flask import Blueprint, jsonify, request
from models import Register, Employee, db
from datetime import time, datetime, timedelta

registers = Blueprint('registers', __name__)

# Constantes
QUERY_LIMIT = 100


@registers.route('/api/v1/registers', methods=['GET'])
def get_registers():  # OK
    try:
        registers_list = Register.query.all()
        registers_data = []
        for register in registers_list:
            employee = db.session.query(Employee).get(register.employee_id)

            register_data = {
                'id': register.id,
                'timestamp': register.check_timestamp.isoformat(),
                'employee': {
                    'first_name': employee.first_name,
                    'last_name': employee.last_name,
                    'check_in_time': employee.check_in_time.strftime('%H:%M:%S'),
                    'check_out_time': employee.check_out_time.strftime('%H:%M:%S')
                },
                'is_check_in': register.is_check_in,
                'deviation_seconds': register.deviation_seconds,
            }
            registers_data.append(register_data)
        return jsonify(registers_data), 200
    except:
        return jsonify({"message": "An unexpected error has occurred"}), 400


@registers.route('/api/v1/registers/<int:id>', methods=['GET'])
def get_register(id):  # OK
    try:
        register = Register.query.get(id)
        employee = db.session.query(Employee).get(register.employee_id)

        if employee is None:
            return jsonify({'message': 'Employee not found'})

        register_data = {
            'employee': {
                'id': employee.id,
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'dni': employee.dni,
            },
            'is_check_in': register.is_check_in,
            'check_timestamp': register.check_timestamp.isoformat(),
            'deviation_seconds': register.deviation_seconds,
        }
        return jsonify(register_data), 200
    except:
        return jsonify({"message": "Register not found"}), 400


@registers.route('/api/v1/registers', methods=['POST'])
def add_new_register():  # OK
    try:
        timestamp = request.json.get("timestamp")
        employee_id = int(request.json.get("employee_id"))

        employee = db.session.query(Employee).get(employee_id)

        if employee is None:
            return jsonify({'message': "Employee not found"}), 404

        check_datetime = datetime.fromisoformat(timestamp)
        (is_check_in, deviation_seconds) = get_register_type(check_datetime, employee)

        register = db.session.query(Register).filter(Register.check_timestamp >= check_datetime.date(),
                                                     Register.check_timestamp < check_datetime.date() + timedelta(days=1),
                                                     Register.is_check_in == is_check_in,
                                                     Register.employee_id == employee_id).first()

        if register is None:
            new_register = Register(
                check_timestamp=check_datetime, employee_id=employee_id, is_check_in=is_check_in,
                deviation_seconds=deviation_seconds)
            db.session.add(new_register)
        else:
            register.check_timestamp = check_datetime,
            register.deviation_seconds = deviation_seconds

        db.session.commit()

        if register is None:
            return jsonify({"message": "New register added successfully"}), 201
        else:
            return jsonify({"message": "The register was updated successfully"}), 201

    except Exception as error:
        print(error)
        return jsonify({'message': "An unexpecter error has occurred"}), 400


@registers.route('/api/v1/registers/<int:id>', methods=['DELETE'])
def delete_register(id):  # OK
    try:
        register = db.session.query(Register).get(id)
        db.session.delete(register)
        db.session.commit()

        return jsonify({"success": "Register deleted successfully"}, 201)
    except:
        return jsonify({"message": "An unexpecter error has occurred"}, 400)


@registers.route('/api/v1/registers/<int:id>', methods=['PUT'])
def update_register(id):
    try:
        register = Register.query.get(id)

        if register is None:
            return jsonify({'message': 'employee does not exist'}), 404

        check_time = request.json.get("check_timestamp")
        if not check_time is None:
            register.check_time = check_time

        employee_id = request.json.get("employee_id")
        if not employee_id is None:
            register.employee_id = employee_id

        is_check_in = request.json.get("is_check_in")
        if not is_check_in is None:
            register.is_check_in = is_check_in

        db.session.commit()

        return jsonify({"message": 'Register updated successfully'}), 201
    except:
        return jsonify({"message": "Some error has occurred"}), 400


def get_register_type(check_timestamp: datetime, employee: Employee):
    # Dado una hora de fichaje, y un employee devuelve si es una entrada y la diferencia en segundos

    right_check_in_datetime = datetime.combine(check_timestamp.date(), employee.check_in_time)
    right_check_out_datetime = datetime.combine(check_timestamp.date(), employee.check_out_time)

    delta_check_in = check_timestamp.timestamp() - right_check_in_datetime.timestamp()
    delta_check_out = check_timestamp.timestamp() - right_check_in_datetime.timestamp()

    is_check_in = abs(delta_check_in) < abs(delta_check_out)

    deviation_seconds = delta_check_out
    if is_check_in:
        deviation_seconds = delta_check_in

    return is_check_in, deviation_seconds
