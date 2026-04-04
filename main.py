from src.data.migrations import run_migrations
from src.ui.windows import App
from src.data.repository import crearUsuario, cargar_curvas_desde_db
from src.analysis.subindices import _CURVAS
from src.data.db import DB_PATH

def bootstarp():

    print(f"Usando base de datos en: {DB_PATH}")
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
