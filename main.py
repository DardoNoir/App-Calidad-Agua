from src.data.migrations import run_migrations
from src.ui.windows import App
from src.data.repository import crearUsuario, cargar_curvas_desde_db
from src.analysis.subindices import _CURVAS

def bootstarp():
    run_migrations()
    try:
        idUsuario = crearUsuario("aaaaa", "12345", rol="Administrador")
        print("Usuario creado, id: ", idUsuario)
    except Exception as e:
        print("No se creó Usuario, posible duplicado: ", e)
    
    cargar_curvas_desde_db()
    app = App()
    app.mainloop()

if __name__ == "__main__":
    bootstarp()

