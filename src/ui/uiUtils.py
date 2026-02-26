import customtkinter as ctk

def crear_subtitulo(contenedor, texto, padx=60):
    """Agrega un título de sección alineado a la izquierda."""
    lbl = ctk.CTkLabel(
        contenedor, 
        text=texto, 
        font=("Segoe UI", 16, "bold"),
        text_color="#555555",
        anchor="w"
    )
    lbl.pack(pady=(15, 5), padx=padx, fill="x")
    return lbl

def crear_separador(contenedor, padx=60):
    """Agrega una línea divisoria horizontal."""
    linea = ctk.CTkFrame(contenedor, height=2, fg_color="gray70")
    linea.pack(fill="x", padx=padx, pady=15)
    return linea

def pie_pagina(self):
    ctk.CTkLabel(self, 
                     text="© 2026 Calidad del Agua", 
                     font=("Segoe UI", 10),
                     text_color="#888888").pack(side="bottom", pady=10)