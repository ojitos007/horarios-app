from fastapi import APIRouter
from app.database import get_connection
import random

router = APIRouter()

# 📅 Datos base
dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]
horas = ["1-2", "3-4", "5-6", "7-8", "9-10", "11-12"]

# 🔥 GENERAR HORARIOS
@router.get("/generar_horarios")
def generar_horarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 🧹 Limpiar horarios anteriores
    cursor.execute("DELETE FROM horarios")

    # 👨‍🏫 Obtener maestros
    cursor.execute("SELECT * FROM usuarios WHERE rol='maestro'")
    maestros = cursor.fetchall()

    for maestro in maestros:
        horas_asignadas = int(maestro["horas"]) if maestro["horas"] else 0

        usados = set()

        for _ in range(horas_asignadas):
            intentos = 0

            while True:
                dia = random.choice(dias)
                hora = random.choice(horas)

                clave = f"{dia}-{hora}"

                # 🔒 Evitar repetir mismo horario
                if clave not in usados:
                    usados.add(clave)
                    break

                intentos += 1
                if intentos > 20:
                    break

            cursor.execute("""
                INSERT INTO horarios (dia, hora, grupo, materia, maestro)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                dia,
                hora,
                maestro["grupo"],
                maestro["materia"],
                maestro["nombre"]
            ))

    conn.commit()
    conn.close()

    return {"status": "horarios generados correctamente"}


# 🔥 OBTENER HORARIO POR MAESTRO
@router.get("/horario_maestro")
def horario_maestro(nombre: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT * FROM horarios WHERE maestro = %s
    """, (nombre,))

    datos = cursor.fetchall()

    conn.close()

    return datos


# 🔥 NUEVO: VER TODOS LOS HORARIOS (ADMIN)
@router.get("/todos_horarios")
def todos_horarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM horarios")
    datos = cursor.fetchall()

    conn.close()

    return datos


# 🔥 GUARDAR CAMBIOS (drag & drop)
@router.post("/guardar_horario")
def guardar_horario(data: list):
    conn = get_connection()
    cursor = conn.cursor()

    # 🧹 Limpiar tabla
    cursor.execute("DELETE FROM horarios")

    # 🔁 Insertar nuevo horario
    for item in data:
        cursor.execute("""
            INSERT INTO horarios (dia, hora, grupo, materia, maestro)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            item["dia"],
            item["hora"],
            item["grupo"],
            item["materia"],
            item["maestro"]
        ))

    conn.commit()
    conn.close()

    return {"status": "horario guardado"}