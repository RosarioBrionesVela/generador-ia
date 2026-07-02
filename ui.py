import tkinter as tk
from tkinter import messagebox, ttk

from conexion import conectar
from generador import generar_registros
from inserciones import insertar_registros


conexion = None
cursor = None
tablas = []
registros = []


def conectar_bd():

    global conexion, cursor, tablas

    conexion = conectar()

    if not conexion:
        messagebox.showerror("Error", "No se pudo conectar")
        return

    cursor = conexion.cursor()

    cursor.execute("SHOW TABLES")
    tablas = cursor.fetchall()

    combo_tablas["values"] = [t[0] for t in tablas]

    if tablas:
        combo_tablas.current(0)

    label_estado.config(text="✨ Conectado correctamente")


def generar_datos():

    global registros

    try:
        tabla = combo_tablas.get()
        cantidad = int(entry_cantidad.get())

        cursor.execute(f"DESCRIBE {tabla}")
        columnas = cursor.fetchall()

        campos = []

        for col in columnas:
            campos.append({
                "nombre": col[0],
                "tipo": col[1],
                "null": col[2],
                "key": col[3],
                "extra": col[5]
            })

        registros = generar_registros(campos, cantidad)

        text.delete("1.0", tk.END)

        for i, r in enumerate(registros, 1):
            text.insert(tk.END, f"{i}. {r}\n")

        label_estado.config(text=f"💖 {len(registros)} registros generados")

    except Exception as e:
        messagebox.showerror("Error", str(e))


def insertar():

    try:
        tabla = combo_tablas.get()

        insertar_registros(cursor, conexion, tabla, registros)

        label_estado.config(text="🌸 Datos insertados con éxito")

        messagebox.showinfo("Listo", "Inserción completada 💕")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# ================= UI =================

ventana = tk.Tk()
ventana.title("🍓 Generador IA Pastel")
ventana.geometry("800x600")
ventana.configure(bg="#ffe6f0")  # rosa pastel fondo


# TÍTULO
titulo = tk.Label(
    ventana,
    text="🍓 GENERADOR IA DE DATOS 🍓",
    font=("Arial", 16, "bold"),
    bg="#ffe6f0",
    fg="#6b4c7a"
)
titulo.pack(pady=10)


# FRAME SUPERIOR
frame_top = tk.Frame(ventana, bg="#ffe6f0")
frame_top.pack(pady=10)


# BOTÓN CONECTAR
btn_conectar = tk.Button(
    frame_top,
    text="🌸 Conectar BD",
    command=conectar_bd,
    bg="#ffd1dc",
    fg="#4a3b4d",
    width=15,
    relief="flat"
)
btn_conectar.grid(row=0, column=0, padx=5)


# COMBO TABLAS
combo_tablas = ttk.Combobox(frame_top, width=30)
combo_tablas.grid(row=0, column=1, padx=5)


# CANTIDAD
entry_cantidad = tk.Entry(frame_top, width=10, bg="#fff0f5", fg="#4a3b4d")
entry_cantidad.grid(row=0, column=2, padx=5)
entry_cantidad.insert(0, "10")


# BOTÓN GENERAR
btn_generar = tk.Button(
    frame_top,
    text="✨ Generar",
    command=generar_datos,
    bg="#cdb4db",
    fg="white",
    width=10,
    relief="flat"
)
btn_generar.grid(row=0, column=3, padx=5)


# BOTÓN INSERTAR
btn_insertar = tk.Button(
    frame_top,
    text="💾 Insertar",
    command=insertar,
    bg="#bde0fe",
    fg="#3a3a3a",
    width=10,
    relief="flat"
)
btn_insertar.grid(row=0, column=4, padx=5)


# ESTADO
label_estado = tk.Label(
    ventana,
    text="🌷 Esperando conexión...",
    bg="#ffe6f0",
    fg="#6b4c7a"
)
label_estado.pack(pady=5)


# TEXTO
text = tk.Text(
    ventana,
    height=20,
    width=90,
    bg="#fffafc",
    fg="#4a3b4d",
    insertbackground="#4a3b4d"
)
text.pack(pady=10)


ventana.mainloop()