from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

from models import db, Empleado, Registro

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
    try:
        registros = Registro.query.all()
        registros_data = []
        for registro in registros:
            registro_data = {
                'id' : registro.id,
                'horario' : registro.horario,
                'empleado_id' : registro.empleado_id,
                'es_entrada' : registro.es_entrada,
                'desfase' : registro.desfase,
            }
            registros_data.append(registro_data)
        return jsonify(registros_data)
    except:
        return jsonify({"error": "No se pudo obtener los registros"}), 400


@app.route('/api/v1/registros/<int:id>', methods=['GET'])
def obtener_registro(id):
    try:
        registro = Registro.query.get(id)
        registro_data = {
            'id' : registro.id,
            'horario' : registro.horario,
            'empleado_id' : registro.empleado_id,
            'es_entrada' : registro.es_entrada,
            'desfase' : registro.desfase,
        }
        return jsonify(registro_data)
    except:
        return jsonify({"error": "Registro Inexistente"}), 400


@app.route('/api/v1/registros', methods=['POST'])
def agregar_registro():
    horario = request.json.get("horario")
    empleado_id = request.json.get("empleado_id")
    es_entrada = request.json.get("es_entrada")
    desfase = request.json.get("desfase")
    nuevo_registro = Registro(horario=horario, empleado_id=empleado_id, es_entrada=es_entrada, desfase=desfase)
    db.session.add(nuevo_registro)
    db.session.commit()
    return jsonify({"msg" : "Agregado Exitosamente"}, 201)


@app.route('/api/v1/registros/<int:id>', methods=['DELETE'])
def eliminar_registro(id):
    try:
        registro = Registro.query.get(id)
        db.session.delete(registro)
        db.session.commit()
        return jsonify({"msg" : "Borrado Exitosamente"}, 201)
    except:
        return jsonify({"msg" : "Registro desconocido"}, 400)


@app.route('/api/v1/registros/<int:id>', methods=['PUT'])
def modificar_registro(id):
    try:
        registro = Registro.query.get(id)
        registro.horario = request.json.get("horario")
        registro.empleado_id = request.json.get("empleado_id")
        registro.es_entrada = request.json.get("es_entrada")
        registro.desfase = request.json.get("desfase")
        db.session.commit()
        return jsonify({"msg" : "Actualizado Exitosamente"}, 201)
    except:
        return jsonify({"msg" : "Registro desconocido"}, 400)

# Endpoints Empleados

@app.route('/api/v1/empleados/<int:id>', methods=['GET'])
def obtener_empleado(id):
    try:
        empleado = Empleado.query.get(id)
        empleado_data = {
            'id' : empleado.id,
            'nombre' : empleado.nombre,
            'apellido' : empleado.apellido,
            'dni' : empleado.dni,
            'horario_entrada' : empleado.horario_entreda,
            'horario_salida' : empleado.horario_salida,
            'registros' : empleado.registros,
        }
        return jsonify(empleado_data)
    except:
        return jsonify({"error": "No se pudo obtener los registros"}), 400

@app.route('/api/v1/empleados', methods=['GET'])
def obtener_empleados(request):
    try:
        datos = request.json
        maximo_registros = datos.get('maximo')

        if not maximo_registros:
            maximo_registros = MAXIMO_REGISTROS_POR_DEFECTO

        empleados = Empleado.query.limit(maximo_registros).all()
        lista_empleados = []

        for empleado in empleados:
            datos_empleado = {
                'id' : empleado.id,
                'nombre' : empleado.nombre,
                'apellido' : empleado.apellido,
                'dni' : empleado.dni,
                'horario_entrada' : empleado.horario_entreda,
                'horario_salida' : empleado.horario_salida,
                'registros' : empleado.registros,
            }

            lista_empleados.append(datos_empleado)

        return jsonify({'empleados': lista_empleados}), 200

    except Exception as error:
        return jsonify({'message': 'Error interno del servidor'}), 500


@app.rotue('/api/v1/empleados', methods=['POST'])
def agregar_empleado():
    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    dni = request.json.get("dni")
    horario_entrada = request.json.get("horario_entrada")
    horario_salida = request.json.get("horario_salida")
    registros = request.json.get("registros")
    nuevo_empleado = Empleado(nombre=nombre, 
                              apellido=apellido, 
                              dni=dni, 
                              horario_entrada=horario_entrada, 
                              horariosalida=horario_salida,
                              registros=registros)
    db.session.add(nuevo_empleado)
    db.session.commit()
    return jsonify({"msg" : "Agregado Exitosamente"}, 201)


@app.rotue('/api/v1/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    try:
        empleado = Empleado.query.get(id)
        db.session.delete(empleado)
        db.session.commit()
        return jsonify({"msg" : "Borrado Exitosamente"}, 201)
    except:
        return jsonify({"msg" : "Empleado desconocido"}, 400)


@app.route('/api/v1/empleados/<int:id>', methods=['PUT'])
def actualizar_empleado(id):
    try:
        empleado = Empleado.query.get(id)
        empleado.nombre = request.json.get("nombre")
        empleado.apellido = request.json.get("apellido")
        empleado.dni = request.json.get("dni")
        empleado.horario_entrada = request.json.get("horario_entrada")
        empleado.horario_salida = request.json.get("horario_salida")
        empleado.registros = request.json.get("registros")
        db.session.commit()
        return jsonify({"msg" : "Actualizado Exitosamente"}, 201)
    except:
        return jsonify({"msg" : "Empleado desconocido"}, 400)


db.init_app(app)

# @app.before_first_request
# def iniciar_db():
#    db.drop_all()
#    db.create_all()

# with app.app_context():
#    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
