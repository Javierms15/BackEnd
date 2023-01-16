from fastapi import FastAPI
from mongoengine import *
import firebase_admin
from fastapi.middleware.cors import CORSMiddleware
from rutas.logs import logRouter
from rutas.paradas import paradaRouter
from fastapi import FastAPI, Request, Response, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, auth

app = FastAPI()

public_routes = ['/', '/docs', '/openapi.json']

origins = [
    'https://editor.swagger.io', "http://localhost:5173", "http://127.0.0.1:5173", "https://examen-web.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.middleware('http')
async def check_token(request: Request, call_next):
    if request.url.path in public_routes or request.method == 'OPTIONS':
        return await call_next(request)
    if "authorization" in request.headers and request.headers["authorization"].startswith("Bearer "):
        token = request.headers["authorization"][len("Bearer "):]
        try:
            auth.verify_id_token(token)
        except ValueError as e:
            return Response(status_code=status.HTTP_400_BAD_REQUEST, content="Se ha enviado un token incorrecto", headers={"WWW-Authenticate": "Bearer"})
        except auth.InvalidIdTokenError as e:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="No se ha enviado un token de Firebase", headers={"WWW-Authenticate": "Bearer"})
        except auth.ExpiredIdTokenError:
            return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="El token enviado a expirado", headers={"WWW-Authenticate": "Bearer"})
        except auth.CertificateFetchError:
            return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content="No se ha podido obtener los certificados")
        return await call_next(request)
    else:
        return Response(status_code=status.HTTP_401_UNAUTHORIZED, content="No se ha enviado ningun token de autenticacion", headers={"WWW-Authenticate": "Bearer"})


app.include_router(
    logRouter,
    prefix="/log",
    tags=["logs"]
)

app.include_router(
    paradaRouter,
    prefix="/parada",
    tags=["paradas"]
)


@app.on_event("startup")
async def create_db_client():
    connect(host="mongodb+srv://javierms15:javierms20@cluster0.uqz7xkn.mongodb.net/test")
    app.firebase = firebase_admin.initialize_app(credentials.Certificate(
        'ingwebpython-firebase-adminsdk-ssvgn-640e7a8989.json'))
    # app.datos = json.load(open('./.json', 'r'))


@app.on_event("shutdown")
async def shutdown_db_client():
    disconnect()
