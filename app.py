from flask import Flask, render_template
from flask_cors import CORS
from models import db

from registers import registers
from employees import employees

app = Flask(__name__, static_url_path='/templates/')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:user@localhost:5432/tpdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
PORT = 5000

app.register_blueprint(registers)
app.register_blueprint(employees)

# Front routes
@app.route('/', methods=['GET'])
def indice():
    return render_template('index.html')


@app.route('/fichar', methods=['GET'])
def front_fichar_empleado():
    return render_template('sign_up/sign_up.html')


@app.route('/employees', methods=['GET'])
def empleados():
    return render_template('employees/employees.html')


@app.route('/empleados/agregar', methods=['GET'])
def front_create_employee():
    return render_template('employees/add_employee/add_employee.html')


@app.route('/empleados/editar', methods=['GET'])
def front_edit_employee():
    return render_template('employees/edit_employee/edit_employee.html')


@app.route('/empleados/<int:id>', methods=['GET'])
def empleado(id):
    return render_template('employees/employee.html')


@app.route('/registros', methods=['GET'])
def front_registros():
    return render_template('registers/registers.html')


@app.route('/registros/agregar', methods=['GET'])
def front_agregar_registro():
    return render_template('registers/add_register/add_register.html')


@app.route('/registros/editar', methods=['GET'])
def front_editar_registro():
    return render_template('registers/edit_register/edit_register.html')


@app.errorhandler(404)
def front_error(e):
    return render_template('page_not_found/page_not_found.html')

db.init_app(app)

if __name__ == '__main__':
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True, port=PORT)
