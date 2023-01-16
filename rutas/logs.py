from datetime import datetime
from fastapi import APIRouter, HTTPException
from mongoengine import ValidationError, OperationError, DoesNotExist
from pydantic import BaseModel
from typing import Union

from modelos.Log import Log
from modelos.Parada import Parada


class CuerpoCreacionLog(BaseModel):
    timestamp: datetime
    usuario: str
    caducidad: datetime
    token: str

logRouter = APIRouter()

@logRouter.post("/")
def crearLog(log: CuerpoCreacionLog):
    try:
        nuevoLog = Log()
        nuevoLog.timestamp = datetime.now()
        nuevoLog.usuario = CuerpoCreacionLog.usuario
        nuevoLog.token = CuerpoCreacionLog.token

    except OperationError as E:
        print(E)


