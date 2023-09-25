from flask import jsonify, request
from flask import current_app as app
from src.models.models import Ocupacion

# Obtener info de ocupaciones de todas las salas
@app.route('/ocupaciones', methods=['GET'])
def get_ocupaciones():
    return Ocupacion.get_ocupaciones() 

"""
# Obtener info de últimas ocupaciones de todas las salas
@app.route('/ult_ocupaciones', methods=['GET'])
def get_ultimas_ocupaciones():
    return Ocupacion.get_ultimas_ocupaciones() 
"""

# Obtener info de ocupaciones de una sala específica
@app.route('/ocupaciones/<int:sala_id>', methods=['GET'])
def get_ocupaciones_by_sala_id(sala_id):
    return Ocupacion.get_ocupaciones_by_sala_id(sala_id)

# Obtener info de última ocupación de una sala específica
@app.route('/ult_ocupacion/<int:sala_id>', methods=['GET'])
def get_ultima_ocupacion_by_sala_id(sala_id):
    return Ocupacion.get_ultima_ocupacion_by_sala_id(sala_id)

# Agregar ocupación actual de una sala específica
@app.route('/ocupacion', methods=['POST'])
def add_ocupacion():

    sala_id = request.args.get('sala_id')
    ocupacion_actual = request.args.get('ocupacion_actual')
    timestamp = request.args.get('timestamp')

    # try:
    Ocupacion.crear(sala_id, ocupacion_actual, timestamp)
    return "OK"
        # return "OK"
    # except:
        # print("Error al añadir dato a tabla Ocupaciones")
        # return "Database Error"

@app.route('/ocupacion/<int:id>', methods=['DELETE'])
def delete_ocupacion(id):
    # implementar mensajes
    Ocupacion.delete_ocupacion_by_id(id)
    return "OK"