from conexion import conectar
from generador import generar_registros
from inserciones import insertar_registros
from exportar import exportar_csv


def linea():
    print("═" * 60)


def titulo(texto):
    linea()
    print(f" {texto.center(58)} ")
    linea()


def mostrar_tablas(cursor):

    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()

    if not tablas:
        print("\n❌ No se encontraron tablas en la base de datos.")
        return []

    titulo("TABLAS DISPONIBLES")

    for i, t in enumerate(tablas, start=1):
        print(f" {i}. {t[0]}")

    return tablas


def obtener_estructura(cursor, tabla):

    cursor.execute(f"DESCRIBE {tabla}")
    columnas = cursor.fetchall()

    campos = []

    titulo(f"ESTRUCTURA DE '{tabla}'")

    print(f"{'Campo':20}{'Tipo':20}{'Llave'}")
    print("-" * 60)

    for col in columnas:

        campo = {
            "nombre": col[0],
            "tipo": col[1],
            "null": col[2],
            "key": col[3],
            "extra": col[5]
        }

        campos.append(campo)

        print(f"{campo['nombre']:20}{campo['tipo']:20}{campo['key']}")

    return campos


def solicitar_conexion():

    titulo("DATOS DE CONEXIÓN")

    host = input("🌐 Host [localhost]: ").strip()
    if host == "":
        host = "localhost"

    puerto = input("🔌 Puerto [3306]: ").strip()
    if puerto == "":
        puerto = "3306"

    usuario = input("👤 Usuario: ").strip()
    password = input("🔒 Contraseña: ")
    database = input("🗄️ Base de datos: ").strip()

    return host, int(puerto), usuario, password, database


def main():

    titulo("GENERADOR INTELIGENTE DE INSERCIONES")

    host, puerto, usuario, password, database = solicitar_conexion()

    conexion = conectar(
        host,
        puerto,
        usuario,
        password,
        database
    )

    if not conexion:
        print("❌ No fue posible establecer la conexión.")
        return

    cursor = conexion.cursor()

    tablas = mostrar_tablas(cursor)

    if not tablas:
        cursor.close()
        conexion.close()
        return

    while True:
        try:

            op = int(input("\n📌 Seleccione una tabla: ")) - 1

            if op < 0 or op >= len(tablas):
                print("❌ Opción inválida.")
                continue

            break

        except ValueError:
            print("❌ Ingrese únicamente números.")

    tabla = tablas[op][0]

    campos = obtener_estructura(cursor, tabla)

    while True:

        try:

            n = int(input("\n📝 ¿Cuántos registros desea generar?: "))

            if n <= 0:
                print("❌ Debe ser mayor que cero.")
                continue

            break

        except ValueError:
            print("❌ Ingrese un número válido.")

    print("\n⏳ Generando datos...")

    registros = generar_registros(campos, n)

    titulo("VISTA PREVIA")

    for i, registro in enumerate(registros, start=1):

        print(f"\nRegistro {i}")

        for campo, valor in registro.items():
            print(f"   {campo:<20}: {valor}")

    exportar_csv(registros)

    print("\n✅ Los datos también fueron exportados a 'datos_generados.csv'.")

    while True:

        resp = input("\n💾 ¿Desea insertar los registros en la base de datos? (S/N): ").upper()

        if resp in ["S", "N"]:
            break

        print("❌ Escriba únicamente S o N.")

    if resp == "S":

        insertar_registros(cursor, conexion, tabla, registros)

        print("\n🎉 Proceso finalizado correctamente.")

    else:

        print("\n⚠ Inserción cancelada por el usuario.")

    cursor.close()
    conexion.close()

    linea()
    print(" Gracias por utilizar el Generador Inteligente ")
    linea()


if __name__ == "__main__":
    main()