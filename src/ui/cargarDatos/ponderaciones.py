import customtkinter as ctk
from tkinter import messagebox

from src.data.repository import (
    traerParametros,
    traerPonderacionParametro,
    traerPonderacionesParametroActivas,
    insertarPonderacionParametro
)
from src.ui.uiUtils import *


class CargarPonderaciones(ctk.CTkFrame):

    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back = on_back

        # ================= DATOS =================
        self.parametros = traerParametros()
        self.parametro_por_nombre = {
            p["nombreParametro"]: p["id"]
            for p in self.parametros
        }

        # ================= UI =================
        ctk.CTkLabel(
            self,
            text="Cargar Ponderaciones",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        crear_subtitulo(self, "Selección de Parámetro")

        self.combo = ctk.CTkOptionMenu(
            self,
            width=300,
            values=list(self.parametro_por_nombre.keys()),
            command=self.on_parametro_seleccionado
        )
        self.combo.set("Seleccione un Parámetro")
        self.combo.pack(pady=10)

        crear_separador(self)

        self.ponderacion_frame = None

    # =====================================================
    # EVENTO: selección de parámetro
    # =====================================================
    def on_parametro_seleccionado(self, nombre):

        if self.ponderacion_frame:
            self.ponderacion_frame.destroy()

        self.ponderacion_frame = ctk.CTkFrame(self)
        self.ponderacion_frame.pack(pady=20)

        self.idParametro = self.parametro_por_nombre[nombre]
        ponderacion_anterior = traerPonderacionParametro(self.idParametro)

        crear_subtitulo(self.ponderacion_frame, "Cargar Ponderación")

        if ponderacion_anterior:
            crear_subtitulo(
                self.ponderacion_frame,
                f"Ponderación anterior: {ponderacion_anterior['ponderacion']}"
            )
            volver_habilitado = True
        else:
            crear_subtitulo(
                self.ponderacion_frame,
                "No cuenta con ponderación anterior"
            )
            volver_habilitado = False

        self.entrada = ctk.CTkEntry(
            self.ponderacion_frame,
            width=300,
            placeholder_text="Nueva Ponderación..."
        )
        self.entrada.pack(pady=10)

        # ================= BOTONES =================

        self.btn_guardar = ctk.CTkButton(
            self.ponderacion_frame,
            width=250,
            height=40,
            text="Guardar Ponderación",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text_color="#0c0000",
            command=self.guardar
        )
        self.btn_guardar.pack(pady=(10, 5))

        self.btn_volver = ctk.CTkButton(
            self.ponderacion_frame,
            width=250,
            height=40,
            text="Volver",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text_color="#ffffff",
            state="normal" if volver_habilitado else "disabled",
            command=self.on_back
        )
        self.btn_volver.pack()

    # =====================================================
    # GUARDAR PONDERACIÓN
    # =====================================================
    def guardar(self):

        try:
            nueva = float(self.entrada.get())
        except ValueError:
            messagebox.showerror("Error", "Ingrese un número válido")
            return

        if not 0 <= nueva <= 1:
            messagebox.showerror("Error", "La ponderación debe estar entre 0 y 1")
            return

        actuales = traerPonderacionesParametroActivas()

        suma = 0
        reemplaza = False

        for p in actuales:
            if p["idParametro"] == self.idParametro:
                suma += nueva
                reemplaza = True
            else:
                suma += p["ponderacion"]

        if not reemplaza:
            suma += nueva

        insertarPonderacionParametro(self.idParametro, nueva)

        suma = round(suma, 2)

        if suma == 1:
            self.btn_volver.configure(state="normal")
            messagebox.showinfo("OK", "Ponderaciones completas ✔")
        else:
            messagebox.showinfo(
                "Atención",
                f"Suma actual: {suma}\nDebe ser 1 para poder salir."
            )
