from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# IMPORTAR RUTAS
from app.routes import usuarios
from app.routes import horarios

app = FastAPI()

# 🔥 CORS (IMPORTANTE)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔥 REGISTRAR RUTAS
app.include_router(usuarios.router)
app.include_router(horarios.router)