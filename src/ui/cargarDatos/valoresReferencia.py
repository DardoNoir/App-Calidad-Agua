import customtkinter as ctk
from src.data.repository import (insertarValoresReferencia, valoresReferenciaCargados, traerParametros)
from src.ui.uiUtils import *
from tkinter import messagebox

class CargarValoresReferencia(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back=on_back

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        self.parametros = traerParametros()

        # Diccionario: nombreParametro → id
        self.parametro_por_nombre = {
            p["nombreParametro"]: p["id"]
            for p in self.parametros}

        # Lista SOLO de nombres para el combo
        nombres_parametros = list(self.parametro_por_nombre.keys())

        ctk.CTkLabel(
            self.scroll_container,
            text=f"Cargar Valores de Referencia",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        crear_subtitulo(self.scroll_container, "Selección de Parámetro")
        self.rol_combo=ctk.CTkOptionMenu(
            self.scroll_container,
            width=300,
            values=nombres_parametros,
            fg_color="#3b3b3b",
            button_color="#555555"
        )
        self.rol_combo.set("Seleccione un Parámetro")
        self.rol_combo.pack(pady=10)
        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Cargar valores de referencia")
        crear_subtitulo(self.scroll_container, "Límites Aceptable")
        self.minAcep=ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Límite Mínimo Aceptable...")
        self.minAcep.pack(pady=10)
        
        self.maxAcep=ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Límite Máximo Aceptable...")
        self.maxAcep.pack(pady=10)
        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Límites Críticos")
        self.minWar=ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Límite Mínimo Crítico...")
        self.minWar.pack(pady=10)
        
        self.maxWar=ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Límite Máximo Crítico...")
        self.maxWar.pack(pady=10)
        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Normativa Vigente")
        self.norm=ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Normativa Vigente...")
        self.norm.pack(pady=10)        
        
        ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Guardar Valores de Referencia", 
            width=250,
            command=self.guardarValoresdeReferencia).pack(pady=10)
        
        ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text="Volver",
            width=250,
            command=on_back).pack()
    
    def guardarValoresdeReferencia(self):
        nombre=self.rol_combo.get()
        if nombre == "Seleccione un Parámetro":
            messagebox.showerror("Error", "No se seleccionó un Parámetro")
            return

        idParametro = self.parametro_por_nombre[nombre]
        
        if (not self.minAcep.get().strip() or
            not self.maxAcep.get().strip() or
            not self.minWar.get().strip() or
            not self.maxWar.get().strip()):
                messagebox.showerror("Error", "Faltan completar límites del parámetro")
                return

        try:
            limiteMinAcep = float(self.minAcep.get())
            limiteMaxAcep = float(self.maxAcep.get())
            limiteMinWarn = float(self.minWar.get())
            limiteMaxWarn = float(self.maxWar.get())
        except ValueError:
            messagebox.showerror("Error","Los límites deben ser numéricos")
            return
        
        if valoresReferenciaCargados(idParametro):
            messagebox.showinfo("Atención", f"El Parámetro {nombre} ya cuenta con valores de referencia")
            return

        insertarValoresReferencia(idParametro, limiteMaxAcep, limiteMaxWarn,
                                  limiteMinAcep, limiteMinWarn, self.norm.get())
        self.on_back()
        messagebox.showinfo("Guardado Existos", "Valores de referencia cargados correctamente ✔")
        