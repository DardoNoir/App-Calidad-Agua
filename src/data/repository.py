from .db import connection
from src.utils.security import hash_password
from typing import Optional
from datetime import datetime

def crearUsuario(nombreUsuario: str, password: str, rol: str, db_path: Optional[str]=None):
    pw_hash = hash_password(password)
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuario (nombreUsuario, password, rol) VALUES (?, ?, ?)",
            (nombreUsuario, pw_hash, rol)
        )
        return cur.lastrowid
    

def TraerUsuarioPorNombre(nombreUsuario: str, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE nombreUsuario = ?", (nombreUsuario,))
        row = cur.fetchone()
        return dict(row) if row else None
    
def InsertarLugar(provincia: str, ciudad: str, cuerpoAgua:str, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        #Buscar si existe
        cur.execute("""
            SELECT id FROM lugar
            WHERE provincia=? AND ciudad=? AND cuerpoAgua=?
        """, (provincia, ciudad, cuerpoAgua))
        row = cur.fetchone()
        if row:
            return row["id"]
        cur.execute("""
            INSERT INTO lugar (provincia, ciudad, cuerpoAgua)
            VALUES (?, ?, ?)
        """,(provincia, ciudad, cuerpoAgua))
        return cur.lastrowid
    
def InsertarMedicion(idLugar: int, fechaMedicion: datetime, medidaTomadaPor: int, comentarios: str, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO medicion (idLugar, fechaMedicion, medidaTomadaPor, comentarios)
        VALUES (?, ?, ?, ?)
        """,(idLugar, fechaMedicion, medidaTomadaPor, comentarios))
        return cur.lastrowid