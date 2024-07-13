from models import db, Employee
from flask import jsonify, request, Blueprint

QUERY_LIMIT = 100

employees = Blueprint('employees', __name__)


@employees.route('/api/v1/employees/<int:id>', methods=['GET'])
def get_employee(id):  # OK
    try:
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({'message': f'Employee with id:{id} does not exist'}), 400

        employee_data = employee.toDict()

        return jsonify(employee_data), 200
    except:
        return jsonify({'message': 'An unexpected error has occurred'}), 400


@employees.route('/api/v1/employees', methods=['GET'])
def get_employees():  # OK
    try:
        query_limit = request.args.get('limit')

        if not query_limit:
            query_limit = QUERY_LIMIT

        all_employees = Employee.query.limit(query_limit).all()
        employees_list = []

        for employee in all_employees:
            employee_data = employee.toDict()

            employees_list.append(employee_data)

        return jsonify(employees_list), 200
    except:
        return jsonify({'message': 'An unexpected error has occurred'}), 500


@employees.route('/api/v1/employees', methods=['POST'])
def add_new_employee():  # OK

    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    dni = request.json.get('dni')
    check_in_time = request.json.get('check_in_time')
    check_out_time = request.json.get('check_out_time')

    if not (first_name and last_name and dni and check_in_time and check_out_time):
        return jsonify({'message': 'There is a missing paramester in the body'}), 400

    employee = db.session.query(Employee).filter(Employee.dni == dni).first()

    if employee is not None:
        return jsonify({'message': 'There is already a employee with the same DNI'}), 400

    new_employee = Employee(
        first_name=first_name,
        last_name=last_name,
        dni=dni,
        check_in_time=check_in_time,
        check_out_time=check_out_time
    )
    db.session.add(new_employee)
    db.session.commit()

    employee = db.session.query(Employee).filter(Employee.dni == dni).first()

    return jsonify({'success': f'Added employee with DNI:{dni} ', 'employee': employee.toDict()}), 200


@employees.route('/api/v1/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):  # OK
    try:
        employee = Employee.query.get(id)

        if employee is None:
            return jsonify({'message': 'Employee not found'})

        db.session.delete(employee)
        db.session.commit()

        return jsonify({'success': 'Deleted successfully', 'employee': employee.toDict()}), 201
    except:
        return jsonify({'message': 'An unexpected error has occurred'}), 404


@employees.route('/api/v1/employees/<int:id>', methods=['PUT'])
def update_employee(id):  # OK
    try:
        employee = db.session.query(Employee).get(id)

        if not employee:
            return jsonify({'message': 'Employee not found'}), 404

        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        dni = request.json.get('dni')
        check_in_time = request.json.get('check_in_time')
        check_out_time = request.json.get('check_out_time')

        if first_name:
            employee.first_name = first_name

        if last_name:
            employee.last_name = last_name

        if dni:
            employee.dni = dni

        if check_in_time:
            employee.check_in_time = check_in_time

        if check_out_time:
            employee.check_out_time = check_out_time

        db.session.commit()
        return jsonify({'success': 'Employee successfully updated', 'employee': employee.toDict()}), 201
    except:
        return jsonify({'message': 'An unexpected error has occurred'}), 400
