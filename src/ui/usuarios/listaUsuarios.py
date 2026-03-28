import customtkinter as ctk
from src.data.repository import *
from src.ui.uiUtils import *
from tkinter import messagebox, ttk
from src.ui.usuarios.fromUsuarios import FormUsuario
from src.utils.datetime import format_fecha_display

class ListaUsuarios(ctk.CTkFrame):
    def __init__(self, master, on_back):
        super().__init__(master)
        self.pack(fill="both", expand = True)
        self.on_back = on_back

        self.usuarios = traerUsuarios()

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        ctk.CTkLabel(
            self.scroll_container,
            text="Gestión de Usuarios",
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        crear_subtitulo(self.scroll_container, "Listado de Usuarios")
        tabla_frame = ctk.CTkFrame(self.scroll_container)
        tabla_frame.pack(fill="both", expand=False, padx=10)

        columnas = ("id", "nombre", "rol", "Ultima Conexión")
        self.tree = ttk.Treeview(tabla_frame, columns=columnas, show="headings")

        self.tree.heading("id", text="Nro")
        self.tree.heading("nombre", text="Nombre de Usuario")
        self.tree.heading("rol", text="Rol")
        self.tree.heading("Ultima Conexión", text="Última Conexión")

        self.tree.column("id", anchor="e", width=50,stretch=False)
        self.tree.column("nombre", anchor="w", width=200,stretch=False)
        self.tree.column("rol", anchor="w", width=150,stretch=False)
        self.tree.column("Ultima Conexión", anchor="w", width=200,stretch=False)

        scroll_x = ttk.Scrollbar(
            tabla_frame,
            orient="horizontal",
            command=self.tree.xview
        )
        self.tree.configure(xscrollcommand=scroll_x.set)
        scroll_x.pack(side="bottom", fill="x")

        self.tree.pack(fill="both", expand=True, padx=5, pady=5)

        for usuario in self.usuarios:
            ultima = usuario.get("ultimoInicio")
            if ultima:
                try:
                    ultima_formateada = format_fecha_display(ultima)
                except Exception as e:
                    print("Error formateando fecha:", e)
                    ultima_formateada = "N/A"
            else:
                ultima_formateada = "N/A"

            self.tree.insert("", "end", values=(
                usuario["id"],
                usuario["nombreUsuario"],
                usuario["rol"],
                ultima_formateada
            ))
 
        crear_separador(self.scroll_container)
        
        frame_botones = ctk.CTkFrame(self, fg_color="transparent")
        frame_botones.pack(pady=20)

        ctk.CTkButton(
            frame_botones,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
             hover_color="#0fb300",
             text="Crear Usuario", 
             width=150,
             command=self.irCrearUsuario
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            frame_botones,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Modificar Usuario", 
            width=150,
            command=self.modificarUsuario
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            frame_botones,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
             hover_color="#f8b808",
             text="Volver",
             width=150,
             command=on_back
        ).pack(side="left", padx=20)

        pie_pagina(self.scroll_container)

    
    def irCrearUsuario(self):
        self.pack_forget()
        FormUsuario(self.master, on_back=self.volver_a_lista,  modo="alta")

    def modificarUsuario(self):
        selected = self.tree.focus()
        if not selected:
            messagebox.showwarning("Selección requerida", "Por favor, seleccione un usuario para modificar.")
            return
        usuario_id = self.tree.item(selected)["values"][0]
        self.pack_forget()
        FormUsuario(self.master, on_back=self.volver_a_lista,  modo="edicion", idUsuario=usuario_id)
    
    def volver_a_lista(self):
        self.destroy()            
        ListaUsuarios(self.master, self.on_back)