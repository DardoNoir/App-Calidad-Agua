import customtkinter as ctk
from src.data.repository import *
from src.ui.uiUtils import *
from tkinter import messagebox, ttk
from pathlib import Path
from src.reports.pdfReport import generarReporte
from src.reports.excelReport import generarExcelMediciones



class DescargarMediciones(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand = True)
        self.on_back = on_back

        self.lugares = traerLugares()

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
        cuerpoAgua = sorted(set(l["cuerpoAgua"]for l in self.lugares))

        self.combo_prov = ctk.CTkComboBox(filtro_frame, values= ["-"] + provincias, width= 150)
        self.combo_prov.grid(row = 0, column = 0, padx = 5)
        self.combo_ciud = ctk.CTkComboBox(filtro_frame, values= ["-"] + ciudades, width= 250)
        self.combo_ciud.grid(row = 0, column = 1, padx = 5)
        self.combo_CA = ctk.CTkComboBox(filtro_frame, values= ["-"] + cuerpoAgua, width= 150)
        self.combo_CA.grid(row = 0, column = 2, padx = 5)

        ctk.CTkButton(filtro_frame,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Buscar", 
            width=150,
            command=self.buscar_mediciones).grid(row=0, column=3, padx=10)
        
        crear_separador(self.scroll_container)

        crear_subtitulo(self.scroll_container, "Descargar medidas")

        tabla_frame = ctk.CTkFrame(self.scroll_container)
        tabla_frame.pack(fill = "both", expand = True, padx =10)

        columnas = ("id", "fecha", "usuario", "ica", "clasificacion", "obs", "cargada")

        self.tree = ttk.Treeview(tabla_frame, columns= columnas, show="headings", selectmode="extended")

        self.tree.heading("id", text="Nro")
        self.tree.heading("fecha", text="Fecha Medición")
        self.tree.heading("usuario", text="Tomada Por")
        self.tree.heading("ica", text="ICA")
        self.tree.heading("clasificacion", text="Clasificación")
        self.tree.heading("obs", text="Observaciones")
        self.tree.heading("cargada", text="Cargada en Sistema")

        self.tree.column("id",anchor="e", width=50)
        self.tree.column("fecha", anchor="w", width=130)
        self.tree.column("usuario", anchor="w", width=120)
        self.tree.column("ica", anchor="e", width=60)
        self.tree.column("clasificacion", anchor="w", width=120)
        self.tree.column("obs", anchor="w", width=200)
        self.tree.column("cargada", anchor="w", width=130)

        self.tree.pack(fill="both", expand=True)

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

        ctk.CTkLabel(self, 
            text="© 2026 Calidad del Agua", 
            font=("Segoe UI", 10),
            text_color="#888888").pack(side="bottom", pady=10)


    def normalizar(self, valor):
        return None if valor in ("", "-", None) else valor
    
    def buscar_mediciones(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        prov = self.normalizar(self.combo_prov.get())
        ciud = self.normalizar(self.combo_ciud.get())
        cuerpoAgua = self.normalizar(self.combo_CA.get())
        
        if (prov == None or ciud == None or cuerpoAgua == None):
            messagebox.showerror("Error", "Lugar no selecionado")
            return


        self.mediciones = traerMedicionesFiltradas(prov, ciud, cuerpoAgua)


        for m in self.mediciones: 
            self.tree.insert("", "end", values=(
                m["id"],
                m["fechaMedicion"],
                m["tomadaPor"],
                round(m["ica"], 2) if m["ica"] else "",
                m["clasificacionICA"] or "",
                m["comentarios"] or "",
                m["cargadaSistema"]
            ))
    
    def descargar_pdf(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showerror("Error", "No se ha seleccionado ninguna medición")
            return
        
        ruta = Path("reporte_prueba.pdf")
        id_medicion = int(self.tree.item(selected)["values"][0])

        generarReporte(
            idMedicion=id_medicion,
            rutaGuardar=ruta
        )

        messagebox.showinfo("Éxito", f"Reporte generado en: {ruta}")
    
    def descargar_excel(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showerror("Error", "No se han seleccionado Mediciones")

        ids = [int(self.tree.item(s)["values"][0]) for s in selected]

        ruta = Path("mediciones_exportadas.xlsx")

        generarExcelMediciones(
            idsMediciones=ids,
            rutaGuardar=ruta
        )

        messagebox.showinfo("Éxito", f"Excel generado en: {ruta}")
