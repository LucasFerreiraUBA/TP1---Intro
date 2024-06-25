from models import db, Empleado, Registro
from flask import  jsonify, request, Blueprint

# Constantes
MAX_REGISTROS = 100

empleados = Blueprint('empleados', __name__)


@empleados.route('/api/v1/empleados/<int:id>', methods=['GET'])
def obtener_empleado(id): #OK
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

@empleados.route('/api/v1/empleados', methods=['GET'])
def obtener_empleados(): #OK
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


@empleados.route('/api/v1/empleados', methods=['POST'])
def agregar_empleado():#OK

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

@empleados.route('/api/v1/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleado(id): #OK
    try:
        empleado = Empleado.query.get(id)
        db.session.delete(empleado)
        db.session.commit()
        return jsonify({"message": "Borrado Exitosamente"}), 201
    except:
        return jsonify({"message": "Empleado desconocido"}), 404


@empleados.route('/api/v1/empleados/<int:id>', methods=['PUT'])
def actualizar_empleado(id): #FALTA PROBAR
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

