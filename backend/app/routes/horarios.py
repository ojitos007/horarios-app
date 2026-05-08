from fastapi import APIRouter
from app.database import get_connection
import random

router = APIRouter()

# 📅 Datos base
dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"]

horas = [
    "7-8",
    "8-9",
    "9-10",
    "10-11",
    "11-12",
    "12-1",
    "1-2"
]

# 🔥 GENERAR HORARIOS
@router.get("/generar_horarios")
def generar_horarios():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # 🧹 Limpiar horarios anteriores
    cursor.execute("DELETE FROM horarios")

    # 👨‍🏫 Obtener maestros
    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE rol='maestro'
    """)

    maestros = cursor.fetchall()

    horarios_generados = []

    usados_global = set()

    for maestro in maestros:

        horas_asignadas = int(maestro["horas"]) if maestro["horas"] else 1

        contador = 0

        while contador < horas_asignadas:

            dia = random.choice(dias)
            hora = random.choice(horas)

            # 🔒 Evitar conflictos
            clave = f"{dia}-{hora}-{maestro['grupo']}"

            if clave in usados_global:
                continue

            usados_global.add(clave)

            cursor.execute("""
                INSERT INTO horarios (
                    dia,
                    hora,
                    grupo,
                    materia,
                    maestro
                )
                VALUES (%s,%s,%s,%s,%s)
            """, (
                dia,
                hora,
                maestro["grupo"],
                maestro["materia"],
                maestro["nombre"]
            ))

            horarios_generados.append({
                "dia": dia,
                "hora": hora,
                "grupo": maestro["grupo"],
                "materia": maestro["materia"],
                "maestro": maestro["nombre"]
            })

            contador += 1

    conn.commit()

    cursor.close()
    conn.close()

    return horarios_generados


# 🔥 OBTENER HORARIO POR MAESTRO
@router.get("/horario_maestro")
def horario_maestro(nombre: str):

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM horarios
        WHERE maestro = %s
    """, (nombre,))

    datos = cursor.fetchall()

    cursor.close()
    conn.close()

    return datos


# 🔥 VER TODOS LOS HORARIOS
@router.get("/todos_horarios")
def todos_horarios():

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM horarios
    """)

    datos = cursor.fetchall()

    cursor.close()
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
            INSERT INTO horarios (
                dia,
                hora,
                grupo,
                materia,
                maestro
            )
            VALUES (%s,%s,%s,%s,%s)
        """, (
            item["dia"],
            item["hora"],
            item["grupo"],
            item["materia"],
            item["maestro"]
        ))

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "status": "horario guardado"
    }