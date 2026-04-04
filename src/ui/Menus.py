import customtkinter as ctk
import src.ui.session as session
from src.ui.mediciones.mediciones import CargarMediciones
from src.ui.mediciones.historialMediciones import HistorialMediciones
from src.ui.mediciones.descargarMediciones import DescargarMediciones
from src.ui.uiUtils import pie_pagina
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.ui.windows import App

class MenuPrincipal(ctk.CTkFrame):   
    def __init__(self, master, on_logout, on_open_mediciones, on_usuarios, on_configuraciones):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        if session.currentUser is None:
            raise RuntimeError("Dashboard abierto sin usuario autenticado")

        user = session.currentUser

        ctk.CTkLabel(
            self, 
            text=f"Bienvenido {user.nombreUsuario} - {user.rol}",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=40)
        
        if user.rol == "Administrador":
            ctk.CTkButton(self, width=250, height=40,
                            text_color="#0c0000",
                            fg_color="#007BFF",
                            hover_color="#0fb300",
                            text="Gestión de Mediciones",
                            command=on_open_mediciones).pack(pady=8)

            ctk.CTkButton(self, width=250, height=40,
                            text_color="#0c0000",
                            fg_color="#007BFF",
                            hover_color="#0fb300",
                            text="Administrar Usuarios",
                            command=on_usuarios).pack(pady=8)

            ctk.CTkButton(self, width=250, height=40,
                            text_color="#0c0000",
                            fg_color="#007BFF",
                            hover_color="#0fb300",
                            text="Configuración",
                            command=on_configuraciones).pack(pady=8)

            ctk.CTkButton(self, width=250, height=40,
                            text_color="#ffffff",
                            fg_color="#FF0000",
                            hover_color="#f8b808",
                            text="Cerrar Sesión",
                            command=on_logout).pack(pady=(50,10))

            pie_pagina(self)

        else:
            on_open_mediciones()


class MenuMediciones(ctk.CTkFrame):   
    def __init__(self, master, on_back_principal, on_logout):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        if session.currentUser is None:
            raise RuntimeError("Menu de Mediciones abierto sin usuario autenticado")

        self.master: "App" = master
        self.on_back_principal = on_back_principal
        self.on_logout = on_logout

        user = session.currentUser

        ctk.CTkLabel(self,
            text=f"Menú de Mediciones - Usuario: {user.nombreUsuario} - {user.rol}",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=40)

        ctk.CTkButton(self, width=250, height=40,
                        text_color="#0c0000",
                        fg_color="#007BFF",
                        hover_color="#0fb300",
                        text="Cargar Medición",
                        command=self.abrir_cargar).pack(pady=8)

        ctk.CTkButton(self, width=250, height=40,
                        text_color="#0c0000",
                        fg_color="#007BFF",
                        hover_color="#0fb300",
                        text="Historial de Mediciones",
                        command=self.abrir_historial).pack(pady=8)

        ctk.CTkButton(self, width=250, height=40,
                        text_color="#0c0000",
                        fg_color="#007BFF",
                        hover_color="#0fb300",
                        text="Exportar Datos",
                        command=self.abrir_exportar).pack(pady=8)

        if user.rol == "Administrador":
            ctk.CTkButton(self, width=250, height=40,
                            text_color="#ffffff",
                            fg_color="#FF0000",
                            hover_color="#f8b808",
                            text="Volver al Menú Principal",
                            command=self.on_back_principal).pack(pady=20)
        else:
            ctk.CTkButton(self, width=250, height=40,
                            text_color="#ffffff",
                            fg_color="#FF0000",
                            hover_color="#f8b808",
                            text="Cerrar Sesión",
                            command=self.on_logout).pack(pady=20)

        pie_pagina(self)

    def volver_a_menu(self):
        self.master.clear()
        MenuMediciones(self.master, self.on_back_principal, self.on_logout)

    def abrir_cargar(self):
        self.master.clear()
        CargarMediciones(self.master, self.volver_a_menu)

    def abrir_historial(self):
        self.master.clear()
        HistorialMediciones(self.master, self.volver_a_menu)

    def abrir_exportar(self):
        self.master.clear()
        DescargarMediciones(self.master, self.volver_a_menu)