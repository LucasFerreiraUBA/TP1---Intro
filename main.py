from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from models import db

app = Flask(__name__, static_url_path='/templates')
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/tpdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Constantes
MAXIMO_REGISTROS_POR_DEFECTO = 10


# Front
@app.route('/', methods=['GET'])
def indice():
    return render_template('index.html')


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
    empleado = {
        'nombre': 'juan',
        'id': id
    }
    return render_template('empleados/empleado.html', empleado=empleado)


@app.route('/registros/agregar', methods=['GET'])
def front_agregar_registro():
    return render_template('registros/nuevo_registro.html')

@app.route('/registros', methods=['GET'])
def front_agregar_registro():
    return render_template('registros/nuevo_registro.html')

# Endpoints Registros
@app.route('/api/v1/registros', methods=['GET'])
def obtener_registros():
    return 'todos los registros'


@app.route('/api/v1/registros/<int:id>', methods=['GET'])
def obtener_registro(id):
    return 'un registro segun id'


@app.route('/api/v1/registros', methods=['POST'])
def agregar_registro(request):
    return 'agregar un registro'


@app.route('/api/v1/registros/<int:id>', methods=['DELETE'])
def eliminar_registro(id):
    return 'eliminar un registro'


@app.route('/api/v1/registros/<int:id>', methods=['PUT'])
def agregar_registro(id):
    return 'actualizar un registro'

# Endpoints Empleados


@app.route('/api/v1/empleados/<int:id>', methods=['GET'])
def obtener_empleado(id):
    return 'un empleado'


@app.route('/api/v1/empleados', methods=['GET'])
def obtener_empleados():
    return 'todos los empleados'


@app.rotue('/api/v1/empleados', methods=['POST'])
def agregar_empleado():
    return 'agregar empleado'


@app.rotue('/api/v1/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado():
    return 'eliminar empleado'


@app.route('/api/v1/empleados/<int:id>', methods=['PUT'])
def actualizar_empleado(id):
    return 'actualizar empleado'


db.init_app(app)

# @app.before_first_request
# def iniciar_db():
#    db.drop_all()
#    db.create_all()

# with app.app_context():
#    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
