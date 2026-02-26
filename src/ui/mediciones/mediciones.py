import customtkinter as ctk
import src.ui.session as session
from src.data.repository import *
from datetime import datetime
from src.utils.datetime import parse_fecha_str
from src.ui.uiUtils import *
from tkinter import messagebox
from tkcalendar import DateEntry


class CargarMediciones(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.on_back = on_back

        self.parametros = traerParametros()
        self.lugares = traerLugares()

        self.provincias = sorted(set(l["provincia"] for l in self.lugares if l["provincia"]))
        self.ciudades = sorted(set(l["ciudad"] for l in self.lugares if l["ciudad"]))
        self.cuerpos = sorted(set(l["cuerpoAgua"] for l in self.lugares if l["cuerpoAgua"]))
        self.zonas = sorted(set(l["zona"] for l in self.lugares if l["zona"]))
        
        self.inputs = {}

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            self.scroll_container,
            text=f"Cargar Medición",
            font=("Segoe UI", 20, "bold") 
        ).pack(pady=20)

        crear_subtitulo(self.scroll_container, "Río a Medir")

        self.prov = ctk.CTkComboBox(self.scroll_container, values=self.provincias,
                                    width=300, height=30, corner_radius=5,
                                    button_color="#097eec", button_hover_color="#0fb300",
                                    dropdown_hover_color="#787978")
        self.prov.set("-")
        self.prov.pack(pady=3)

        self.ciudad = ctk.CTkComboBox(self.scroll_container, values=self.ciudades,
                                      width=300, height=30, corner_radius=5, 
                                      button_color="#097eec", button_hover_color="#0fb300",
                                      dropdown_hover_color="#787978")
        self.ciudad.set("-")
        self.ciudad.pack(pady=3)

        self.cuerpoAgua = ctk.CTkComboBox(self.scroll_container, values=self.cuerpos,
                                          width=300, height=30, corner_radius=5, 
                                          button_color="#097eec", button_hover_color="#0fb300",
                                          dropdown_hover_color="#787978")
        self.cuerpoAgua.set("-")
        self.cuerpoAgua.pack(pady=3)

        self.zona = ctk.CTkComboBox(self.scroll_container, values=self.zonas,
                                    width=300, height=30, corner_radius=5,
                                    button_color="#097eec", button_hover_color="#0fb300",
                                    dropdown_hover_color="#787978")
        self.zona.set("-")
        self.zona.pack(pady=3)

        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container,"Fecha de la Medición")
        self.frame_fecha = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.frame_fecha.pack(pady=5)

        self.fechaEntry = DateEntry(self.frame_fecha, date_pattern="dd/mm/yyyy" ,width=40, 
                                    background="#097eec", foreground="white", borderwidth=2)
        self.fechaEntry.pack(side = "left", padx=5)
        horas = [f"{h:02d}" for h in range(24)]
        minutos = [f"{m:02d}" for m in range(60)]

        self.horaCombo = ctk.CTkComboBox(self.frame_fecha, values=horas, width=80, height=30, corner_radius=5,
                                        button_color="#097eec", button_hover_color="#0fb300",
                                        dropdown_hover_color="#787978")
        self.horaCombo.set("hs")
        self.horaCombo.pack(side = "left", padx=5)

        self.minutoCombo = ctk.CTkComboBox(self.frame_fecha, values=minutos, width=80, height=30, corner_radius=5,
                                        button_color="#097eec", button_hover_color="#0fb300",
                                        dropdown_hover_color="#787978")
        self.minutoCombo.set("min")
        self.minutoCombo.pack(side = "left", padx=5)

        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Valores Medidos")
        
        self.frame_parametros = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.frame_parametros.pack(pady=10)
        
        for i, p in enumerate(self.parametros):

            lbl = ctk.CTkLabel(
                self.frame_parametros,
                text=f'{p["nombreParametro"]} ({p["unidad"]})',
                anchor="w")
            
            lbl.grid(row=i, column=0, sticky="w", padx=(20,10), pady=4)

            e = ctk.CTkEntry(self.frame_parametros, width=120)
            e.grid(row=i, column=1, padx=(0,20), pady=4)

            self.inputs[p["id"]] = e

        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Observaciones a tener en cuenta")
        self.comments = ctk.CTkEntry(self.scroll_container, width=300, placeholder_text="Observaciones")
        self.comments.pack(pady=10)

        ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Guardar Medición", 
            width=250,
            command=self.guardar).pack(pady=10)
        
        ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text="Volver",
            width=250,
            command=on_back).pack()

        pie_pagina(self.scroll_container)

            
    def guardar(self):
        if session.currentUser is None:
            print("Error: No user is currently logged in")
            return
        
        if self.prov.get() == "-" or self.ciudad.get() == "-" or self.cuerpoAgua.get() == "-" or self.zona.get() == "-":
            messagebox.showerror("Error en selección de lugar", "Por favor, seleccione o ingrese un Cuerpo de Agua válido.")
            return

        fechastr = self.fechaEntry.get()
        hora = self.horaCombo.get()
        minuto = self.minutoCombo.get()
        if hora == "hs" or minuto == "min":
            messagebox.showerror("Error en fecha y hora", "Por favor, seleccione una hora y minuto válidos.")
            return

        fechaCompletaStr = f"{fechastr} {hora}:{minuto}"
        fecha = parse_fecha_str(fechaCompletaStr)

        valores = {}
        errores = []

        for pid, entry in self.inputs.items():
            valor_str = entry.get().strip()

            if not valor_str:
                par = traerParametroPorId(pid)
                if par is not None:
                    errores.append(f"Valor vacío en parámetro: {par['nombreParametro']}")
                    continue

            try:
                valor = float(valor_str)
            except ValueError:
                par = traerParametroPorId(pid)
                if par is not None:
                    errores.append(f"Valor inválido en parámetro: {par['nombreParametro']}\n"
                                   f"Se esperaba un número.")
                    continue

            referencia = traerValoresReferenciaPorParametro(pid)

            if referencia:
                rango_min = referencia.get("rangoPosibleMin")
                rango_max = referencia.get("rangoPosibleMax")

                if rango_min is not None and valor < rango_min:
                    parametro = traerParametroPorId(pid)
                    if parametro is not None:
                        errores.append(
                            f"{parametro['nombreParametro']} fuera de rango.\n"
                            f"Rango posible: {rango_min} - {rango_max}"
                        )


                if rango_max is not None and valor > rango_max:
                    parametro = traerParametroPorId(pid)
                    if parametro is not None:
                        errores.append(
                            f"{parametro['nombreParametro']} fuera de rango.\n"
                            f"Rango posible: {rango_min} - {rango_max}"
                        )

            valores[pid] = valor

        if errores:
            messagebox.showerror(
                "Error en valores cargados",
                "\n\n".join(errores)
            )
            return

        idMed = guardarMedicionCompleta(
            self.prov.get(),
            self.ciudad.get(),
            self.cuerpoAgua.get(),
            fecha,
            session.currentUser.id,
            self.comments.get(),
            valores,
            self.zona.get()
        )

        self.on_back()
        messagebox.showinfo("Guardado Exitoso", "✔ Medición Guardada Correctamente")
    
        