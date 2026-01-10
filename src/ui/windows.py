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
        self.current_frame = LoginWindow(self, self.show_dashboard)
        self.current_frame.pack(fill="both", expand=True)

    def show_dashboard(self):
        print("Mostrando dashboard")
        self.clear()
        self.current_frame = Dashboard(self)
        self.current_frame.pack(fill="both", expand=True)
