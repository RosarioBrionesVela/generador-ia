from faker import Faker
import random

fake = Faker("es_MX")


def generar_registros(campos, cantidad):

    registros = []

    for _ in range(cantidad):

        registro = {}

        for campo in campos:

            nombre = campo["nombre"].lower()
            tipo = campo["tipo"].lower()

            # PK AUTO_INCREMENT
            if campo["key"] == "PRI" and "auto_increment" in campo["extra"]:
                continue

            valor = None

            # ENUM
            if "enum" in tipo:

                opciones = tipo.split("(")[1].replace(")", "").replace("'", "").split(",")
                opciones = [o.strip() for o in opciones]

                valor = random.choice(opciones)

            # TEXTO
            elif "varchar" in tipo or "char" in tipo or "text" in tipo:

                if "nombre" in nombre:
                    valor = fake.first_name()

                elif "apellido" in nombre:
                    valor = fake.last_name()

                elif "correo" in nombre or "email" in nombre:
                    valor = fake.email()

                elif "telefono" in nombre:
                    valor = fake.numerify("449########")

                elif "direccion" in nombre:
                    valor = fake.address()

                elif "ciudad" in nombre:
                    valor = fake.city()

                elif "pais" in nombre:
                    valor = fake.country()

                else:
                    valor = fake.word()

            # ENTEROS
            elif "int" in tipo:

                if "edad" in nombre:
                    valor = random.randint(18, 80)
                else:
                    valor = random.randint(1, 1000)

            # FECHAS
            elif "date" in tipo:
                valor = fake.date_between(start_date="-2y", end_date="today")

            # DECIMALES
            elif "float" in tipo or "decimal" in tipo:

                if "precio" in nombre:
                    valor = round(random.uniform(10, 5000), 2)
                else:
                    valor = round(random.uniform(1, 1000), 2)

            # NOT NULL fallback
            if valor is None:

                if campo["null"] == "NO":
                    valor = "DEFAULT"

            registro[nombre] = valor

        registros.append(registro)

    return registros