from datetime import datetime
from mongoengine import *


class Parada(Document):
    # usuario = StringField(required=True)
    # vivienda = StringField(required=True)
    # plazas_reservadas = IntField(min_value=1, required=True)
    # fecha_reserva = DateTimeField(default=datetime.utcnow, required=True)
    # inicio_estancia = DateTimeField(required=True)
    # fin_estancia = DateTimeField(required=True)

    codLinea = IntField(required=True)
    nombreLinea = StringField(required=True)
    sentido = IntField(required=True)
    orden = IntField()
    codParada = IntField()
    nombreParada = StringField(required=True)
    direccion = StringField()
    lon = FloatField(required=True)
    lat = FloatField(required=True)

