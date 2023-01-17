
from mongoengine import *
from enumerados.Servicios import Servicios
from modelos.Coordenadas import Coordenadas
import requests
import datetime
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from pymongo import MongoClient


class Log(Document):
    timestamp = DateTimeField(required=True)
    usuario = StringField(required=True)
    caducidad = DateTimeField(required=True)
    token = StringField(required=True)

    # anfitrion = StringField(required=True)
    # titulo = StringField(required=True)
    # descripcion = StringField(max_length=500)
    # imagenes = ListField(URLField())
    # precio_noche = FloatField(min_value=0, required=True)
    # capacidad = IntField(min_value=1, required=True)
    # direccion = StringField(max_length=500, required=True)
    # reservas = ListField(ReferenceField(Reserva, reverse_delete_rule=PULL))
    # servicios = ListField(EnumField(Servicios))
    # coordenadas = EmbeddedDocumentField(Coordenadas, required=True)
    # disponible_reserva = BooleanField(required=True)