import time


def insertar_registros(cursor, conexion, tabla, registros):

    if not registros:
        print("⚠️ No hay registros.")
        return

    insertados = 0
    errores = 0
    inicio = time.time()

    for registro in registros:

        try:

            columnas = ", ".join(registro.keys())
            valores = list(registro.values())
            placeholders = ", ".join(["%s"] * len(valores))

            sql = f"""
            INSERT INTO {tabla}
            ({columnas})
            VALUES ({placeholders})
            """

            cursor.execute(sql, valores)
            insertados += 1

        except Exception as e:

            errores += 1

            with open("logs/errores.log", "a", encoding="utf-8") as f:
                f.write(f"\nREGISTRO: {registro}\nERROR: {str(e)}\n{'-'*50}\n")

    conexion.commit()

    fin = time.time()

    print("\n========== ESTADÍSTICAS ==========")
    print(f"✔ Insertados: {insertados}")
    print(f"❌ Errores: {errores}")
    print(f"⏱ Tiempo: {round(fin - inicio, 2)} seg")
    print("===================================")