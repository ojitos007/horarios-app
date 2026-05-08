from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# IMPORTAR RUTAS
from app.routes import usuarios
from app.routes import horarios

# CREAR APP
app = FastAPI(
    title="Sistema Inteligente de Horarios",
    description="API para gestión académica y generación automática de horarios escolares",
    version="1.0.0"
)

# CONFIGURACIÓN CORS
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://18.220.231.121",
        "http://18.220.231.121:8080",
        "http://localhost",
        "http://localhost:8080",
        "http://127.0.0.1",
        "http://127.0.0.1:8080"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

# REGISTRAR RUTAS
app.include_router(usuarios.router)
app.include_router(horarios.router)

# RUTA PRINCIPAL
@app.get("/")
def inicio():

    return {
        "status": "ok",
        "mensaje": "API del Sistema de Horarios funcionando correctamente",
        "documentacion": "/docs"
    }

# HEALTH CHECK
@app.get("/health")
def health():

    return {
        "server": "activo",
        "api": "online"
    }