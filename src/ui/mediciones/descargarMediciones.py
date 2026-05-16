import customtkinter as ctk
from src.data.repository import *
from src.ui import session
from src.ui.uiUtils import *
from tkinter import messagebox, ttk
from pathlib import Path
from src.reports.pdfReport import generarReporte
from src.reports.excelReport import generarExcelMediciones
from src.utils.datetime import format_fecha_display



class DescargarMediciones(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand = True)
        self.on_back = on_back

        self.selecciones = set()

        if session.currentUser is None:
            raise ValueError("No hay usuario autenticado")

        self.lugares = traerLugaresPorUsuario(session.currentUser.id)

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            self.scroll_container,
            text=f"Descargar Mediciones",
            font=("Segoe UI", 20, "bold") 
        ).pack(pady=20)

        crear_subtitulo(self.scroll_container, "Seleccionar lugar medido")

        filtro_frame = ctk.CTkFrame(self.scroll_container, fg_color= "transparent")
        filtro_frame.pack(pady=10)

        provincias = sorted(set(l["provincia"]for l in self.lugares))
        ciudades = sorted(set(l["ciudad"]for l in self.lugares))
        cuerpoAgua = sorted(set(l["cuerpo_agua"]for l in self.lugares))
        zonas = sorted(set(l["zona"] for l in self.lugares))

        self.combo_prov = ctk.CTkComboBox(filtro_frame, values= ["-"] + provincias, width= 150)
        self.combo_prov.grid(row = 0, column = 0, padx = 5)
        self.combo_ciud = ctk.CTkComboBox(filtro_frame, values= ["-"] + ciudades, width= 250)
        self.combo_ciud.grid(row = 0, column = 1, padx = 5)
        self.combo_CA = ctk.CTkComboBox(filtro_frame, values= ["-"] + cuerpoAgua, width= 150)
        self.combo_CA.grid(row = 0, column = 2, padx = 5)
        self.combo_zona = ctk.CTkComboBox(filtro_frame, values= ["-"] + zonas, width= 150)
        self.combo_zona.grid(row = 0, column = 3, padx = 5)

        ctk.CTkButton(filtro_frame,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Buscar", 
            width=150,
            command=self.buscar_mediciones).grid(row=0, column=4, padx=10)
        
        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Descargar medidas")

        tabla_frame = ctk.CTkFrame(self.scroll_container)
        tabla_frame.pack(fill = "both", expand = True, padx =10)

        columnas = ("id", "fecha", "usuario", "ica", "clasificacion", "obs", "cargada", "seleccion")

        self.tree = ttk.Treeview(tabla_frame, columns= columnas, show="headings", selectmode="extended")

        self.tree.heading("id", text="Nro")
        self.tree.heading("fecha", text="Fecha Medición")
        self.tree.heading("usuario", text="Tomada Por")
        self.tree.heading("ica", text="ICA")
        self.tree.heading("clasificacion", text="Clasificación")
        self.tree.heading("obs", text="Observaciones")
        self.tree.heading("cargada", text="Cargada en Sistema")
        self.tree.heading("seleccion", text="✔")


        self.tree.column("id",anchor="e", width=50)
        self.tree.column("fecha", anchor="w", width=130)
        self.tree.column("usuario", anchor="w", width=120)
        self.tree.column("ica", anchor="e", width=60)
        self.tree.column("clasificacion", anchor="w", width=120)
        self.tree.column("obs", anchor="w", width=200)
        self.tree.column("cargada", anchor="w", width=130)
        self.tree.column("seleccion", anchor="center", width=40)  

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<Button-1>", self.toggle_check)

        crear_separador(self.scroll_container)

        frame_botones = ctk.CTkFrame(self.master, fg_color="transparent")
        frame_botones.pack(pady=20)

        btn_descargarPdf = ctk.CTkButton(frame_botones,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Descargar Medición (PDF)",
            width=150,
            command=self.descargar_pdf)
        btn_descargarPdf.pack(side="left", padx=20)

        btn_descargarExcel = ctk.CTkButton(frame_botones,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Descargar Mediciones (Excel)",
            width=150,
            command=self.descargar_excel)
        btn_descargarExcel.pack(side="left", padx=20)

        btn_volver = ctk.CTkButton(frame_botones,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",                            
            text="Volver", 
            width=150,
            command=self.on_back)
        btn_volver.pack(side="left", padx=20)

        pie_pagina(self.scroll_container)


    def normalizar(self, valor):
        return None if valor in ("", "-", None) else valor
    
    def buscar_mediciones(self):
        user = session.currentUser    
        if user is None:
            raise ValueError("No hay usuarioa autenticado")
        
        for item in self.tree.get_children():
            self.tree.delete(item)

        prov = self.normalizar(self.combo_prov.get())
        ciud = self.normalizar(self.combo_ciud.get())
        cuerpoAgua = self.normalizar(self.combo_CA.get())
        zona = self.normalizar(self.combo_zona.get())
        
        if (prov == None or ciud == None or cuerpoAgua == None):
            messagebox.showerror("Error", "Lugar no selecionado")
            return


        self.mediciones = traerMedicionesFiltradas(user.id, prov, ciud, cuerpoAgua, zona)


        for m in self.mediciones: 
            self.tree.insert("", "end", values=(
                m["id"],
                format_fecha_display(m["fecha_medicion"]),
                m["tomada_por"] or "",
                round(m["ica"], 2) if m["ica"] else "",
                m["clasificacion_ica"] or "",
                m["comentarios"] or "",
                m["cargada_sistema"],
                "☐"
            ))
    
    def descargar_pdf(self):
        if not self.selecciones:
            messagebox.showerror("Error", "No se ha seleccionado ninguna medición")
            return
        
        if len(list(self.selecciones)) != 1:
            messagebox.showerror("Error", "Solo seleccionar una medición por reporte")
            return
        id_medicion = list(self.selecciones)[0]
        ruta = Path("Reporte de Medición.pdf")


        generarReporte(
            idMedicion=id_medicion,
            rutaGuardar=ruta
        )

        messagebox.showinfo("Éxito", f"Reporte generado en: {ruta}")
    
    def descargar_excel(self):
        if not self.selecciones:
            messagebox.showerror("Error", "No se han seleccionado Mediciones")

        ids = list(self.selecciones)

        ruta = Path("mediciones_exportadas.xlsx")

        generarExcelMediciones(
            idsMediciones=ids,
            rutaGuardar=ruta
        )

        messagebox.showinfo("Éxito", f"Excel generado en: {ruta}")

    
    def toggle_check(self, event):
        item = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if column != "#8":
            return

        if not item:
            return

        values = list(self.tree.item(item, "values"))
        id_medicion = values[0]  

        if id_medicion in self.selecciones:
            self.selecciones.remove(id_medicion)
            values[7] = "☐"  
        else:
            self.selecciones.add(id_medicion)
            values[7] = "✔"

        self.tree.item(item, values=values)