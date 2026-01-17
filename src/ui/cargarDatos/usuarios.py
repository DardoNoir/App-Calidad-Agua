from typing import Any, Tuple
import customtkinter as ctk
from src.data.repository import (crearUsuario, existeUsuario)
from src.utils.security import hash_password
from src.ui.uiUtils import *
from tkinter import messagebox


class CargarUsuario(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back = on_back

        ctk.CTkLabel(
            self,
            text=f"Crear un Usuario",
            font=("Segoe UI", 20, "bold") 
        ).pack(pady=20)

        crear_subtitulo(self, "Nombre del Usuario")
        self.nombre=ctk.CTkEntry(self, width=300, placeholder_text="Nombre de Usuario...")
        self.nombre.pack(pady=10)
        crear_separador(self)

        crear_subtitulo(self, "Contraseña del Usuario")
        self.password=ctk.CTkEntry(self, width=300, placeholder_text="Contraseña...")
        self.password.pack(pady=10)
        crear_separador(self)

        crear_subtitulo(self,"Rol de Usuario")
        self.rol_combo=ctk.CTkOptionMenu(
            self,
            width=300,
            values=["Usuario", "Administrador"],
            fg_color="#3b3b3b",
            button_color="#555555"
        )
        self.rol_combo.set("Usuario")
        self.rol_combo.pack(pady=10)
        
        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Crear Usuario", 
            width=250,
            command=self.guardarUsuario).pack(pady=10)
        
        ctk.CTkButton(
            self,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text="Volver",
            width=250,
            command=on_back).pack()

    def guardarUsuario(self):
        nombre = self.nombre.get().strip()
        contra = self.password.get().strip()
        rol = self.rol_combo.get()

        if not nombre or not contra:
            messagebox.showerror("Error", "Faltan completar Usuario y/o Contraseña")
            return 
        
        if existeUsuario(nombre):
            messagebox.showinfo("Atención", "El Usuario ya existe")
            return
        
        crearUsuario(nombre, contra, rol)
        self.on_back()
        messagebox.showinfo("Guardado Exitoso","Usuario creado Correctamente ✔")
        