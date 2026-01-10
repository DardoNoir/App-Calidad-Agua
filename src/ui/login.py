import customtkinter as ctk
from tkinter import messagebox
from src.ui.session import currentUser, SesionUsuario
from src.data.repository import autenticarUsuario

class LoginWindow(ctk.CTkFrame):
    def __init__(self, master, on_login_success):
        super().__init__(master)
        self.on_login_success = on_login_success

        self.pack(expand=True)

        ctk.CTkLabel(self, text="Sistema Calidad del Agua", font=("Arial",20)).pack(pady=20)

        self.usuario_entry = ctk.CTkEntry(self, placeholder_text="Usuario")
        self.usuario_entry.pack(pady=5)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Contraseña", show = "*")
        self.password_entry.pack(pady=5)

        ctk.CTkButton(self, text= "Ingresar", command=self.login).pack(pady=15)

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

        global currentUser
        currentUser = SesionUsuario(
            id=data["id"],
            nombreUsuario=data["nombreUsuario"],
            rol=data["rol"]
        )

        self.on_login_success