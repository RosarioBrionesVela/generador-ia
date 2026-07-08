import mysql.connector


def conectar(host, puerto, usuario, password, database):

    try:
        conexion = mysql.connector.connect(
            host=host,
            port=puerto,
            user=usuario,
            password=password,
            database=database
        )

        if conexion.is_connected():
            print("\n✅ Conexión establecida correctamente.\n")
            return conexion

    except mysql.connector.Error as error:
        print(f"\n❌ Error de conexión: {error}\n")

    return None