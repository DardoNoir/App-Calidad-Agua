from src.data.migrations import run_migrations
from src.ui.windows import App
from src.data.repository import crearUsuario, cargar_curvas_desde_db
from src.analysis.subindices import _CURVAS

def bootstarp():
    run_migrations()
    try:
        crearUsuario("admin", "admin123", rol="Administrador")
    except:
        pass
    
    cargar_curvas_desde_db()
    app = App()
    app.mainloop()

if __name__ == "__main__":
    bootstarp()
