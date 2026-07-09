import tkinter as tk
from tkinter import ttk, messagebox
import time

from conexion import conectar
from generador import generar_registros
from inserciones import insertar_registros


class GeneradorIAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍓 Generador IA de Datos")
        self.root.geometry("1100x750")
        self.root.configure(bg="#ffe6f0")

        self.conexion = None
        self.cursor = None
        self.registros = []

        self._crear_conexion()
        self._crear_configuracion()
        self._crear_vista_previa()
        self._crear_sql()
        self._crear_estadisticas()

    def _crear_frame(self, titulo):
        frame = tk.LabelFrame(
            self.root,
            text=titulo,
            bg="#ffe6f0",
            fg="#6b4c7a",
            font=("Arial", 11, "bold"),
            padx=8,
            pady=8
        )
        frame.pack(fill="x", padx=10, pady=5)
        return frame

    def _crear_conexion(self):
        f = self._crear_frame("🔐 Conexión")

        labels = ["Host", "Puerto", "Usuario", "Contraseña", "Base de datos"]
        defaults = ["localhost", "3306", "root", "", ""]
        self.entries = {}

        for i, (lab, val) in enumerate(zip(labels, defaults)):
            tk.Label(f, text=lab, bg="#ffe6f0").grid(row=i, column=0, sticky="w")
            ent = tk.Entry(f, width=30, show="*" if "Contraseña" in lab else "")
            ent.insert(0, val)
            ent.grid(row=i, column=1, padx=5, pady=2)
            self.entries[lab] = ent

        tk.Button(
            f,
            text="🌸 Conectar",
            bg="#ffd1dc",
            command=self.conectar_bd
        ).grid(row=5, column=0, columnspan=2, pady=5)

        self.estado = tk.Label(f, text="Sin conexión", bg="#ffe6f0", fg="red")
        self.estado.grid(row=6, column=0, columnspan=2)

    def _crear_configuracion(self):
        f = self._crear_frame("⚙ Configuración")

        tk.Label(f, text="Buscar tabla", bg="#ffe6f0").grid(row=0, column=0)

        self.combo = ttk.Combobox(
            f,
            width=35
        )
        self.combo.grid(row=0, column=1, padx=5)

        # Lista completa de tablas
        self.lista_tablas = []

        # Filtrar mientras escribe
        self.combo.bind("<KeyRelease>", self.filtrar_tablas)

        tk.Label(f, text="Cantidad", bg="#ffe6f0").grid(row=0, column=2)

        self.cantidad = tk.Entry(f, width=10)
        self.cantidad.insert(0, "10")
        self.cantidad.grid(row=0, column=3)

        tk.Button(
            f,
            text="✨ Generar",
            command=self.generar,
            bg="#cdb4db",
            fg="white"
        ).grid(row=0, column=4, padx=5)

        tk.Button(
            f,
            text="💾 Insertar",
            command=self.insertar,
            bg="#bde0fe"
        ).grid(row=0, column=5)


    def _crear_vista_previa(self):
        f = self._crear_frame("📋 Vista previa")

        self.tree = ttk.Treeview(f)
        self.tree.pack(fill="both", expand=True)

    def _crear_sql(self):
        f = self._crear_frame("📄 SQL generado")

        self.sql = tk.Text(f, height=8)
        self.sql.pack(fill="both", expand=True)

    def _crear_estadisticas(self):
        f = self._crear_frame("📊 Estadísticas")

        self.stats = tk.Label(
            f,
            text="Base de datos: -\nTabla: -\nRegistros: 0\nTiempo: 0 s",
            justify="left",
            bg="#ffe6f0"
        )
        self.stats.pack(anchor="w")

    def conectar_bd(self):

        self.conexion = conectar(
            self.entries["Host"].get(),
            self.entries["Puerto"].get(),
            self.entries["Usuario"].get(),
            self.entries["Contraseña"].get(),
            self.entries["Base de datos"].get()
        )

        if not self.conexion:
            return

        self.cursor = self.conexion.cursor()

        try:
            self.cursor.execute("SHOW TABLES")

            self.lista_tablas = [t[0] for t in self.cursor.fetchall()]

            self.combo["values"] = self.lista_tablas

            if self.lista_tablas:
                self.combo.current(0)

            self.estado.config(
                text="✅ Conectado correctamente",
                fg="green"
            )

            messagebox.showinfo(
                "Conexión",
                "Conexión establecida correctamente."
            )

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudieron obtener las tablas.\n\n{e}"
            )

    def filtrar_tablas(self, event=None):
        texto = self.combo.get().lower()

        if texto == "":
            self.combo["values"] = self.lista_tablas
            return

        coincidencias = [
            tabla for tabla in self.lista_tablas
            if texto in tabla.lower()
        ]

        self.combo["values"] = coincidencias

        if coincidencias:
            self.combo.event_generate("<Down>")

    def generar(self):
        if not self.cursor:
            messagebox.showwarning("Aviso", "Conéctate primero.")
            return

        inicio = time.time()

        tabla = self.combo.get()
        cantidad = int(self.cantidad.get())

        self.cursor.execute(f"DESCRIBE {tabla}")
        columnas = self.cursor.fetchall()

        campos = [{
            "nombre": c[0],
            "tipo": c[1],
            "null": c[2],
            "key": c[3],
            "extra": c[5]
        } for c in columnas]


        self.registros = generar_registros(campos, cantidad)


        for i in self.tree.get_children():
            self.tree.delete(i)

        self.tree["columns"] = [c["nombre"] for c in campos]
        self.tree["show"] = "headings"

        for c in campos:
            self.tree.heading(c["nombre"], text=c["nombre"])
            self.tree.column(c["nombre"], width=120)

        for r in self.registros:
            self.tree.insert("", "end", values=list(r.values()))

        if self.registros:
            cols = ",".join(self.registros[0].keys())
            values = []
            for r in self.registros:
                fila = "(" + ",".join(repr(v) for v in r.values()) + ")"
                values.append(fila)
            sql = f"INSERT INTO {tabla} ({cols}) VALUES\n" + ",\n".join(values) + ";"
            self.sql.delete("1.0", tk.END)
            self.sql.insert(tk.END, sql)

        tiempo = round(time.time() - inicio, 2)

        self.stats.config(
            text=f"Base de datos: {self.entries['Base de datos'].get()}\n"
                 f"Tabla: {tabla}\n"
                 f"Registros: {len(self.registros)}\n"
                 f"Tiempo: {tiempo} s\n"
                 f"Estado: Correcto"
        )

    def insertar(self):
        if not self.registros:
            messagebox.showwarning("Aviso", "Genera registros primero.")
            return

        insertar_registros(
            self.cursor,
            self.conexion,
            self.combo.get(),
            self.registros
        )

        messagebox.showinfo("Éxito", "Registros insertados correctamente.")


if __name__ == "__main__":
    root = tk.Tk()
    app = GeneradorIAApp(root)
    root.mainloop()