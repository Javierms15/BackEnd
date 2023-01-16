import math

from fastapi import APIRouter, HTTPException
from mongoengine import ValidationError, OperationError, DoesNotExist
from pydantic import BaseModel
from datetime import datetime

from modelos.Coordenadas import Coordenadas
from enumerados.Servicios import Servicios
from modelos.Parada import Parada

paradaRouter = APIRouter()

def append_parada(lista: list, parada: Parada):
    lista.append({"codLinea": parada.codLinea,
                  "nombreLinea": parada.nombreLinea,
                  "sentido": parada.sentido,
                  "orden": parada.orden,
                  "codParada": parada.codParada,
                  "nombreParada": parada.nombreParada,
                  "direccion": parada.direccion,
                  "lon": parada.lon,
                  "lat": parada.lat})
    return lista


def intersection(lista1, lista2):
    listaResul = [value for value in lista1 if value in lista2]
    return listaResul


@paradaRouter.get("/")
def filtrar(linea: int | None = None, sentido: int | None = None):
    try:
        lista = list()
        listaLin = list()
        listaSen = list()

        if (linea is not None and linea < 1) or (sentido is not None and (sentido < 1 or sentido > 2)):
            raise HTTPException(status_code=400)

        if linea is not None:
            for parada in Parada.objects(linea__=linea):
                listaLin = append_parada(listaLin, parada)
            if len(listaLin) == 0:
                return listaLin
            lista = listaLin
            print(len(lista))

        if sentido is not None:
            for parada in Parada.objects(sentido__=sentido):
                listaSen = append_parada(listaSen, parada)
            if len(listaSen) == 0:
                return listaSen
            if len(lista) == 0 and len(listaSen) == 0:
                lista = listaLin
            else:
                lista = intersection(lista, listaLin)
            print(len(lista))

        if len(lista) == 0 and linea is None and sentido is None:
            for parada in Parada.objects:
                lista = append_parada(lista, parada)

        return lista
    except OperationError as E:
        print(E)
        raise HTTPException(status_code=500)

@paradaRouter.get("/{nombreParada}")
def filtro_nombreParada(nombreParada):
    try:
        lista = list()
        parada = Parada.objects(nombreParada__contains=nombreParada)
        return append_parada(lista, parada)
    except OperationError as E:
        print(E)
        raise HTTPException(status_code=500)


def haversine(lat1, lon1, lat2, lon2):
    dLat = (lat2 - lat1) * math.pi / 180.0
    dLon = (lon2 - lon1) * math.pi / 180.0

    lat1 = lat1 * math.pi / 180.0
    lat2 = lat2 * math.pi / 180.0

    a = (pow(math.sin(dLat / 2), 2) +
         pow(math.sin(dLon / 2), 2) *
         math.cos(lat1) * math.cos(lat2))
    rad = 6371
    c = 2 * math.asin(math.sqrt(a))
    return rad * c


@paradaRouter.get("/coordenadas/{latitud}/{longitud}")
def paradas_cercanas(longitud: float, latitud: float):
    try:
        lista = list()

        if -90 > latitud or latitud > 90 or -180 > longitud or longitud > 180:
            raise HTTPException(status_code=400)

        for parada in Parada.objects:
            if parada.lat < latitud+0.003 and parada.lat > latitud-0.003 and parada.lon < longitud+0.003 and parada.lon > longitud-0.003:
                lista = append_parada(lista, parada)

        return lista
    except OperationError as E:
        print(E)
        raise HTTPException(status_code=500)

@paradaRouter.get("/{latitud}/{longitud}/")
def viviendas_multifiltro(longitud: float, latitud: float, coor: bool, sentido: int | None = None, linea: float | None = None, nombreParada: str | None = None):
    if not coor:
        if nombreParada == "":
            return filtrar(linea, sentido)
        else:
            return intersection(filtrar(linea, sentido), filtro_nombreParada(nombreParada))
    else:
        if linea != 0 and nombreParada == "":
            return intersection(filtrar(linea, sentido), paradas_cercanas(longitud, latitud));
        elif linea != 0 and nombreParada != "":
            return intersection(intersection(filtrar(linea, sentido), paradas_cercanas(longitud, latitud)), filtro_nombreParada(nombreParada))
        elif linea == 0 and nombreParada == "":
            return paradas_cercanas(longitud, latitud)
        else:
            return intersection(paradas_cercanas(longitud, latitud), filtro_nombreParada(nombreParada))