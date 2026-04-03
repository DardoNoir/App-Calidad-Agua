import customtkinter as ctk
from tkinter import messagebox

from matplotlib import text
from src.data.repository import *
from src.ui.uiUtils import *

class FormParametro(ctk.CTkFrame):
    def __init__(self, master, on_back, modo="alta", id_parametro=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_back = on_back
        self.modo = modo
        self.id_parametro = id_parametro

        self.parametros = traerParametros()

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        titulo = "Agregar Parámetro" if modo == "alta" else "Modificar Parámetro"

        ctk.CTkLabel(
            self.scroll_container,
            text=titulo,
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        self.entries = {}

        crear_subtitulo(self.scroll_container, "Datos del Parámetro")

        camposDatos = [
            ("codigo", "Código"),
            ("nombreParametro", "Nombre del Parámetro"),
            ("unidad", "Unidad")]
        
        for key, label in camposDatos:
            ctk.CTkLabel(self.scroll_container, text=label).pack(anchor="w", pady=(10, 0))
            entry = ctk.CTkEntry(self.scroll_container)
            entry.pack(fill="x", pady=5)
            self.entries[key] = entry
        
        crear_separador(self.scroll_container)
        
        crear_subtitulo(self.scroll_container, "Valores de Referencia")
        camposReferencia = [
            ("limiteMinAceptable", "Límite Mínimo Aceptable"),
            ("limiteMaxAceptable", "Límite Máximo Aceptable"),
            ("limiteMinWarning", "Límite Mínimo Crítico"),
            ("limiteMaxWarning", "Límite Máximo Crítico"),
            ("rangoPosibleMin", "Rango Posible Mínimo"),
            ("rangoPosibleMax", "Rango Posible Máximo"),
            ("normativa", "Normativa")]
        
        for key, label in camposReferencia:
            ctk.CTkLabel(self.scroll_container, text=label).pack(anchor="w", pady=(10, 0))
            entry = ctk.CTkEntry(self.scroll_container)
            entry.pack(fill="x", pady=5)
            self.entries[key] = entry
        
        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Ponderación")
        camposPonderacion = [
            ("ponderacion", "Ponderación (0-1)")
        ]

        for key, label in camposPonderacion:
            ctk.CTkLabel(self.scroll_container, text=label).pack(anchor="w", pady=(10, 0))
            entry = ctk.CTkEntry(self.scroll_container)
            entry.pack(fill="x", pady=5)
            self.entries[key] = entry

        if modo == "edicion" and id_parametro:
            self.cargar_datos()

        frame_botones = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        frame_botones.pack(pady=20)

        btn_guardar = ctk.CTkButton(
            frame_botones,
            height=40,
            text="Guardar",
            width=140,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            command=self.guardar
        )
        btn_guardar.pack(side="left", padx=15)

        btn_volver = ctk.CTkButton(
            frame_botones,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text="Volver",
            width=150,
            command=self.volver
        )
        
        btn_volver.pack(side="left", padx=15)


    # =============================
    # CARGA DE DATOS (EDICIÓN)
    # =============================
    def cargar_datos(self):
        if self.id_parametro is None:
            return
        id_param = int(self.id_parametro) if isinstance(self.id_parametro, (int, str)) else 0
        p = traerParametroPorId(id_param)
        if p is None:
            messagebox.showerror("Error", "Parámetro no encontrado.")
            return
        r = traerValoresReferenciaPorParametro(id_param) or {}
        pond = traerPonderacionParametro(id_param) or {}

        self.entries["codigo"].insert(0, p["codigo"])
        self.entries["nombreParametro"].insert(0, p["nombreParametro"])
        self.entries["unidad"].insert(0, p["unidad"])
        self.entries["limiteMinAceptable"].insert(0, r.get("limiteMinAceptable", 0))
        self.entries["limiteMaxAceptable"].insert(0, r.get("limiteMaxAceptable", 0))
        self.entries["limiteMinWarning"].insert(0, r.get("limiteMinWarning", 0))
        self.entries["limiteMaxWarning"].insert(0, r.get("limiteMaxWarning", 0))
        self.entries["rangoPosibleMin"].insert(0, r.get("rangoPosibleMin", 0))
        self.entries["rangoPosibleMax"].insert(0, r.get("rangoPosibleMax", 0))
        self.entries["normativa"].insert(0, r.get("normativa", ""))
        self.entries["ponderacion"].insert(0, pond.get("ponderacion", 0))

        pie_pagina(self.scroll_container)

    # =============================
    # GUARDAR
    # =============================
    def guardar(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}

        if any(v == "" for v in datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            ponderacion = float(datos["ponderacion"])
        except:
            messagebox.showerror("Error", "Ponderación inválida.")
            return

        if not (0 <= ponderacion <= 1):
            messagebox.showerror("Error", "La ponderación debe estar entre 0 y 1.")
            return

        try:
            if self.modo == "alta":
                id_param = insertarParametro(
                    datos["codigo"],
                    datos["nombreParametro"],
                    datos["unidad"]
                )

                insertarValoresReferencia(
                    id_param,
                    float(datos["limiteMaxAceptable"]),
                    float(datos["limiteMaxWarning"]),
                    float(datos["limiteMinAceptable"]),
                    float(datos["limiteMinWarning"]),
                    datos["normativa"],
                    float(datos["rangoPosibleMin"]),
                    float(datos["rangoPosibleMax"])
                )

                insertarPonderacionParametro(id_param, ponderacion)

            else:
                if self.id_parametro is None:
                    messagebox.showerror("Error", "ID del parámetro no válido.")
                    return
                actualizarParametro(
                    int(self.id_parametro),
                    datos["codigo"],
                    datos["nombreParametro"],
                    datos["unidad"]
                )

                actualizarValoresReferencia(
                    int(self.id_parametro),
                    float(datos["limiteMaxAceptable"]),
                    float(datos["limiteMaxWarning"]),
                    float(datos["limiteMinAceptable"]),
                    float(datos["limiteMinWarning"]),
                    datos["normativa"],
                    float(datos["rangoPosibleMin"]),
                    float(datos["rangoPosibleMax"])
                )

                actualizarPonderacion(
                    int(self.id_parametro),
                    ponderacion
                )

        except Exception as e:
            messagebox.showerror("Error BD", str(e))
            return

        messagebox.showinfo("Éxito", "Parámetro guardado correctamente.")
        self.volver()

    def volver(self):
        self.destroy()
        self.on_back()
