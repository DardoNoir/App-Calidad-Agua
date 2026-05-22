import customtkinter as ctk
from tkinter import messagebox
from src.data.repository import *
from src.ui.uiUtils import *

class FormParametro(ctk.CTkFrame):
    def __init__(self, master, on_back, modo="alta", id_parametro=None):
        super().__init__(master)
        self.pack(fill="both", expand=True)

        self.on_back = on_back
        self.modo = modo
        self.id_parametro = id_parametro

        self.scroll_container = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

        titulo = "Agregar Parámetro" if modo == "alta" else "Modificar Parámetro"

        ctk.CTkLabel(
            self.scroll_container,
            text=titulo,
            font=("Segoe UI", 20, "bold")
        ).pack(pady=20)

        self.entries = {}
        self.puntos_entries = []

        # ==========================
        # DATOS
        # ==========================
        crear_subtitulo(self.scroll_container, "Datos del Parámetro")

        camposDatos = [
            ("codigo", "Código"),
            ("nombre_parametro", "Nombre del Parámetro"),
            ("unidad", "Unidad")
        ]

        for key, label in camposDatos:
            ctk.CTkLabel(self.scroll_container, text=label).pack(anchor="w", pady=(10, 0))
            entry = ctk.CTkEntry(self.scroll_container)
            entry.pack(fill="x", pady=5)
            self.entries[key] = entry

        crear_separador(self.scroll_container)

        # ==========================
        # REFERENCIA
        # ==========================
        crear_subtitulo(self.scroll_container, "Valores de Referencia")

        camposReferencia = [
            ("limite_min_aceptable", "Límite Mínimo Aceptable"),
            ("limite_max_aceptable", "Límite Máximo Aceptable"),
            ("limite_min_warning", "Límite Mínimo Crítico"),
            ("limite_max_warning", "Límite Máximo Crítico"),
            ("rango_posible_min", "Rango Posible Mínimo"),
            ("rango_posible_max", "Rango Posible Máximo"),
            ("normativa", "Normativa")
        ]

        for key, label in camposReferencia:
            ctk.CTkLabel(self.scroll_container, text=label).pack(anchor="w", pady=(10, 0))
            entry = ctk.CTkEntry(self.scroll_container)
            entry.pack(fill="x", pady=5)
            self.entries[key] = entry

        crear_separador(self.scroll_container)

        # ==========================
        # PONDERACIÓN
        # ==========================
        crear_subtitulo(self.scroll_container, "Ponderación")

        ctk.CTkLabel(self.scroll_container, text="Ponderación (0-1)").pack(anchor="w", pady=(10, 0))
        entry = ctk.CTkEntry(self.scroll_container)
        entry.pack(fill="x", pady=5)
        self.entries["ponderacion"] = entry

        crear_separador(self.scroll_container)

        # ==========================
        # CURVA SUBINDICE
        # ==========================
        crear_subtitulo(self.scroll_container, "Curva Subíndice (Valor - Subíndice)")

        self.frame_curva = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        self.frame_curva.pack(fill="x", pady=10)

        btn_agregar = ctk.CTkButton(
            self.scroll_container,
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            text="Agregar Punto",
            command=self.agregar_fila
        )
        btn_agregar.pack(pady=5)

        # Cargar datos si es edición
        if modo == "edicion" and id_parametro:
            self.cargar_datos()

        # ==========================
        # BOTONES
        # ==========================
        frame_botones = ctk.CTkFrame(self.scroll_container, fg_color="transparent")
        frame_botones.pack(pady=20)

        ctk.CTkButton(
            frame_botones,
            text="Guardar",
            height=40,
            text_color="#0c0000",
            fg_color="#007BFF",
            hover_color="#0fb300",
            width=140,
            command=self.guardar
        ).pack(side="left", padx=15)

        ctk.CTkButton(
            frame_botones,
            text="Volver",
            width=150,
            height=40,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            command=self.volver
        ).pack(side="left", padx=15)

    # ==========================================================
    # CURVA
    # ==========================================================
    def agregar_fila(self, valor="", subindice=""):
        fila = ctk.CTkFrame(self.frame_curva, fg_color="transparent")
        fila.pack(fill="x", pady=2)

        entry_valor = ctk.CTkEntry(fila, placeholder_text="Valor medido")
        entry_valor.pack(side="left", expand=True, fill="x", padx=5)
        entry_valor.insert(0, valor)

        entry_sub = ctk.CTkEntry(fila, placeholder_text="Subíndice")
        entry_sub.pack(side="left", expand=True, fill="x", padx=5)
        entry_sub.insert(0, subindice)

        btn_eliminar = ctk.CTkButton(
            fila,
            text="X",
            width=40,
            height=20,
            text_color="#ffffff",
            fg_color="#FF0000",
            hover_color="#f8b808",
            command=lambda: self.eliminar_fila(fila)
        )
        btn_eliminar.pack(side="left", padx=5)

        self.puntos_entries.append({"fila": fila, "valor": entry_valor, "subindice": entry_sub})

    def eliminar_fila(self, fila):
        self.puntos_entries = [e for e in self.puntos_entries if e["fila"] != fila]
        fila.destroy()

    # ==========================================================
    # CARGA DATOS
    # ==========================================================
    def cargar_datos(self):
        if not self.id_parametro:
            messagebox.showerror("Error", "ID inválido.")
            return

        id_param = int(self.id_parametro)

        p = traerParametroPorId(id_param) or {}
        r = traerValoresReferenciaPorParametro(id_param) or {}
        pond = traerPonderacionParametro(id_param) or {}
        curva = traerSubindices(id_param) or []

        self.entries["codigo"].insert(0, p["codigo"])
        self.entries["nombre_parametro"].insert(0, p["nombre_parametro"])
        self.entries["unidad"].insert(0, p["unidad"])
        self.entries["limite_min_aceptable"].insert(0, r.get("limite_min_aceptable", 0))
        self.entries["limite_max_aceptable"].insert(0, r.get("limite_max_aceptable", 0))
        self.entries["limite_min_warning"].insert(0, r.get("limite_min_warning", 0))
        self.entries["limite_max_warning"].insert(0, r.get("limite_max_warning", 0))
        self.entries["rango_posible_min"].insert(0, r.get("rango_posible_min", 0))
        self.entries["rango_posible_max"].insert(0, r.get("rango_posible_max", 0))
        self.entries["normativa"].insert(0, r.get("normativa", ""))
        self.entries["ponderacion"].insert(0, pond.get("ponderacion", 0))

        for punto in curva:
            if punto:
                self.agregar_fila(punto["valor"], punto["subindice"])

    # ==========================================================
    # GUARDAR
    # ==========================================================
    def guardar(self):
        datos = {k: e.get().strip() for k, e in self.entries.items()}

        if any(v == "" for v in datos.values()):
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            ponderacion = float(datos["ponderacion"])
            if not (0 <= ponderacion <= 1):
                raise ValueError()
        except:
            messagebox.showerror("Error", "Ponderación inválida.")
            return

        try:
            # ALTA
            if self.modo == "alta":
                id_param = insertarParametro(
                    datos["codigo"],
                    datos["nombre_parametro"],
                    datos["unidad"]
                )

                insertarValoresReferencia(
                    id_param,
                    float(datos["limite_max_aceptable"]),
                    float(datos["limite_max_warning"]),
                    float(datos["limite_min_aceptable"]),
                    float(datos["limite_min_warning"]),
                    datos["normativa"],
                    float(datos["rango_posible_min"]),
                    float(datos["rango_posible_max"])
                )

                insertarPonderacionParametro(id_param, ponderacion)

            # EDICION
            else:
                if not self.id_parametro:
                    messagebox.showerror("Error", "ID inválido.")
                    return

                id_param = int(self.id_parametro)

                actualizarParametro(
                    id_param,
                    datos["codigo"],
                    datos["nombre_parametro"],
                    datos["unidad"]
                )

                actualizarValoresReferencia(
                    id_param,
                    float(datos["limite_max_aceptable"]),
                    float(datos["limite_max_warning"]),
                    float(datos["limite_min_aceptable"]),
                    float(datos["limite_min_warning"]),
                    datos["normativa"],
                    float(datos["rango_posible_min"]),
                    float(datos["rango_posible_max"])
                )

                actualizarPonderacion(id_param, ponderacion)

            # GUARDAR CURVA
            puntos = []
            for punto in self.puntos_entries:
                valor = punto["valor"].get().strip()
                subindice = punto["subindice"].get().strip()

                if valor == "" or subindice == "":
                    messagebox.showerror("Error", "Todos los puntos de la curva deben tener valor y subíndice.")
                    return

                try:
                    valor_f = float(valor)
                    subindice_f = float(subindice)
                    puntos.append((valor_f, subindice_f))
                except:
                    messagebox.showerror("Error", "Valores de curva inválidos.")
                    return
                
            if len (puntos) < 2:
                messagebox.showerror("Error", "Se requieren al menos dos puntos para guardar la curva.")
                return
                
            puntos.sort(key=lambda x: x[0])  # Ordenar por valor medido
            guardarCurvas(id_param, puntos)

        except Exception as e:
            messagebox.showerror("Error BD", str(e))
            return

        messagebox.showinfo("Éxito", "Parámetro guardado correctamente.")
        self.volver()

    def volver(self):
        self.destroy()
        self.on_back()