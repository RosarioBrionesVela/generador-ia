# 🤖 Generador Inteligente de Inserciones para Bases de Datos

Este proyecto es un sistema que genera e inserta datos automáticamente en tablas de bases de datos MySQL utilizando estructuras dinámicas y generación de datos realistas.

---

## 🚀 Descripción

El sistema se conecta a una base de datos MySQL, detecta automáticamente la estructura de una tabla y genera registros compatibles con cada tipo de dato. Posteriormente, inserta los datos en la base de datos o permite visualizarlos antes de la inserción.

Incluye una interfaz gráfica amigable y generación de datos realistas usando Faker.

---

## ✨ Características

- 🔌 Conexión a MySQL
- 📋 Detección automática de tablas
- 🧠 Generación inteligente de datos según tipo de columna
- 💖 Interfaz gráfica (Tkinter) 
- 👀 Vista previa de datos generados
- 💾 Inserción automática en la base de datos
- 📊 Estadísticas del proceso
- 🪵 Registro de errores en logs
- 🎲 Uso de datos realistas con Faker

---

## 🛠️ Tecnologías utilizadas

- Python 3
- MySQL
- mysql-connector-python
- Faker
- Tkinter

---

## 📂 Estructura del proyecto
GeneradorIA/
│
├── main.py
├── ui.py
├── conexion.py
├── generador.py
├── inserciones.py
├── exportar.py
│
└── logs/
└── errores.log

---

## 🧠 Uso de Inteligencia Artificial

Este proyecto utiliza la librería Faker para generar datos realistas como nombres, correos, direcciones y teléfonos. Esto simula el comportamiento de una IA generadora de datos para pruebas de bases de datos.


## ⚙️ Instalación

git clone https://github.com/tuusuario/generador-ia.git
cd generador-ia
pip install mysql-connector-python faker

## 🚀 Mejoras futuras

- Soporte para PostgreSQL y SQLite
- Exportación a Excel
- Interfaz web
- Detección avanzada de llaves foráneas


## 🔧 Configuración

Editar conexion.py:

host="localhost"
user="root"
password="tu_contraseña"
database="generador_ia"

## ▶️ Ejecución
-Consola:
python main.py
-Interfaz gráfica:
python ui.py