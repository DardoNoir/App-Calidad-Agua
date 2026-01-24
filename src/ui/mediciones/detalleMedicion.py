import customtkinter as ctk
from src.data.repository import *
from src.ui.uiUtils import *
from tkinter import messagebox


class DetalleMedicion(ctk.CTkFrame):
    def __init__(self, master, id_medicion, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back = on_back

        medicion = traerMedicionPorId(id_medicion)
        if medicion == None:
            messagebox.showerror("Error", "Medicion Inexistente")
            return


        lugar = traerLugarPorId(medicion["idLugar"])
        if lugar == None:
            messagebox.showerror("Error","Lugar Inexistente")
            return


        valores = traerValoresMedidosDeMedicion(id_medicion)
        usuario = traerUsuarioPorId(medicion["medidaTomadaPor"])
        if usuario == None:
            messagebox.showerror("Error", "Usuario Inexistente")
            return

        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        ctk.CTkLabel(scroll, text="Detalle de Medición", font=("Segoe UI", 20, "bold")).pack(pady=10)

        crear_subtitulo(scroll, "Lugar")

        ctk.CTkLabel(scroll, text=f"Provincia: {lugar['provincia']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"Ciudad: {lugar['ciudad']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"Cuerpo de Agua: {lugar['cuerpoAgua']}").pack(anchor="w", padx=60)

        crear_separador(scroll)

        crear_subtitulo(scroll, "Datos Generales")

        ctk.CTkLabel(scroll, text=f"Fecha Medición: {medicion['fechaMedicion']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"Tomada por: {usuario['nombreUsuario']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"ICA: {medicion['ica']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"Clasificación ICA: {medicion['clasificacionICA']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"Observaciones: {medicion['comentarios']}").pack(anchor="w", padx=60)

        crear_separador(scroll)

        crear_subtitulo(scroll, "Parámetros Medidos")

        frame_tabla = ctk.CTkFrame(scroll)
        frame_tabla.pack(padx=40, pady=10)

        headers = ["Parámetro", "Unidad", "Valor", "Estado", "Desviación"]
        for col, h in enumerate(headers):
            ctk.CTkLabel(frame_tabla, text=h, font=("Segoe UI", 12, "bold")).grid(row=0, column=col, padx=10, pady=5)

        for i, v in enumerate(valores, start=1):
            ctk.CTkLabel(frame_tabla, text=v["nombreParametro"]).grid(row=i, column=0, padx=10)
            ctk.CTkLabel(frame_tabla, text=v["unidad"]).grid(row=i, column=1, padx=10)
            ctk.CTkLabel(frame_tabla, text=v["valor"]).grid(row=i, column=2, padx=10)
            ctk.CTkLabel(frame_tabla, text=v["estado"]).grid(row=i, column=3, padx=10)
            ctk.CTkLabel(frame_tabla, text=v["desviacion"]).grid(row=i, column=4, padx=10)

        ctk.CTkButton(scroll, text="Volver", fg_color="#FF0000", command=self.on_back).pack(pady=20)
