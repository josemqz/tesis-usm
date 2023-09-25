from sqlalchemy.sql import func
from flask import jsonify
from datetime import datetime
from src import db # importa db de __init__

"""
svg_id: id de figura correspondiente a la sala en mapa svg
nombre: nombre de sala (ej: A-001, Patio de las Lámparas, Arquitectura...)
ocupacion_max: ocupación máxima recomendada de sala
"""
class Sala(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    svg_id = db.Column(db.String(50), nullable=False)
    nombre = db.Column(db.String(50), nullable=False)
    ocupacion_max = db.Column(db.Integer, nullable=False)
    ocupaciones = db.relationship('Ocupacion', lazy='dynamic')
    # lazy=dinamic: retorna un objeto al que se puede aplicar distintos filtros, como all() y filter_by()
    
    def __init__(self, svg_id: int, nombre: str, ocupacion_max: int):
        self.svg_id = svg_id
        self.nombre = nombre
        self.ocupacion_max = ocupacion_max
    
    def __repr__(self):
        return '<Sala %r>' % self.nombre
    
    @staticmethod
    def crear(svg_id, nombre, ocupacion_max):
        nueva_sala = Sala(svg_id, nombre, ocupacion_max)
        db.session.add(nueva_sala)
        db.session.commit()

    @staticmethod
    def get_salas():
        salas = Sala.query.order_by('id').all()
        return jsonify([{'id': i.id, 
                         'svg_id': i.svg_id, 
                         'nombre': i.nombre, 
                         'ocupacion_max': i.ocupacion_max}
                        for i in salas])
    
    @staticmethod
    def get_sala_by_id(id):
        sala = Sala.query.filter_by(id=id).first()
        return jsonify({'id':sala.id, 
                        'svg_id': sala.svg_id, 
                        'nombre': sala.nombre, 
                        'ocupacion_max': sala.ocupacion_max})
    
    @staticmethod
    def get_sala_by_nombre(nombre):
        sala = Sala.query.filter_by(nombre=nombre).first()
        return jsonify({'id':sala.id, 
                        'svg_id': sala.svg_id, 
                        'nombre': sala.nombre, 
                        'ocupacion_max': sala.ocupacion_max})
        


"""
sala_id: id de tabla Sala asociado a la ocupación 
ocupacion: cantidad de personas estimadas por Portenta en la sala
timestamp: fecha y hora de detección
"""
class Ocupacion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sala_id = db.Column(db.Integer, db.ForeignKey(Sala.id))
    ocupacion_actual = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime(timezone=True),
                           server_default=func.now())
    
    def __init__(self, sala_id: int, ocupacion_actual: int, timestamp: datetime):
        self.sala_id = sala_id
        self.ocupacion_actual = ocupacion_actual
        # FIX: está en otro formato, que en verdad no es terrible, pero está en GMT (Greenwich)
        if self.timestamp != None:
            self.timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S.%fZ')

    def __repr__(self):
        return '<Ocupacion: %r [Sala %r] (%r)>' % (self.ocupacion_actual, self.sala_id, self.timestamp)

    @staticmethod
    def crear(sala_id, ocupacion_actual, timestamp):
        nueva_ocupacion = Ocupacion(sala_id, ocupacion_actual, timestamp)
        db.session.add(nueva_ocupacion)
        db.session.commit()

    @staticmethod
    def get_ocupaciones():
        ocupaciones = Ocupacion.query.order_by('id').all()
        return jsonify([{'id': oc.id, 
                 'sala_id': oc.sala_id, 
                 'ocupacion_actual': oc.ocupacion_actual,
                 'timestamp': oc.timestamp}
                for oc in ocupaciones])
    
    """
    # retornar lista con última ocupación de cada sala que cuente con una
    @staticmethod
    def get_ultimas_ocupaciones():

        # en este caso, se ordena por id de forma decreciente, con tal de obtener el último registro
        ocupaciones = Ocupacion.order_by(-Ocupacion.id).first()

        return jsonify([{'id': oc.id, 
                        'sala_id': oc.sala_id, 
                        'ocupacion_actual': oc.ocupacion_actual,
                        'timestamp': oc.timestamp}
                        for oc in ocupaciones])
    """
    
    @staticmethod
    def get_ocupaciones_by_sala_id(sala_id):
        # se obtiene el objeto de la sala buscada
        sala = Sala.query.filter_by(id=sala_id).first()
        # se obtienen sus ocupaciones
        ocupaciones = sala.ocupaciones.all()

        return jsonify([{'id': oc.id, 
                        'sala_id': oc.sala_id, 
                        'ocupacion_actual': oc.ocupacion_actual,
                        'timestamp': oc.timestamp}
                        for oc in ocupaciones])

    @staticmethod
    def get_ultima_ocupacion_by_sala_id(sala_id):

        sala = Sala.query.filter_by(id=sala_id).first()
        # en este caso, se ordena por id de forma decreciente, con tal de obtener el último registro
        ocupacion = sala.ocupaciones.order_by(-Ocupacion.id).first()

        return jsonify({'id': ocupacion.id, 
                        'sala_id': ocupacion.sala_id, 
                        'ocupacion_actual': ocupacion.ocupacion_actual,
                        'timestamp': ocupacion.timestamp})

    @staticmethod
    def delete_ocupacion_by_id(id):
        Ocupacion.query.filter_by(id=id).delete()
        db.session.commit()