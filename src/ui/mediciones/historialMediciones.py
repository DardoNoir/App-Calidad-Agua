import customtkinter as ctk
from src.data.repository import *
from src.ui.uiUtils import *
from tkinter import messagebox, ttk
from src.ui.mediciones.detalleMedicion import DetalleMedicion

class HistorialMediciones(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand = True)
        self.on_back = on_back

        self.lugares = traerLugares()
        self.mediciones = []

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            self.scroll_container,
            text=f"Historial de Mediciones",
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
        self.combo_ciud = ctk.CTkComboBox(filtro_frame, values= ["-"] + ciudades, width= 150)
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

        crear_subtitulo(self.scroll_container, "Historial de medidas")

        tabla_frame = ctk.CTkFrame(self.scroll_container)
        tabla_frame.pack(fill = "both", expand = True, padx =10)

        columnas = ("id", "fecha", "usuario", "ica", "clasificacion", "obs", "cargada")

        self.tree = ttk.Treeview(tabla_frame, columns= columnas, show="headings")

        self.tree.heading("id", text="Nro")
        self.tree.heading("fecha", text="Fecha Medición")
        self.tree.heading("usuario", text="Tomada Por")
        self.tree.heading("ica", text="ICA")
        self.tree.heading("clasificacion", text="Clasificación")
        self.tree.heading("obs", text="Observaciones")
        self.tree.heading("cargada", text="Cargada en Sistema")

        self.tree.column("id", width=50)
        self.tree.column("fecha", width=130)
        self.tree.column("usuario", width=120)
        self.tree.column("ica", width=60)
        self.tree.column("clasificacion", width=120)
        self.tree.column("obs", width=200)
        self.tree.column("cargada", width=130)

        self.tree.pack(fill="both", expand=True)

        crear_separador(self.scroll_container)

        ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Ver detalle", 
            width=250,
            command=self.ver_detalle).pack(side="left", padx=10)
        
        ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            text="Volver",
            width=250,
            command=on_back).pack(side="left", padx=10)
        
        self.buscar_mediciones()
    
    def buscar_mediciones(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        prov = self.combo_prov.get() or None
        ciud = self.combo_ciud.get() or None
        cuerpoAgua = self.combo_CA.get or None

        self.mediciones = traerMedicionesFiltradas(prov, ciud, cuerpoAgua)

        for m in self.mediciones:
            self.tree.insert("", "end", values=(
                m["id"],
                m["fechaMedicion"],
                m["medidaTomadaPor"],
                round(m["ica"], 2) if m["ica"] else "",
                m["clasificacionICA"] or "",
                m["comentarios"] or "",
                m["cargadaSistema"]
            ))

    def ver_detalle(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atención", "Seleccione una medición")
            return
        
        item = self.tree.item(selected[0])
        id_medicion = item["values"][0]

        for widget in self.master.winfo_children():
            widget.destroy()
        DetalleMedicion(self.master, id_medicion, self.on_back)

        