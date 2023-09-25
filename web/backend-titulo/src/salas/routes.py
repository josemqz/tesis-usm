from flask import jsonify
from flask import current_app as app
from src.models.models import Sala

# obtener información de la sala, incluyendo id, nombre, ocupación máxima 
@app.route('/salas', methods=['GET'])
def get_salas():
    return Sala.get_salas()

@app.route('/sala/<int:id>', methods=['GET'])
def get_sala_by_id(id):
    return Sala.get_sala_by_id(id)    
