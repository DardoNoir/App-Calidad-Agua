import customtkinter as ctk
import src.ui.session as session
from src.ui.mediciones.mediciones import CargarMediciones
from src.ui.usuarios.usuarios import CargarUsuario
from src.ui.mediciones.historialMediciones import HistorialMediciones
from src.ui.mediciones.descargarMediciones import DescargarMediciones
from src.ui.parametros.listaParamteros import ListaParametros


class MenuPrincipal(ctk.CTkFrame):   
    def __init__(self, master, on_logout, on_open_mediciones, on_usuarios, on_configuraciones):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_logout = on_logout
        self.on_open_mediciones = on_open_mediciones
        self.on_usuarios = on_usuarios
        self.on_configuraciones = on_configuraciones

        if session.currentUser is None:
            raise RuntimeError("Dashboard abierto sin usuario autenticado")

        user = session.currentUser

        ctk.CTkLabel(
            self, 
            text=f"Bienvenido {user.nombreUsuario} - {user.rol}",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=40)
        
        if user.rol == "Administrador":
            ctk.CTkButton(self,width=250, 
                        height=40,
                        text_color="#0c0000",
                        fg_color="#007BFF",
                        hover_color="#0fb300",
                        text="Gestión de Mediciones",
                        command=self.on_open_mediciones).pack(pady=8)
            ctk.CTkButton(self, width=250,
                        height=40, 
                        text_color="#0c0000",
                        fg_color="#007BFF",
                        hover_color="#0fb300",
                        text="Administrar Usuarios",
                        command=self.on_usuarios).pack(pady=8)
            ctk.CTkButton(self, width=250, 
                        height=40,
                        text_color="#0c0000",
                        fg_color="#007BFF",
                        hover_color="#0fb300", 
                        text="Configuración",
                        command=self.on_configuraciones).pack(pady=8)
            ctk.CTkButton(self, width=250, 
                        height=40,
                        text_color="#ffffff",
                        fg_color="#FF0000",
                        hover_color="#f8b808",
                        text="Cerrar Sesión",
                        command=self.on_logout
                        ).pack(pady=(50,10))
            ctk.CTkLabel(self, 
            text="© 2026 Calidad del Agua", 
            font=("Segoe UI", 10),
            text_color="#888888").pack(side="bottom", pady=10)

        else:
            self.on_open_mediciones()

class MenuUsuarios(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        if session.currentUser is None:
            raise RuntimeError("Menu de Usuarios abierto sin usuario autenticado")
        
        user = session.currentUser

        ctk.CTkLabel(self,
                        text=f"Menú de Usuarios - Usuario: {user.nombreUsuario} - Rol: {user.rol}",
                        font=("Segoe UI", 20, "bold")
                        ).pack(pady=40)
        
        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Agregar Usuario", 
            width=250,
            command=lambda: master.clear() or CargarUsuario(master, on_back)).pack(pady=8)
        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Gestión del Usuario", width=250).pack(pady=8)
        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Movimientos del Usuario", width=250).pack(pady=8)
        ctk.CTkButton(
                self,
                height=40,
                text_color="#ffffff",
                fg_color="#FF0000",
                hover_color="#f8b808",
                text="Volver al Menú Principal",
                width=250,
                command=on_back
            ).pack(pady=20)
        ctk.CTkLabel(self, 
        text="© 2026 Calidad del Agua", 
        font=("Segoe UI", 10),            
        text_color="#888888").pack(side="bottom", pady=10)
      
class MenuMediciones(ctk.CTkFrame):   
    def __init__(self, master, on_back, on_logout):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        if session.currentUser is None:
            raise RuntimeError("Menu de Mediciones abierto sin usuario autenticado")

        user = session.currentUser

        ctk.CTkLabel(self,
                        text=f"Menú de Mediciones - Usuario: {user.nombreUsuario} - {user.rol}",
                        font=("Segoe UI", 20, "bold")
                        ).pack(pady=40)
        
        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Cargar Medición", 
            width=250,
            command=lambda: master.clear() or CargarMediciones(master, on_back)).pack(pady=8)
        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Historial de Mediciones", 
            width=250,
            command=lambda: master.clear() or HistorialMediciones(master, on_back)).pack(pady=8)
        ctk.CTkButton(
            self,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Exportar Datos", 
            width=250,
            command=lambda: master.clear() or DescargarMediciones(master, on_back)).pack(pady=8)

        if user.rol == "Administrador":
            ctk.CTkButton(
                self,
                height=40,
                text_color="#ffffff",
                fg_color="#FF0000",
                hover_color="#f8b808",
                text="Volver al Menú Principal",
                width=250,
                command=on_back
            ).pack(pady=20)
        else:
            ctk.CTkButton(
                self,
                text="Cerrar Sesión",
                width=250,
                text_color="#0c0000",
                fg_color="#FF0000",
                hover_color="#f8b808",
                command=on_logout
            ).pack(pady=20)

        ctk.CTkLabel(self, 
        text="© 2026 Calidad del Agua", 
        font=("Segoe UI", 10),
        text_color="#888888").pack(side="bottom", pady=10)

