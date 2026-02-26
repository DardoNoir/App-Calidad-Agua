import customtkinter as ctk
from src.data.repository import *
from src.ui.uiUtils import *
from tkinter import messagebox, ttk
from src.ui.parametros.formParametro import FormParametro


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
            command=self.irAgregarParametro
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            frame_botones,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Modificar",
            width=150,
            command= self.irModificarParametro
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

        pie_pagina(self.scroll_container)


    def irAgregarParametro(self):
        self.destroy()
        FormParametro(self.master, self.volver_a_lista, modo="alta")

    def irModificarParametro(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Seleccione un parámetro para modificar.")
            return
        values = self.tree.item(selected[0], "values")
        id_parametro = values[0]
        self.destroy()
        FormParametro(self.master, self.volver_a_lista, modo="edicion", id_parametro=id_parametro)

    def volver_a_lista(self):
        self.destroy()
        ListaParametros(self.master, self.on_back)

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

