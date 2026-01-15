import customtkinter as ctk
import src.ui.session as session
from src.data.repository import *
from datetime import datetime
from src.utils.datetime import parse_fecha_str

class CargarMediciones(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back = on_back

        self.parametros = traerParametros()
        self.inputs = {}

        ctk.CTkLabel(
            self,
            text=f"Cargar Medición",
            font=("Segoe UI", 20, "bold") 
        ).pack(pady=20)

        self.prov = ctk.CTkEntry(self, width=300, placeholder_text="Provincia")
        self.prov.pack()

        self.ciudad = ctk.CTkEntry(self, width=300, placeholder_text="Ciudad")
        self.ciudad.pack()

        self.cuerpoAgua = ctk.CTkEntry(self, width=300, placeholder_text="Cuerpo de Agua")
        self.cuerpoAgua.pack()

        self.fechaMedicion = ctk.CTkEntry(self, width=300, placeholder_text="Fecha de Medición (DD/MM/AAAA HH:MM)")
        self.fechaMedicion.pack()


        self.frame_parametros = ctk.CTkFrame(self)
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


        self.comments = ctk.CTkEntry(self, width=300, placeholder_text="Observaciones")
        self.comments.pack(pady=10)

        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Guardar Medición", 
            width=250,
            command=self.guardar).pack(pady=10)
        
        ctk.CTkButton(
            self,
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

        popup = ctk.CTkToplevel(self)
        popup.title("Medición guardada")
        popup.geometry("300x150")
        popup.resizable(False, False)
        popup.grab_set() 

        ctk.CTkLabel(
        popup,
        text="✔ Medición guardada correctamente",
        text_color="green",
        font=("Segoe UI", 14, "bold")).pack(pady=25)

        def cerrar():
            popup.destroy()
            self.on_back()

        ctk.CTkButton(
            popup,
            text="Aceptar",                
            fg_color="#007BFF",
            command=cerrar).pack()