import customtkinter as ctk
from src.data.repository import *
from src.ui.uiUtils import *
from tkinter import messagebox, ttk

class ListaParametros(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand = True)
        self.on_back = on_back

        self.parametros = traerParametros()

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            self.scroll_container,
            text="Configuración General",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        crear_subtitulo(self.scroll_container, "Listado de Parámetros")

        tabla_frame = ctk.CTkFrame(self.scroll_container)
        tabla_frame.pack(fill="both", expand=False, padx=10)

        columnas = ("id", "codigo", "nombre","unidad", "limiteMinimo", "limiteMaximo",
                     "limiteWarningMin", "LimiteWarningMax", "normativa", "ponderacion")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

        self.tree.heading("id", text="Nro")
        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Parámetro")
        self.tree.heading("unidad", text="Unidad")
        self.tree.heading("limiteMinimo", text="Límite Mínimo Aceptable")
        self.tree.heading("limiteMaximo", text="Límite Máximo Aceptable")
        self.tree.heading("limiteWarningMin", text="Límite Mínimo Crítico")
        self.tree.heading("LimiteWarningMax", text="Límite Máximo Crítico")
        self.tree.heading("normativa", text="Normativa")
        self.tree.heading("ponderacion", text="Ponderación")


        self.tree.column("id", anchor="e", width=50,stretch=False)
        self.tree.column("codigo", anchor="e", width=50,stretch=False)
        self.tree.column("nombre", anchor="w", width=150,stretch=False)
        self.tree.column("unidad", anchor="w", width=100,stretch=False)
        self.tree.column("limiteMinimo", anchor="e", width=180,stretch=False)
        self.tree.column("limiteMaximo", anchor="e", width=180,stretch=False)
        self.tree.column("limiteWarningMin", anchor="e", width=180,stretch=False)
        self.tree.column("LimiteWarningMax", anchor="e", width=180,stretch=False)
        self.tree.column("normativa", anchor="w", width=200,stretch=False)
        self.tree.column("ponderacion", anchor="e", width=100,stretch=False)

        scroll_x = ttk.Scrollbar(
            tabla_frame,
            orient="horizontal",
            command=self.tree.xview
        )
        self.tree.configure(xscrollcommand=scroll_x.set)

        self.tree.pack(fill="both", expand=True)
        scroll_x.pack(side="bottom", fill="x")


        for p in self.parametros:
            r = traerValoresReferenciaPorParametro(p["id"]) or {}
            pond = traerPonderacionParametro(p["id"]) or {}
            self.tree.insert("", "end", values=(
                p["id"],
                p["codigo"],
                p["nombreParametro"],
                p["unidad"],
                r.get("limiteMinAceptable",0),
                r.get("limiteMaxAceptable",0),
                r.get("limiteMinWarning",0),
                r.get("limiteMaxWarning",0),
                r.get("normativa",""),
                pond.get("ponderacion",0)      
            ))

        crear_separador(self.scroll_container)

        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=20)

        ctk.CTkButton(
            frame_botones,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Agregar Parámetro",
            width=150,
            command=self.FormularioAgregarParametro
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            frame_botones,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Modificar",
            width=150,
            command= self.ModificarParametro
        ).pack(side="left", padx=20)
        
        ctk.CTkButton(
            frame_botones,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text="Volver",
            width=150,
            command=self.verificarYSalir
        ).pack(side="left", padx=20)


    def FormularioAgregarParametro(self):

        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Agregar Nuevo Parámetro")

        if hasattr(self, "form_frame"):
            self.form_frame.destroy()
        self.form_frame = ctk.CTkFrame(self.scroll_container)
        self.form_frame.pack(pady=20, fill="x", padx=20)

        self.entries = {}
        campos = [
            ("codigo", "Código"),
            ("nombreParametro", "Nombre del Parámetro"),
            ("unidad", "Unidad (En caso de no aplicar, colocar '-')"),
            ("limiteMinAceptable", "Límite Mínimo Aceptable"),
            ("limiteMaxAceptable", "Límite Máximo Aceptable"),
            ("limiteMinWarning", "Límite Mínimo Crítico"),
            ("limiteMaxWarning", "Límite Máximo Crítico"),
            ("normativa", "Normativa (En caso de no aplicar, colocar '-')"),
            ("ponderacion", "Ponderación (0-1)")
        ]

        for key, label in campos:
            ctk.CTkLabel(self.form_frame,text=label).pack(anchor="w", pady=(10,0))
            entry = ctk.CTkEntry(self.form_frame)
            entry.pack(fill="x", pady=5)
            self.entries[key] = entry

        self.btnGuardar = ctk.CTkButton(
            self.form_frame,
            text="Guardar",
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            width=150,
            command=self.guardarParametro
        )
        self.btnGuardar.pack(pady=20)

    def guardarParametro(self):

        datos = {key: entry.get() for key, entry in self.entries.items()}

        if any(v == "" for v in datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        
        try:
            ponderacion = float(datos["ponderacion"])
        except ValueError:
            messagebox.showerror("Error", "La ponderación debe ser numérica.")
            return
        
        if not (0 <= ponderacion <= 1):
            messagebox.showerror("Error", "La ponderación debe estar entre 0 y 1.")
            return
        
        for p in self.parametros:
            if p["codigo"] == datos["codigo"]:
                messagebox.showerror("Error", "El código del parámetro ya existe.")
                return
            if p["nombreParametro"] == datos["nombreParametro"]:
                messagebox.showerror("Error", "El nombre del parámetro ya existe.")
                return
        
        try:
            id_parametro = insertarParametro(
                    datos["codigo"],
                    datos["nombreParametro"],
                    datos["unidad"]
                )
            
            insertarValoresReferencia(
                id_parametro,
                float(datos["limiteMaxAceptable"]),
                float(datos["limiteMaxWarning"]),
                float(datos["limiteMinAceptable"]),
                float(datos["limiteMinWarning"]),
                datos["normativa"]
            )

            insertarPonderacionParametro(
                id_parametro,
                ponderacion
            )

        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error al guardar el parámetro: {str(e)}")
            return
        
        messagebox.showinfo("Éxito", "Parámetro guardado exitosamente.")
        self.form_frame.destroy()
        del self.form_frame
        
        self.recargarTabla()
    
    def recargarTabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        self.parametros = traerParametros()

        for p in self.parametros:
            r = traerValoresReferenciaPorParametro(p["id"]) or {}
            pond = traerPonderacionParametro(p["id"]) or {}
            self.tree.insert("", "end", values=(
                p["id"],
                p["codigo"],
                p["nombreParametro"],
                p["unidad"],
                r.get("limiteMinAceptable",0),
                r.get("limiteMaxAceptable",0),
                r.get("limiteMinWarning",0),
                r.get("limiteMaxWarning",0),
                r.get("normativa",""),
                pond.get("ponderacion",0)      
            ))
    
    def verificarYSalir(self):
        ponderaciones = traerPonderacionesParametroActivas()
        
        suma_ponderaciones = sum(p["ponderacion"] for p in ponderaciones)
        if round(suma_ponderaciones, 6) != 1:
            messagebox.showerror(
                "Error de Configuración",
                f"La suma de las ponderaciones debe ser 1.\n\n"
                f"Suma actual: {round(suma_ponderaciones, 6)}"
            )
            return

        self.on_back()

    def ModificarParametro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una medición")
            return

        item = self.tree.item(selected[0])
        valores = item["values"]

        self.id_parametro_editando = valores[0]

        self.mostrar_formulario_edicion(valores)
    
    def mostrar_formulario_edicion(self, valores):
        
        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Modificar Parámetro")
        
        
        if hasattr(self, "form_frame"):
            self.form_frame.destroy()
            del self.form_frame

        self.form_frame = ctk.CTkFrame(self.scroll_container)
        self.form_frame.pack(pady=20, fill="x", padx=20)

        self.entries = {}

        campos = [
            ("codigo", "Código", valores[1]),
            ("nombre", "Nombre", valores[2]),
            ("unidad", "Unidad", valores[3]),
            ("limiteMinAceptable", "Límite Mín Aceptable", valores[4]),
            ("limiteMaxAceptable", "Límite Máx Aceptable", valores[5]),
            ("limiteMinWarning", "Límite Mín Crítico", valores[6]),
            ("limiteMaxWarning", "Límite Máx Crítico", valores[7]),
            ("normativa", "Normativa", valores[8]),
            ("ponderacion", "Ponderación", valores[9])
        ]

        for key, label, value in campos:
            ctk.CTkLabel(self.form_frame, text=label).pack(anchor="w", pady=(10,0))
            entry = ctk.CTkEntry(self.form_frame)
            entry.insert(0, str(value))
            entry.pack(pady=5, fill="x")
            self.entries[key] = entry

        ctk.CTkButton(
            self.form_frame,
            text="Guardar Cambios",
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            width=150,
            command=self.guardar_modificacion
        ).pack(pady=10)
    
    def guardar_modificacion(self):

        datos = {k: e.get().strip() for k, e in self.entries.items()}

        if any(v == "" for v in datos.values()):
            messagebox.showerror("Error", "Todos los campos deben completarse." \
            "Colocar - si aplica a campos no numéricos.")
            return

        try:
            nueva_ponderacion = float(datos["ponderacion"])
        except ValueError:
            messagebox.showerror("Error", "La ponderación debe ser numérica.")
            return

        if not (0 <= nueva_ponderacion <= 1):
            messagebox.showerror("Error", "La ponderación debe estar entre 0 y 1.")
            return

    
        for p in self.parametros:
            if p["id"] == self.id_parametro_editando:
                continue

            if p["codigo"] == datos["codigo"]:
                messagebox.showerror("Error", "Código duplicado.")
                return

            if p["nombreParametro"] == datos["nombre"]:
                messagebox.showerror("Error", "Nombre duplicado.")
                return

        self.id_parametro_editando = int(self.id_parametro_editando)

        try:
            actualizarParametro(
                self.id_parametro_editando,
                datos["codigo"],
                datos["nombre"],
                datos["unidad"]
            )

            actualizarValoresReferencia(
                self.id_parametro_editando,
                float(datos["limiteMaxAceptable"]),
                float(datos["limiteMaxWarning"]),
                float(datos["limiteMinAceptable"]),
                float(datos["limiteMinWarning"]),
                datos["normativa"]
            )

            actualizarPonderacion(
                self.id_parametro_editando,
                nueva_ponderacion
            )

        except Exception as e:
            messagebox.showerror("Error BD", str(e))
            return

        messagebox.showinfo("Éxito", "Parámetro modificado correctamente.")

        self.form_frame.destroy()
        del self.form_frame

        self.recargarTabla()

