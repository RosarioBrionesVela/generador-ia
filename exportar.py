import csv


def exportar_csv(registros, nombre="datos.csv"):

    if not registros:
        return

    keys = registros[0].keys()

    with open(nombre, "w", newline="", encoding="utf-8") as f:

        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(registros)

    print(f"📁 Exportado a {nombre}")