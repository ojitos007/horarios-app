from fastapi import APIRouter
from app.database import get_connection

router = APIRouter()

# ---------------- LOGIN ----------------
@router.post("/login")
def login(data: dict):

    # 🔥 ADMIN FIJO
    if data["usuario"] == "admin" and data["password"] == "1234":

        return {
            "status": "admin"
        }

    conn = get_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM usuarios
        WHERE usuario=%s
        AND password=%s
    """, (
        data["usuario"],
        data["password"]
    ))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    # 🔥 SI EXISTE
    if user:

        return {
            "status": "maestro",
            "nombre": user["nombre"],
            "tipo": user["tipo"],
            "materia": user["materia"],
            "grupo": user["grupo"],
            "horas": user["horas"]
        }

    # ❌ LOGIN INCORRECTO
    return {
        "status": "error"
    }


# ---------------- CREAR MAESTRO ----------------
@router.post("/crear_maestro")
def crear_maestro(data: dict):

    conn = get_connection()

    cursor = conn.cursor()

    # 🔥 INSERTAR MAESTRO
    cursor.execute("""
        INSERT INTO usuarios (
            usuario,
            password,
            nombre,
            rol,
            tipo,
            materia,
            grupo,
            horas
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["usuario"],
        data["password"],
        data["nombre"],
        "maestro",
        data["tipo"],
        data["materia"],
        data["grupo"],
        data["horas"]
    ))

    conn.commit()

    # 🔥 REGENERAR HORARIOS AUTOMÁTICAMENTE
    from app.routes.horarios import generar_horarios

    generar_horarios()

    cursor.close()
    conn.close()

    return {
        "status": "Maestro creado y horarios actualizados"
    }