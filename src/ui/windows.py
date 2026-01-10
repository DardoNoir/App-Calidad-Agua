import customtkinter as ctk
from src.ui.login import LoginWindow
from src.ui.dashboard import Dashboard

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Calidad del Agua")
        self.geometry("600x500")
        self.show_login()

    def clear(self):
        for widget in self.winfo_children():
           widget.destroy()
           
    def show_login(self):
        self.clear()
        LoginWindow(self, self.show_dashboard)
    
    def show_dashboard(self):
        self.clear()
        Dashboard(self)
