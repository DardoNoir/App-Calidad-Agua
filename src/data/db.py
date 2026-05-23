import psycopg2
import os
import sys

from dotenv import load_dotenv
from contextlib import contextmanager


def resource_path(relative_path):
    """
    Devuelve la ruta absoluta compatible
    con desarrollo y PyInstaller
    """

    if getattr(sys, 'frozen', False):
        # Ejecutable PyInstaller
        base_path = sys._MEIPASS
    else:
        # Proyecto en desarrollo
        base_path = os.path.dirname(
            os.path.dirname(
                os.path.dirname(__file__)
            )
        )

    return os.path.join(base_path, relative_path)


# Cargar variables de entorno
dotenv_path = resource_path(".env")

print("Cargando .env desde:", dotenv_path)

load_dotenv(dotenv_path)


@contextmanager
def connection():

    print("HOST:", os.getenv("DB_HOST"))

    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
        sslmode=os.getenv("DB_SSLMODE")
    )

    try:
        yield conn
        conn.commit()

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()