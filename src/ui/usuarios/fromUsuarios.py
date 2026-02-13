import customtkinter as ctk
from tkinter import messagebox
from matplotlib import text
from src.data.repository import *
from src.ui.uiUtils import *

class FormUsuario(ctk.CTkFrame):
    def __init__(self, master, on_back, modo="alta", idUsuario=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_back = on_back
        self.modo = modo
        self.idUsuario = idUsuario

        self.usuarios = traerUsuarios()

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        titulo = "Crear Usuario" if modo == "alta" else "Modificar Usuario"

        ctk.CTkLabel(
            self.scroll_container,
            text=titulo,
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        self.entries = {}

        crear_subtitulo(self.scroll_container, "Datos del Usuario")
        ctk.CTkLabel(self.scroll_container, text="Nombre de Usuario", text_color= "black").pack(anchor="w", pady=(10, 0))
        self.entries["nombre"] = ctk.CTkEntry(self.scroll_container)
        self.entries["nombre"].pack(fill="x", pady=5)

        # Password (solo obligatoria en alta)
        ctk.CTkLabel(self.scroll_container, text="Contraseña").pack(anchor="w", pady=(10, 0))
        self.entries["password"] = ctk.CTkEntry(self.scroll_container, show="*")
        self.entries["password"].pack(fill="x", pady=5)

        # Rol
        ctk.CTkLabel(self.scroll_container, text="Rol").pack(anchor="w", pady=(10, 0))
        self.rol_combo = ctk.CTkOptionMenu(
            self.scroll_container,
            values=["Usuario", "Administrador"]
        )
        self.rol_combo.set("Usuario")
        self.rol_combo.pack(fill="x", pady=5)

        if modo == "edicion" and idUsuario:
            self.cargar_datos()

        crear_separador(self.scroll_container)

        frame_botones = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        frame_botones.pack(pady=20)

        ctk.CTkButton(
            frame_botones,
            text="Guardar",
            width=140,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            command=self.guardar
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            frame_botones,
            text="Volver",
            width=140,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            command=self.volver
        ).pack(side="left", padx=15)


    def cargar_datos(self):
        if self.idUsuario is None:
            return
        idUser = int(self.idUsuario) if isinstance (self.idUsuario, (int, str)) else 0
        usuario = traerUsuarioPorId(idUser)


        if not usuario:
            messagebox.showerror("Error", "Usuario no encontrado.")
            return

        self.entries["nombre"].insert(0, usuario["nombreUsuario"])
        self.entries["password"].insert(0, "")
        self.rol_combo.set(usuario["rol"])


    def guardar(self):
        nombre = self.entries["nombre"].get().strip()
        password = self.entries["password"].get().strip()
        rol = self.rol_combo.get().strip()


        if not nombre:
            messagebox.showerror("Error", "Nombre obligatorio.")
            return

        try:
            if self.modo == "alta":
                if existeUsuario(nombre):
                    messagebox.showerror("Error", "El usuario ya existe.")
                    return

                crearUsuario(nombre, password, rol)

            else:
                if self.modo == "edicion":
                    if password:
                        actualizarUsuario(self.idUsuario, nombre, hash_password(password), rol)
                else:
                    actualizarUsuarioSinPassword(self.idUsuario, nombre, rol)


        except Exception as e:
            messagebox.showerror("Error BD", str(e))
            return

        messagebox.showinfo("Éxito", "Usuario guardado correctamente.")
        self.volver()

    def volver(self):
        self.destroy()
        self.on_back()
