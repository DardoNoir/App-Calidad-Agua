import customtkinter as ctk
from src.data.repository import (insertarParametro, existeParametro)
from src.ui.uiUtils import *
from tkinter import messagebox

class CargarParametro(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back=on_back

        ctk.CTkLabel(
            self,
            text=f"AgregarParámetro",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        crear_subtitulo(self, "Parámetro")
        self.codParam=ctk.CTkEntry(self, width=300, placeholder_text="Código del Parámetro...")
        self.codParam.pack(pady=10)

        self.nomParam=ctk.CTkEntry(self, width=300, placeholder_text="Nombre del Parámetro...")
        self.nomParam.pack(pady=10)
        
        self.uniParam=ctk.CTkEntry(self, width=300, placeholder_text="Unidad de Medida del Parámetro...")
        self.uniParam.pack(pady=10)

        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Guardar Parametro", 
            width=250,
            command=self.guardarParametro).pack(pady=10)
        
        ctk.CTkButton(
            self,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text="Volver",
            width=250,
            command=on_back).pack()
    
    def guardarParametro(self):
        nombreParametro=self.nomParam.get().strip()
        codigo=self.codParam.get().strip()
        unidad=self.uniParam.get().strip()

        if not nombreParametro or not codigo:
            messagebox.showerror("Error","Falta completar Nombre o Código del Parámetro")
            return
        
        if existeParametro(nombreParametro):
            messagebox.showinfo("Atención", "El Parámetro que se quiere crear, ya existe")

        insertarParametro(codigo, nombreParametro, unidad)
        self.on_back()
        messagebox.showinfo("Guardado Existos", "Parámetro agregado correctamente ✔")
        