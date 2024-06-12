from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from models import db

app = Flask(__name__, static_url_path='/templates')
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/tpdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


@app.route('/')
def hola_mundo():
    return render_template('index.html')

@app.route('/empleados')
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

@app.route('/empleado/<int:id>')
def empleado(id):
    empleado = {
        'nombre': 'juan',
        'id' : id
    }
    return render_template('empleados/empleado.html', empleado=empleado)



#Endpoints registros
@app.route('api/v1/registros')
def obtener_registros():
    return 'todos los registros'

@app.route('api/v1/registros/<int:id>')
def obtener_registro(id):
    return 'un registro segun id'

@app.route('api/v1/registros', methods=['POST'])
def agregar_registro(request):
    return 'agregar un registro'
    
@app.route('api/v1/registros/<int:id>', methods=['DELETE'])
def eliminar_registro(id):
    return 'eliminar un registro'

@app.route('api/v1/registros/<int:id>', methods=['PUT'])
def agregar_registro(id):
    return 'actualizar un registro'











db.init_app(app)


# @app.before_first_request
# def iniciar_db():
#    db.drop_all()
#    db.create_all()

# with app.app_context():
#    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
