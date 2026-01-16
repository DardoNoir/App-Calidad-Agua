import customtkinter as ctk
import src.ui.session as session
from src.data.repository import *
from datetime import datetime
from src.utils.datetime import parse_fecha_str
from src.ui.uiUtils import *
from tkinter import messagebox


class CargarMediciones(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back = on_back

        self.parametros = traerParametros()
        self.inputs = {}

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            self.scroll_container,
            text=f"Cargar Medición",
            font=("Segoe UI", 20, "bold") 
        ).pack(pady=20)

        crear_subtitulo(self.scroll_container, "Río a Medir")

        self.prov = ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Provincia")
        self.prov.pack()

        self.ciudad = ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Ciudad")
        self.ciudad.pack()

        self.cuerpoAgua = ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Cuerpo de Agua")
        self.cuerpoAgua.pack()

        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container,"Fecha de la Medición")
        self.fechaMedicion = ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Fecha de Medición (DD/MM/AAAA HH:MM)")
        self.fechaMedicion.pack()
        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Valores Medidos")
        
        self.frame_parametros = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.frame_parametros.pack(pady=10)
        
        for i, p in enumerate(self.parametros):

            lbl = ctk.CTkLabel(
                self.frame_parametros,
                text=f'{p["nombreParametro"]} ({p["unidad"]})',
                anchor="w")
            
            lbl.grid(row=i, column=0, sticky="w", padx=(20,10), pady=4)

            e = ctk.CTkEntry(self.frame_parametros, width=120)
            e.grid(row=i, column=1, padx=(0,20), pady=4)

            self.inputs[p["id"]] = e

        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Observaciones a tener en cuenta")
        self.comments = ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Observaciones")
        self.comments.pack(pady=10)

        ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Guardar Medición", 
            width=250,
            command=self.guardar).pack(pady=10)
        
        ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text="Volver",
            width=250,
            command=on_back).pack()
            
    def guardar(self):
        if session.currentUser is None:
            print("Error: No user is currently logged in")
            return
    
        fecha = parse_fecha_str(self.fechaMedicion.get())

        valores = { pid: float(e.get()) for pid, e in self.inputs.items() if e.get()}

        idMed = guardarMedicionCompleta(
            self.prov.get(),
            self.ciudad.get(),
            self.cuerpoAgua.get(),
            fecha,
            session.currentUser.id,
            self.comments.get(),
            valores)

        self.on_back()
        messagebox.showinfo("Guardado Exitoso","✔ Medición Guardada Correctamente")
        