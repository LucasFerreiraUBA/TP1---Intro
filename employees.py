from models import db, Employee, Register
from flask import  jsonify, request, Blueprint
from sqlalchemy import or_, and_
import auxiliaries as aux

QUERY_LIMIT = 100

employees = Blueprint('employees', __name__)

@employees.route('/api/v1/employees/<int:id>', methods=['GET'])
def get_employee(id):
    '''
    Devuelve los datos de un empleado dado un @id.
    '''
    try:
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({'message': f'Employee with id:{id} does not exist'}), 400

        employee_data = employee.toDict()

        return jsonify(employee_data), 200
    except:
        return jsonify({'message': 'An unexpected error has occurred'}), 400


@employees.route('/api/v1/employees', methods=['GET'])
def get_employees():
    '''
    Devuelve una lista de todos los empleados
    '''
    try:
        query_limit = request.args.get('limit',QUERY_LIMIT, int)

        all_employees = Employee.query.order_by(Employee.last_name.asc()).limit(query_limit).all()
        employees_list = []

        for employee in all_employees:
            employee_data = employee.toDict()

            employees_list.append(employee_data)

        return jsonify(employees_list), 200
    except Exception as error:
        print(error)
        return jsonify({'message': 'An unexpected error has occurred'}), 500


@employees.route('/api/v1/employees', methods=['POST'])
def add_new_employee():
    '''
    Agrega un nuevo empleado con los datos presentes en el body.
    '''

    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')
    dni = request.json.get('dni')
    check_in_time = request.json.get('check_in_time')
    check_out_time = request.json.get('check_out_time') 

    if not all([first_name, last_name, dni, check_in_time, check_out_time]):
        return jsonify({'message': 'There is a missing parameter in the body'}), 400

    employee = db.session.query(Employee).filter(Employee.dni == dni).first()

    if not (employee is None):
        return jsonify({'message': 'There is already a employee with the same DNI'}), 400

    new_employee = Employee(
        first_name=first_name,
        last_name=last_name,
        dni=dni,
        check_in_time=check_in_time,
        check_out_time=check_out_time,
    )
    db.session.add(new_employee)
    db.session.commit()

    employee = db.session.query(Employee).filter(Employee.dni == dni).first()

    return jsonify({'success': f'Added employee with DNI:{dni}', 'employee': employee.toDict()}), 200


@employees.route('/api/v1/employees/<int:id>', methods=['DELETE'])
def delete_employee(id):
    '''
    Elimina a un empleado dado su @id.
    '''
    try:
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({'message': 'Employee not found'})
        
        db.session.delete(employee)

        db.session.query(Register).filter(Register.employee_id == employee.id).delete()
        db.session.commit()

        return jsonify({'success': 'Deleted successfully', 'employee': employee.toDict()}), 201
    except:
        return jsonify({'message': 'An unexpected error has occurred'}), 404


@employees.route('/api/v1/employees/<int:id>', methods=['PUT'])
def update_employee(id):
    '''
    Dado un empleado mediante su @id, actualiza sus datos presentes en el body.
    '''
    try:
        employee = db.session.query(Employee).get(id)

        if not employee:
            return jsonify({'message': 'Employee not found'}), 404

   
        first_name = request.json.get('first_name')
        last_name = request.json.get('last_name')
        dni = request.json.get('dni')
        check_in_time = request.json.get('check_in_time')
        check_out_time = request.json.get('check_out_time')

        employee.first_name = str(aux.replace_attr(employee.first_name, first_name))
        employee.last_name = str(aux.replace_attr(employee.last_name, last_name))
        employee.dni = aux.replace_attr(employee.dni, dni)
        employee.check_in_time = aux.replace_attr(employee.check_in_time, check_in_time)
        employee.check_out_time = aux.replace_attr(employee.check_out_time, check_out_time)

        db.session.commit()
        return jsonify({'success': 'Employee successfully updated', 'id': employee.id}), 201
    except Exception as error:
        print(error)
        return jsonify({'error': 'An unexpected error has occurred'}), 400


@employees.route('/api/v1/employees/<int:id>/registers/unpunctual/', methods=['GET'])
def get_employee_unpunctual_registers(id):
    '''
    Dada una toleancia de entrada y salida, ademas de un @id de empleado, devuelve los registros inpuntuales.
    '''
    try:
        employee = db.session.query(Employee).get(id)

        if not employee:
            return jsonify({'message': 'Employee not found'}), 404
        
        entering_tolerancy = int(request.args.get('entering_tolerancy', 0)) 
        leaving_tolerancy = int(request.args.get('leaving_tolerancy', 0)) 
        
        entering_tolerancy_seconds = entering_tolerancy * 60
        leaving_tolerancy_seconds = leaving_tolerancy * 60

        register_list = db.session.query(Register).filter(
            or_(
            and_(Register.is_check_in == True, Register.deviation_seconds > entering_tolerancy_seconds),
            and_(Register.is_check_in == False, Register.deviation_seconds < leaving_tolerancy_seconds)
            ), 
            Register.employee_id == id,
            ).order_by(Register.check_timestamp.desc()).all()

        registers_data = []
      
        for register in register_list:
            registers_data.append(register.toDict())

        return jsonify(registers_data), 201
    except:
        return jsonify({'error':'An unexpected error had occurred'}), 400

@employees.route('/api/v1/employees/<int:id>/registers/', methods=['GET'])
def get_employee_registers(id):
    '''
    Dado un empleado mediante su @id, devuelve sus registros de entrada y salida.
    '''
    try:
        employee = db.session.query(Employee).get(id)

        if not employee:
            return jsonify({'message': 'Employee not found'}), 404
        
        register_list = db.session.query(Register)      \
        .filter(Register.employee_id == id)             \
        .order_by(Register.check_timestamp.desc()).all()

        registers_data = []
        for register in register_list:
            registers_data.append(register.toDict())

        return jsonify(registers_data),201
    
    except:
        return jsonify({'error':'An unexpected error had occurred'}), 400
