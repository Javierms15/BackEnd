from datetime import datetime
from mongoengine import *


class Parking(Document):
    # usuario = StringField(required=True)
    # vivienda = StringField(required=True)
    # plazas_reservadas = IntField(min_value=1, required=True)
    # fecha_reserva = DateTimeField(default=datetime.utcnow, required=True)
    # inicio_estancia = DateTimeField(required=True)
    # fin_estancia = DateTimeField(required=True)

    poiID = IntField(required=True)
    nombre = StringField(required=True)
    direccion = StringField(required=True)
    latitud = FloatField()(required=True)
    longitud = FloatField()(required=True)
    capacidad = IntField(required=True)
    libres = IntField()(required=True)
    correo = StringField(required=True)