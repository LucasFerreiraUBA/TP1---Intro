from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, time, timedelta
from models import db, Empleado, Registro

from registros import registros
from employees import employees

app = Flask(__name__, static_url_path='/templates/')
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:user@localhost:5432/tpdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.register_blueprint(registros)
app.register_blueprint(empleados)


# Front routes
@app.route('/', methods=['GET'])
def indice():
    return render_template('index.html')

@app.route('/fichar', methods=['GET'])
def front_fichar_empleado():
    return render_template('fichar/fichar.html')

@app.route('/empleados/agregar', methods=['GET'])
def front_create_employee():
    return render_template('empleados/agregar/agregar.html')

@app.route('/empleados/editar', methods=['GET'])
def front_edit_employee():
    return render_template('empleados/editar/editar.html')

@app.route('/empleados', methods=['GET'])
def empleados():
    empleados = [
        {
            'nombre': 'juan'
        },
        {
            'nombre': 'lucas'
        }
    ]
    return render_template('empleados/empleados.html', empleados=empleados)


@app.route('/empleados/<int:id>', methods=['GET'])
def empleado(id):
    empleado = Empleado.query.get(id)
    return render_template('empleados/empleado.html', empleado=empleado)


@app.route('/registros/agregar', methods=['GET'])
def front_agregar_registro():
    return render_template('registros/nuevo_registro.html')


@app.route('/registros', methods=['GET'])
def front_registros():
    return render_template('registros/nuevo_registro.html')


db.init_app(app)

if __name__ == '__main__': 
    
    with app.app_context():
        #db.drop_all()
        db.create_all()
    app.run(debug=True, port=port)
