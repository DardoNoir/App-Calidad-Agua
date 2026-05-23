import psycopg2
import os
import sys

from dotenv import load_dotenv
from contextlib import contextmanager


def resource_path(relative_path):
    """
    Obtiene la ruta absoluta al recurso,
    compatible con desarrollo y PyInstaller
    """

    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))

    return os.path.join(base_path, relative_path)


# Cargar .env
load_dotenv(resource_path(".env"))


@contextmanager
def connection():
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