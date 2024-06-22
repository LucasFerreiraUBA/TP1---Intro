from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS #instalar flask-cors de python
from datetime import datetime
from models import db, Empleado, Registro

app = Flask(__name__, static_url_path='/templates/')
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:user@localhost:5432/tpdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Constantes
MAX_REGISTROS = 100


# Front
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


# Endpoints Registros ########################################

# OK, falta probar
@app.route('/api/v1/registros', methods=['GET'])
def obtener_registros():
    try:
        registros = Registro.query.all()
        registros_data = []
        for registro in registros:
            empleado = db.session.query(Empleado).get(registro.empleado_id)

            registro_data = {
                'id': registro.id,
                'horario': registro.horario.isoformat(),
                'empleado': {
                    'nombre': empleado.nombre,
                    'apellido': empleado.apellido
                },
                'es_entrada': registro.es_entrada,
                'desfase': registro.desfase.strftime("%H:%M:%S"),
            }
            registros_data.append(registro_data)
        return jsonify(registros_data)
    except:
        return jsonify({"error": "No se pudo obtener los registros"}), 400

# OK


@app.route('/api/v1/registros/<int:id>', methods=['GET'])
def obtener_registro(id):
    try:
        registro = Registro.query.get(id)
        registro_data = {
            'id': registro.id,
            'horario': registro.horario,
            'empleado_id': registro.empleado_id,
            'es_entrada': registro.es_entrada,
            'desfase': registro.desfase,
        }
        return jsonify(registro_data)
    except:
        return jsonify({"error": "Registro Inexistente"}), 400

# OK


@app.route('/api/v1/registros', methods=['POST'])
def agregar_registro():
    try:
        horario = request.json.get("horario")
        empleado_id = request.json.get("empleado_id")

        empleado = db.session.query(Empleado).get(empleado_id)

        if empleado is None:
            return jsonify({'message': "Employee not found"}), 404

        fecha = datetime.fromisoformat(horario)

        hora_fichaje = fecha.time()
#pendiente de correccion de error
        hora_entrada = datetime(empleado.horario_entrada).time()
        hora_salida = datetime(empleado.horario_salida).time()

        diferencia_entrada = hora_fichaje - hora_entrada
        diferencia_salida = hora_fichaje - hora_salida

        es_entrada = False
        if diferencia_entrada < diferencia_salida:
            es_entrada = True

        valor_absoluto_diferencia = diferencia_salida
        if es_entrada:
            valor_absoluto_diferencia = diferencia_entrada

        desfase = datetime.fromtimestamp(
            valor_absoluto_diferencia)
        desfase = desfase.strftime("%H:%M:%S")

        nuevo_registro = Registro(
            horario=horario, empleado_id=empleado_id, es_entrada=es_entrada, desfase=desfase)

        db.session.add(nuevo_registro)
        db.session.commit()

        return jsonify({"message": "Agregado Exitosamente"}), 201
    except Exception as error:
        print(error)
        return jsonify({'message': "Hubo un error"}), 400
# Falta probar


@app.route('/api/v1/registros/<int:id>', methods=['DELETE'])
def eliminar_registro(id):
    try:
        registro = Registro.query.get(id)
        db.session.delete(registro)
        db.session.commit()
        return jsonify({"sucess": "Borrado Exitosamente"}, 201)
    except:
        return jsonify({"message": "Registro desconocido"}, 400)

# Falta probar


@app.route('/api/v1/registros/<int:id>', methods=['PUT'])
def modificar_registro(id):
    try:
        registro = Registro.query.get(id)

        registro.horario = request.json.get("horario")
        registro.empleado_id = request.json.get("empleado_id")
        registro.es_entrada = request.json.get("es_entrada")
        registro.desfase = request.json.get("desfase")
        db.session.commit()
        return jsonify({"message": "Actualizado Exitosamente"}, 201)
    except:
        return jsonify({"message": "Registro desconocido"}, 400)

# Endpoints Empleados ################################################

# OK


