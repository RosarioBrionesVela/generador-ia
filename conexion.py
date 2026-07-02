import mysql.connector

def conectar():

    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Contraseña123@",
            database="generador_ia"
        )

        if conexion.is_connected():
            print("✅ Conexión exitosa a MySQL.")
            return conexion

    except mysql.connector.Error as error:
        print("❌ Error de conexión:", error)

    return None