import customtkinter as ctk
from tkinter import messagebox
import src.ui.session as session
from src.ui.session import SesionUsuario
from src.data.repository import autenticarUsuario
from src.ui.uiUtils import pie_pagina

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success
        self.pack(expand=True)

        ctk.CTkLabel(self, 
                     text="Sistema Calidad del Agua", 
                     font=("Segoe UI",22, "bold"),
                     text_color="#007BFF").pack(pady=30)

        self.usuario_entry = ctk.CTkEntry(self,width=150, placeholder_text="Usuario")
        self.usuario_entry.pack(pady=8)

        self.password_entry = ctk.CTkEntry(self,width=150, placeholder_text="Contraseña", show="*")
        self.password_entry.pack(pady=8)

        ctk.CTkButton(self, 
                      text="Ingresar", 
                      width=200,
                      height=40,
                      text_color="#0c0000",
                      fg_color="#007BFF",
                      hover_color="#00b300",
                      command=self.login).pack(pady=(20,5))

        ctk.CTkButton(self, 
                      text="Salir", 
                      width=200,
                      height=40,
                      text_color="#ffffff",
                      fg_color="#FF0000",
                      hover_color="#f8b808",
                      command=master.destroy).pack(pady=(5,10))

        pie_pagina(self)

    def login(self):
        usuario = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()

        if not usuario or not password:
            messagebox.showerror("Error", "Faltan completar Usuario y/o Contraseña")
            return

        data = autenticarUsuario(usuario, password)
        if not data:
            messagebox.showerror("Error", "Usuario y/o Contraseña Incorrectos")
            return
        
        session.currentUser = SesionUsuario(
            id=data["id"],
            nombreUsuario=data["nombre_usuario"],
            rol=data["rol"]
        )

        self.on_login_success()
