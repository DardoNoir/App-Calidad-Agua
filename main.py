from src.data.migrations import run_migrations
from src.data.repository import crearUsuario

def bootstarp():
    run_migrations()
    #Crear admin de ejemplo
    try:
        idUsuario = crearUsuario("AAAAA", "67890", rol="Usuario")
        print("Usuario creado, id: ", idUsuario)
    except Exception as e:
        print("No se creó Usuario, posible duplicado: ", e)

if __name__ == "__main__":
    bootstarp()

