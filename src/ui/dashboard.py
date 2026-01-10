from typing import Any
import customtkinter as ctk
import src.ui.session as session
from src.ui.session import SesionUsuario

class Dashboard(ctk.CTkFrame):   
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        print("USUARIO:", session.currentUser)

        if session.currentUser is None:
            raise RuntimeError("Dashboard abierto sin usuario autenticado")

        user = session.currentUser

        ctk.CTkLabel(
            self, 
            text=f"Bienvenido {user.nombreUsuario} - ({user.rol})",
            font=("Arial", 16)
        ).pack(pady=10)
        
        self.buildMenu(user)

    def buildMenu(self, user: SesionUsuario):
        ctk.CTkButton(self, text="Cargar Medición").pack(pady=5)
        ctk.CTkButton(self, text="Historial").pack(pady=5)

        if user.rol == "Administrador":
            ctk.CTkButton(self, text="Importar Excel / CSV").pack(pady=5)
            ctk.CTkButton(self, text="Administrar Usuarios").pack(pady=5)
            ctk.CTkButton(self, text="Parámetros y Valores de Referencia").pack(pady=5)
