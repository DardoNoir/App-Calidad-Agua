import customtkinter as ctk
from src.data.repository import *
from src.ui.uiUtils import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from src.charts.datasource import traerSeriesParametroPorLugar
from src.charts.timeseries import graficarParametro
from typing import cast
from src.analysis.evaluacion import ReferenciaParametro
from src.utils.datetime import format_fecha_display


class DetalleMedicion(ctk.CTkFrame):
    def __init__(self, master, id_medicion, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back = on_back

        # ======================
        # Carga de datos
        # ======================
        self.medicion = traerMedicionPorId(id_medicion)
        if self.medicion is None:
            messagebox.showerror("Error", "Medición inexistente")
            self.on_back()
            return

        self.lugar = traerLugarPorId(self.medicion["idLugar"])
        if self.lugar is None:
            messagebox.showerror("Error", "Lugar inexistente")
            self.on_back()
            return

        self.usuario = traerUsuarioPorId(self.medicion["medidaTomadaPor"])
        if self.usuario is None:
            messagebox.showerror("Error", "Usuario inexistente")
            self.on_back()
            return

        self.valores = traerValoresMedidosDeMedicion(id_medicion)

        # ======================
        # Contenedor scroll
        # ======================
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True)

        # ======================
        # Título
        # ======================
        ctk.CTkLabel(
            scroll,
            text="Detalle de Medición",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=10)

        # ======================
        # Lugar
        # ======================
        crear_subtitulo(scroll, "Lugar")

        ctk.CTkLabel(scroll, text=f"Provincia: {self.lugar['provincia']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"Ciudad: {self.lugar['ciudad']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"Cuerpo de Agua: {self.lugar['cuerpoAgua']}").pack(anchor="w", padx=60)
        ctk.CTkLabel(scroll, text=f"Zona: {self.lugar['zona']}").pack(anchor="w", padx=60)
        
        crear_separador(scroll)

        # ======================
        # Datos Generales
        # ======================
        crear_subtitulo(scroll, "Datos Generales")

        ctk.CTkLabel(
            scroll,
            text=f"Fecha Medición: {format_fecha_display(self.medicion['fechaMedicion'])}"
        ).pack(anchor="w", padx=60)

        ctk.CTkLabel(
            scroll,
            text=f"Tomada por: {self.usuario['nombreUsuario']}"
        ).pack(anchor="w", padx=60)

        ctk.CTkLabel(
            scroll,
            text=f"ICA: {round(self.medicion['ica'], 2) if self.medicion['ica'] else '-'}"
        ).pack(anchor="w", padx=60)

        ctk.CTkLabel(
            scroll,
            text=f"Clasificación ICA: {self.medicion['clasificacionICA'] or '-'}"
        ).pack(anchor="w", padx=60)

        ctk.CTkLabel(
            scroll,
            text=f"Observaciones: {self.medicion['comentarios'] or '-'}"
        ).pack(anchor="w", padx=60)

        crear_separador(scroll)

        # ======================
        # Parámetros medidos
        # ======================
        crear_subtitulo(scroll, "Parámetros Medidos")

        frame_tabla = ctk.CTkFrame(scroll)
        frame_tabla.pack(padx=40, pady=10)

        headers = ["Parámetro", "Unidad", "Valor", "Estado", "Desviación", "Gráfico"]
        for col, h in enumerate(headers):
            ctk.CTkLabel(
                frame_tabla,
                text=h,
                font=("Segoe UI", 12, "bold")
            ).grid(row=0, column=col, padx=10, pady=5)

        for i, v in enumerate(self.valores, start=1):
            ctk.CTkLabel(frame_tabla, text=v["nombreParametro"]).grid(row=i, column=0, padx=10)
            ctk.CTkLabel(frame_tabla, text=v["unidad"]).grid(row=i, column=1, padx=10)
            ctk.CTkLabel(frame_tabla, text=v["valor"]).grid(row=i, column=2, padx=10)
            ctk.CTkLabel(frame_tabla, text=v["estado"]).grid(row=i, column=3, padx=10)
            ctk.CTkLabel(frame_tabla, text=v["desviacion"]).grid(row=i, column=4, padx=10)

            ctk.CTkButton(
                frame_tabla,
                text="📈",
                width=40,
                command=lambda p=v["idParametro"]: self.mostrar_grafico(p)
            ).grid(row=i, column=5, padx=5)

        # ======================
        # Botón volver
        # ======================
        ctk.CTkButton(
            scroll,
            text="Volver",
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            width=150,
            command=self.on_back
        ).pack(pady=20)

        pie_pagina(scroll)

    # =====================================================
    # Gráfico de parámetro
    # =====================================================
    def mostrar_grafico(self, id_parametro: int):
        try:
            if self.medicion is None:
                messagebox.showerror("Error", "Medición no disponible")
                return

            serie = traerSeriesParametroPorLugar(
                idLugar=self.medicion["idLugar"],
                idParametro=id_parametro
            )

            if not serie:
                messagebox.showinfo(
                    "Sin datos",
                    "No hay datos suficientes para graficar este parámetro."
                )
                return

            parametro = traerParametroPorId(id_parametro)
            if parametro is None:
                messagebox.showerror("Error", "Parámetro no encontrado")
                return
            referencia = traerValoresReferenciaPorParametro(id_parametro)
            ref = cast(ReferenciaParametro | None, referencia)

            graficarParametro(
                fechas=[s["fecha"] for s in serie],
                valores=[s["valor"] for s in serie],
                nombreParametro=parametro["nombreParametro"],
                unidad=parametro["unidad"],
                referencia=ref,
                titulo=f"– {self.lugar['cuerpoAgua'] if self.lugar is not None else '-'}"
            )

            plt.show()

        except Exception as e:
            messagebox.showerror(
                "Error",
                f"No se pudo generar el gráfico:\n{e}"
            )