@app.route('/api/v1/empleados/<int:id>', methods=['GET'])
def obtener_empleado(id):
    try:
        empleado = Empleado.query.get(id)

        if not empleado:
            return jsonify({'message': f'No existe el empleado con id:{id}'}), 400

        empleado_data = {
            'id': empleado.id,
            'nombre': empleado.nombre,
            'apellido': empleado.apellido,
            'dni': empleado.dni,
            'horario_entrada': empleado.horario_entrada.strftime('%H:%M:%S'),
            'horario_salida': empleado.horario_salida.strftime('%H:%M:%S'),
        }

        return jsonify(empleado_data), 200
    except:
        return jsonify({"error": "No se pudo obtener el empleado"}), 400

# OK


@app.route('/api/v1/empleados', methods=['GET'])
def obtener_empleados():
    try:
        maximo_registros = request.args.get('maximo')

        if not maximo_registros:
            maximo_registros = MAX_REGISTROS

        empleados = Empleado.query.limit(maximo_registros).all()
        lista_empleados = []

        for empleado in empleados:
            datos_empleado = {
                'id': empleado.id,
                'nombre': empleado.nombre,
                'apellido': empleado.apellido,
                'dni': empleado.dni,
                'horario_entrada': empleado.horario_entrada.strftime('%H:%M:%S'),
                'horario_salida': empleado.horario_salida.strftime('%H:%M:%S')
            }
            lista_empleados.append(datos_empleado)

        return jsonify(lista_empleados), 200

    except:
        return jsonify({'message': 'Error interno del servidor'}), 500


#OK


@app.route('/api/v1/empleados', methods=['POST'])
def agregar_empleado():

    nombre = request.json.get("nombre")
    apellido = request.json.get("apellido")
    dni = request.json.get("dni")
    horario_entrada = request.json.get("horario_entrada")
    horario_salida = request.json.get("horario_salida")

    if not (nombre and apellido and dni and horario_entrada and horario_entrada):
        return jsonify({'message': 'faltan parametros en el body'}), 400
    
    #por si el emplado ya existe
    empleado = db.session.query(Empleado.id).filter(Empleado.dni==dni).first()
    
    if empleado != None:
        return jsonify({'message': 'empleado ya existente'}), 400

    nuevo_empleado = Empleado(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        horario_entrada=horario_entrada,
        horario_salida=horario_salida
        )
    db.session.add(nuevo_empleado)
    db.session.commit()

    ##para que devuelva su id de tabla
   
    empleado = db.session.query(Empleado.id).filter(Empleado.dni==dni).first()

    return jsonify({"sucess": f"Agregado DNI:{dni} ", "id":empleado.id}), 200 #debe ir sucess para que no aparesca un aviso

# OK


@app.route('/api/v1/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado(id):
    try:
        empleado = Empleado.query.get(id)
        db.session.delete(empleado)
        db.session.commit()
        return jsonify({"message": "Borrado Exitosamente"}), 201
    except:
        return jsonify({"message": "Empleado desconocido"}), 404

# Falta probar


@app.route('/api/v1/empleados/<int:id>', methods=['PUT'])
def actualizar_empleado(id):
    try:
        empleado = db.session.query(Empleado).get(id)

        if not empleado:
            return jsonify({'message': 'No existe el empleado'}), 404

        nombre = request.json.get("nombre")
        apellido = request.json.get("apellido")
        dni = request.json.get('dni')
        horario_entrada = request.json.get('horario_entrada')
        horario_salida = request.json.get('horario_salida')
        if nombre:
            empleado.nombre = nombre

        if apellido:
            empleado.apellido = apellido

        if dni:
            empleado.dni = dni

        if horario_entrada:
            empleado.horario_entrada = horario_entrada

        if horario_salida:
            empleado.horario_salida = horario_salida
        db.session.commit() 
        return jsonify({"sucess": "Actualizado Exitosamente", "id":id}), 201
    except:
        return jsonify({"message": "Ha ocurrido un error"}), 400


db.init_app(app)

if __name__ == '__main__': 
    
    with app.app_context():
        # db.drop_all()
        db.create_all()
    app.run(debug=True, port=port)
