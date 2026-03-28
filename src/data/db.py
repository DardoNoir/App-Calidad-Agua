import sqlite3
from contextlib import contextmanager
from pathlib import Path

# Ruta absoluta al archivo de base de datos SQLite (app.db en la raíz del proyecto)
DB_PATH = Path(__file__).resolve().parents[1] / "app.db"

def get_connection(path: str | None = None):
    path = path or str(DB_PATH)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def connection(path : str | None = None):
    conn = get_connection(path)
    try:
        yield conn
        conn.commit()  # Guarda cambios si todo salió bien
    except:
        conn.rollback()  # Revierte cambios en caso de error
        raise
    finally:
        conn.close()  # Cierra conexión siempre
