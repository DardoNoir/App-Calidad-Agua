from src.data.migrations import run_migrations
from src.ui.windows import App
from src.data.repository import crearUsuario

def bootstarp():
    run_migrations()
    try:
        idUsuario = crearUsuario("bbbbb", "12345", rol="Administrador")
        print("Usuario creado, id: ", idUsuario)
    except Exception as e:
        print("No se creó Usuario, posible duplicado: ", e)
    app = App()
    app.mainloop()

if __name__ == "__main__":
    bootstarp()

