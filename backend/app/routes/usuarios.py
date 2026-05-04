from fastapi import APIRouter
from app.database import get_connection
import random

router = APIRouter()

# ---------------- LOGIN ----------------
@router.post("/login")
def login(data: dict):

    if data["usuario"] == "admin" and data["password"] == "1234":
        return {"status": "admin"}

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=%s AND password=%s",
        (data["usuario"], data["password"])
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return {
            "status": "maestro",
            "nombre": user["nombre"],
            "tipo": user["tipo"],
            "materia": user["materia"],
            "grupo": user["grupo"],
            "horas": user["horas"]
        }

    return {"status": "error"}


# ---------------- CREAR MAESTRO ----------------
@router.post("/crear_maestro")
def crear_maestro(data: dict):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO usuarios
        (usuario, password, nombre, tipo, materia, grupo, horas)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["usuario"],
        data["password"],
        data["nombre"],
        data["tipo"],
        data["materia"],
        data["grupo"],
        data["horas"]
    ))

    conn.commit()
    conn.close()

    return {"status": "ok"}


# ---------------- GENERAR HORARIO ----------------
@router.get("/generar_horario")
def generar_horario():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM usuarios")
    maestros = cursor.fetchall()

    conn.close()

    dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
    horas_dia = ["7-8", "8-9", "9-10", "10-11", "11-12", "12-1", "1-2"]

    horario = []
    ocupados = {}

    for maestro in maestros:

        horas_restantes = maestro["horas"]
        intentos = 0

        while horas_restantes > 0 and intentos < 200:

            intentos += 1

            dia = random.choice(dias)
            hora = random.choice(horas_dia)

            clave = f"{dia}-{hora}-{maestro['grupo']}"

            # ❌ evitar choque de grupo en misma hora
            if clave in ocupados:
                continue

            # ❌ evitar que el mismo maestro tenga 2 clases al mismo tiempo
            conflicto_maestro = any(
                h["dia"] == dia and
                h["hora"] == hora and
                h["maestro"] == maestro["nombre"]
                for h in horario
            )

            if conflicto_maestro:
                continue

            # ❌ evitar repetir materia del mismo maestro en el mismo día
            ya_tiene = any(
                h["dia"] == dia and
                h["maestro"] == maestro["nombre"]
                for h in horario
            )

            if ya_tiene:
                continue

            # ✅ asignar horario
            ocupados[clave] = True

            horario.append({
                "dia": dia,
                "hora": hora,
                "grupo": maestro["grupo"],
                "materia": maestro["materia"],
                "maestro": maestro["nombre"]
            })

            horas_restantes -= 1

        # ⚠️ aviso si no se pudieron asignar todas las horas
        if horas_restantes > 0:
            print(f"No se pudieron asignar todas las horas a {maestro['nombre']}")

    return horario