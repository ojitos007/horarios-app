from pydantic import BaseModel
from typing import Optional

# =========================
# LOGIN
# =========================
class Login(BaseModel):

    usuario: str
    password: str


# =========================
# USUARIO / MAESTRO
# =========================
class Usuario(BaseModel):

    usuario: str
    password: str

    nombre: str

    rol: Optional[str] = "maestro"

    tipo: str

    materia: str

    grupo: str

    horas: int


# =========================
# HORARIO
# =========================
class Horario(BaseModel):

    dia: str

    hora: str

    grupo: str

    materia: str

    maestro: str