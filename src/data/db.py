import sqlite3
from contextlib import contextmanager
from pathlib import Path
import sys
import os

def get_base_path():
    if getattr(sys, 'frozen', False):
        # Ejecutable (.exe)
        return Path(sys.executable).parent
    else:
        # Desarrollo (VS Code)
        return Path(__file__).resolve().parents[1]

# Ruta final de la DB
DB_PATH = get_base_path() / "app.db"

def get_connection(path: str | None = None):
    db_path = Path(path) if path else DB_PATH

    # Asegurar que el directorio exista
    os.makedirs(db_path.parent, exist_ok=True)

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def connection(path: str | None = None):
    conn = get_connection(path)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()