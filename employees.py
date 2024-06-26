from models import db, Employee, Registro
from flask import  jsonify, request, Blueprint

QUERY_LIMIT = 100

employees = Blueprint('employees', __name__)


@employees.route('/api/v1/employees/<int:id>', methods=['GET'])
def get_employee(id): #OK
    try:
        employee = Employee.query.get(id)

        if not employee:
            return jsonify({'message': f'Employee with id:{id} does not exist'}), 400

        employee_data = {
            'id': employee.id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'dni': employee.dni,
            'check_in_time': employee.check_in_time.strftime('%H:%M:%S'),
            'check_out_time': employee.check_out_time.strftime('%H:%M:%S'),
        }

        return jsonify(employee_data), 200
    except:
        return jsonify({"message": "An unexpected error has occurred"}), 400

@employees.route('/api/v1/employees', methods=['GET'])
def get_employees(): #OK
    try:
        query_items_limit = request.args.get('limit')

        if not query_items_limit:
            query_items_limit = QUERY_LIMIT

        employees = Employee.query.limit(query_items_limit).all()
        employees_list = []

        for employee in employees:
            employee_data = employee.toDict()
            
            employees_list.append(employee_data)

        return jsonify(employees_list), 200
    except:
        return jsonify({'message': 'An unexpected error has occurred'}), 500


@employees.route('/api/v1/employees', methods=['POST'])
def add_new_employee():#OK

    fist_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    dni = request.json.get("dni")
    check_in_time = request.json.get("check_in_time")
    check_out_time = request.json.get("check_out_time")

    if not (fist_name and last_name and dni and check_in_time and check_out_time):
        return jsonify({'message': 'There is a missing parameter in the body'}), 400
    
    empleado = db.session.query(Employee.id).filter(Employee.dni==dni).first()
    
    if empleado != None:
        return jsonify({'message': 'There is already a employee with the same DNI'}), 400

    new_employee = Employee(
        fist_name=fist_name,
        last_name=last_name,
        dni=dni,
        check_in_time=check_in_time,
        check_out_time=check_out_time
        )
    db.session.add(new_employee)
    db.session.commit()

    employee = db.session.query(Employee.id).filter(Employee.dni==dni).first()

    return jsonify({"sucess": f"Added employee with DNI:{dni} ", "id":empleado.id, 'employee': employee.toDict()}), 200 #debe ir sucess para que no aparesca un aviso

@employees.route('/api/v1/employees/<int:id>', methods=['DELETE'])
def delete_employee(id): #OK
    try:
        employee = Employee.query.get(id)

        if employee == None:
            return jsonify({'message': 'Employee not found'})
        db.session.delete(employee)
        db.session.commit()
        
        return jsonify({"message": "Deleted successfully"}), 201
    except:
        return jsonify({"message": "An unexpected error has occurred"}), 404


@employees.route('/api/v1/employees/<int:id>', methods=['PUT'])
def update_employee(id): #OK
    try:
        employee = db.session.query(Employee).get(id)

        if not employee:
            return jsonify({'message': 'Employee not found'}), 404

        first_name = request.json.get("first_name")
        last_name = request.json.get("last_name")
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
        return jsonify({"message": "Employee successfully updated", "employee": employee.toDict()}), 201
    except:
        return jsonify({"message": "An unexpected error has occurred"}), 400

