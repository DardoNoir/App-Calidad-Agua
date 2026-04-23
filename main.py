from src.data.repository import cargar_curvas_desde_db, crearUsuario
from src.ui.windows import App


def bootstarp():
    print("Conectando a Supabase...")

    try:
        crearUsuario("admin", "admin123", rol="Administrador")
    except:
        pass

    cargar_curvas_desde_db()

    app = App()
    app.mainloop()

if __name__ == "__main__":    
    bootstarp()