from src.data.db import connection
from psycopg2.extras import RealDictCursor

from src.analysis.subindices import(
    registrar_curva,
    existe_curva,
    eliminar_curva
)

def getCursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)

def cargar_curva(id_parametro: int):
    with connection() as conn:
        cur = getCursor(conn)

        cur.execute(
            """
            SELECT valor, subindice
            FROM curva_subindice
            WHERE id_parametro = %s
            ORDER BY valor
            """, (id_parametro,))
        
        puntos = cur.fetchall()

    if len(puntos) < 2:
        eliminar_curva(id_parametro)
        raise ValueError(f"El parámetro {id_parametro}")
    
    lista_puntos = [(pt["valor"], pt["subindice"]) for pt in puntos]

    registrar_curva(id_parametro, lista_puntos)

def asegurar_curva_cargada(id_parametro: int):
    if not existe_curva(id_parametro):
        cargar_curva(id_parametro)

def invalidar_curva(id_parametro: int):
    eliminar_curva(id_parametro)

def recargar_curva(id_parametro: int):
    invalidar_curva(id_parametro)
    cargar_curva(id_parametro)