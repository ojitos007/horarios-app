from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    nombre: Optional[str] = None
    correo: str
    password: str
    tipo: Optional[str] = None
    matricula: Optional[str] = None
    carrera: Optional[str] = None
    semestre: Optional[int] = None
