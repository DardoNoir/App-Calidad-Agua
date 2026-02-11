import customtkinter as ctk
from src.ui.login import LoginWindow
from src.ui.Menus import *
from src.ui.parametros.listaParamteros import ListaParametros

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.title("Calidad del Agua")
        self.geometry("800x500")
        self.show_login()

    def clear(self):
        for widget in self.winfo_children():
           widget.destroy()
           
    def show_login(self):
        self.clear()
        LoginWindow(self, self.show_dashboard)
    
    def show_dashboard(self):
        self.clear()
        MenuPrincipal(
            self, 
            on_logout=self.show_login, 
            on_open_mediciones=self.show_mediciones,
            on_usuarios=self.show_usuarios,
            on_configuraciones=self.show_configuraciones
        )
    
    def show_mediciones(self):
        self.clear()
        MenuMediciones(self,
                       on_back=self.show_dashboard,
                       on_logout=self.show_login)
        
    def show_usuarios(self):
        self.clear()
        MenuUsuarios(self,
                     on_back=self.show_dashboard)
        
    def show_configuraciones(self):
        self.clear()
        ListaParametros(
            self,
            on_back=self.show_dashboard
    )
        

