from conexion import conectar
from generador import generar_registros
from inserciones import insertar_registros
from exportar import exportar_csv   


def mostrar_tablas(cursor):

    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()

    if not tablas:
        print("❌ No hay tablas.")
        return []

    print("\n===== TABLAS =====\n")

    for i, t in enumerate(tablas, 1):
        print(f"{i}. {t[0]}")

    return tablas


def obtener_estructura(cursor, tabla):

    cursor.execute(f"DESCRIBE {tabla}")
    columnas = cursor.fetchall()

    campos = []

    print("\n===== ESTRUCTURA =====\n")

    for col in columnas:

        campo = {
            "nombre": col[0],
            "tipo": col[1],
            "null": col[2],
            "key": col[3],
            "extra": col[5]
        }

        campos.append(campo)

        print(f"{campo['nombre']} | {campo['tipo']} | {campo['key']}")

    return campos


def main():

    conexion = conectar()

    if not conexion:
        return

    cursor = conexion.cursor()

    tablas = mostrar_tablas(cursor)

    if not tablas:
        return

    # VALIDAR TABLA
    while True:
        try:
            op = int(input("\nSeleccione tabla: ")) - 1

            if op < 0 or op >= len(tablas):
                print("❌ Opción inválida")
                continue
            break
        except:
            print("❌ Número inválido")

    tabla = tablas[op][0]

    campos = obtener_estructura(cursor, tabla)

    # VALIDAR CANTIDAD
    while True:
        try:
            n = int(input("\nCantidad de registros: "))
            if n <= 0:
                print("❌ Mayor a 0")
                continue
            break
        except:
            print("❌ Número inválido")

    registros = generar_registros(campos, n)

    print("\n===== VISTA PREVIA =====\n")

    exportar_csv(registros)

    for r in registros:
        print(r)

    # CONFIRMACIÓN
    while True:

        resp = input("\n¿Insertar? (S/N): ").upper()

        if resp in ["S", "N"]:
            break

        print("❌ Solo S o N")

    if resp == "S":
        insertar_registros(cursor, conexion, tabla, registros)
    else:
        print("❌ Cancelado")

    cursor.close()
    conexion.close()
    print("\n🔒 Fin del programa")


if __name__ == "__main__":
    main()