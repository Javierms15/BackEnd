from mongoengine import *


class Coordenadas(EmbeddedDocument):
    latitud = FloatField(required=True)
    longitud = FloatField(required=True)
