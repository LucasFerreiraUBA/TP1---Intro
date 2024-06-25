from flask import Blueprint, jsonify, request
from models import Registro, Empleado, db
from datetime import time, datetime, timedelta

registros = Blueprint('registros', __name__)

# Constantes
MAX_REGISTROS = 100


# OK
@registros.route('/api/v1/registros', methods=['GET'])
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
                    'apellido': empleado.apellido,
                    'horario_entrada': empleado.horario_entrada.strftime('%H:%M:%S'),
                    'horario_salida': empleado.horario_salida.strftime('%H:%M:%S')
                },
                'es_entrada': registro.es_entrada,
                'desfase': registro.desfase.seconds // 60,
                'diferencia' : {
                    'horas' : registro.desfase.seconds // 3600,
                    'minutos': (registro.desfase.seconds % 3600) // 60,
                    'segundos' : (registro.desfase.seconds % 60)
                }
            }
            registros_data.append(registro_data)
        return jsonify(registros_data)
    except:
        return jsonify({"error": "No se pudo obtener los registros"}), 400

# OK
@registros.route('/api/v1/registros/<int:id>', methods=['GET'])
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
@registros.route('/api/v1/registros', methods=['POST'])
def agregar_registro():
    try:
        horario = request.json.get("horario")
        empleado_id = int(request.json.get("empleado_id"))

        empleado = db.session.query(Empleado).get(empleado_id)

        if empleado is None:
            return jsonify({'message': "Employee not found"}), 404

        hora_fichaje = datetime.fromisoformat(horario)

        hora_entrada = datetime.combine(hora_fichaje.date(), empleado.horario_entrada)
        hora_salida = datetime.combine(hora_fichaje.date(), empleado.horario_salida)

        print('hora entrada', hora_entrada)
        print('hora_salida', hora_salida)
            
        diferencia_entrada = abs(hora_fichaje - hora_entrada)
        diferencia_salida = abs(hora_fichaje - hora_salida)

        print('fichaje', hora_fichaje)

        print('dif entrada', diferencia_entrada)
        print('dif salida', diferencia_salida)

        es_entrada = diferencia_entrada < diferencia_salida

        diferencia = diferencia_salida
        if(es_entrada):
            diferencia = diferencia_entrada

        registro = db.session.query(Registro).filter(Registro.horario >= hora_fichaje.date(), Registro.horario < hora_fichaje.date() + timedelta(days=1), Registro.es_entrada == es_entrada,Registro.empleado_id == empleado_id).first()

        if registro == None:
            nuevo_registro = Registro(
            horario=hora_fichaje, empleado_id=empleado_id, es_entrada=es_entrada, desfase=diferencia)
            db.session.add(nuevo_registro)
        else:
            registro.horario = hora_fichaje,
            registro.desfase = diferencia

        db.session.commit()

        if registro == None:
            return jsonify({"message": "Agregado Exitosamente"}), 201
        else:
            return jsonify({"message": "Se actualizo la hora de entrada"}), 201
    
    except Exception as error:
        print(error)
        return jsonify({'message': "Hubo un error"}), 400

# Falta probar
@registros.route('/api/v1/registros/<int:id>', methods=['DELETE'])
def eliminar_registro(id):
    try:
        registro = Registro.query.get(id)
        db.session.delete(registro)
        db.session.commit()
        return jsonify({"sucess": "Borrado Exitosamente"}, 201)
    except:
        return jsonify({"message": "Registro desconocido"}, 400)

# Falta probar
@registros.route('/api/v1/registros/<int:id>', methods=['PUT'])
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
