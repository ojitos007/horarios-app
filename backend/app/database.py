import mysql.connector
from mysql.connector import Error

# CONFIGURACIÓN BASE DE DATOS
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "1234",
    "database": "horarios",
    "port": 3306
}

# FUNCIÓN DE CONEXIÓN
def get_connection():

    try:

        conexion = mysql.connector.connect(**DB_CONFIG)

        if conexion.is_connected():

            print("✅ Conexión exitosa a MySQL")

            return conexion

    except Error as e:

        print("❌ Error al conectar a MySQL:", e)

        return None