from .db import connection
from src.utils.security import hash_password
from typing import Optional
from datetime import datetime
from src.analysis.evaluacion import ReferenciaParametro

# --- Manejo de usuarios ---
# Crear un usuario
def crearUsuario(nombreUsuario: str, password: str, rol: str, db_path: Optional[str]=None):
    pw_hash = hash_password(password)
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuario (nombreUsuario, password, rol) VALUES (?, ?, ?)",
            (nombreUsuario, pw_hash, rol)
        )
        return cur.lastrowid

# Traer lista de todos los usuarios
def traerUsuarios(db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombreUsuario, rol FROM usuario")
        return [dict(row) for row in cur.fetchall()]

# Traer los datos de un usuario por nombre    
def traerUsuarioPorNombre(nombreUsuario: str, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE nombreUsuario = ?", (nombreUsuario,))
        row = cur.fetchone()
        return dict(row) if row else None

# Traer los datos de un usuario por id
def traerUsuarioPorId(id: int, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT nombreUsuario FROM usuario WHERE id = ?", (id,))
        row = cur.fetchone()
        return dict(row) if row else None


# --- Manejo de lugares ---
# Agregar un lugar    
def insertarLugar(provincia: str, ciudad: str, cuerpoAgua: str, db_path: Optional[str] = None) -> int:
    with connection(db_path) as conn:
        cur = conn.cursor()
        # Verificar si existe
        cur.execute(
            """
            SELECT id FROM lugar
            WHERE provincia = ? AND ciudad = ? AND cuerpoAgua = ?
            """,
            (provincia, ciudad, cuerpoAgua)
        )
        row = cur.fetchone()
        # Si existe, devolvemos el ID garantizado como int
        if row is not None and row["id"] is not None:
            return int(row["id"])
        # Insertar nuevo
        cur.execute(
            """
            INSERT INTO lugar (provincia, ciudad, cuerpoAgua)
            VALUES (?, ?, ?)
            """,
            (provincia, ciudad, cuerpoAgua)
        )
        # cur.lastrowid NUNCA es None cuando hay INSERT, pero lo tipamos igual
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)

# Traer la lista de los lugares
def traerLugares(db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM lugar ORDER BY provincia, ciudad, cuerpoAgua")
        return [dict(row) for row in cur.fetchall()]
    
# Traer un lugar por id
def traerLugarPorId(idLugar: int, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM lugar WHERE id = ?", (idLugar,))
        row = cur.fetchone()
        return dict(row) if row else None


# --- Manejo de parametros ---
# Agregar un parametro
def insertarParametro(codigo: str,nombreParametro:str, unidad:str, db_path: Optional[str] = None) -> int:
     with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id FROM parametro
            WHERE codigo = ? AND nombreParametro = ? AND unidad = ?
            """,
            (codigo, nombreParametro, unidad)
        )
        row = cur.fetchone()
        
        if row is not None and row["id"] is not None:
            return int(row["id"])

        cur.execute("""
             INSERT INTO parametro (codigo, nombreParametro, unidad)
            VALUES (?, ?, ?)
            """,(codigo, nombreParametro, unidad))
        
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)

# Traer la lista de parametros
def traerParametros(db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM parametro")
        return [dict(row) for row in cur.fetchall()]

# Traer un parametro por id
def traerParametroPorId(idParametro: int, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM parametro WHERE id = ?", (idParametro,))
        row = cur.fetchone()
        return dict(row) if row else None


# --- Manejo de Mediciones ---
# Agregar una medicion
def insertarMedicion(idLugar: int, fechaMedicion: datetime, medidaTomadaPor: int, comentarios: str, db_path: Optional[str] = None) -> int:
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO medicion (idLugar, fechaMedicion, medidaTomadaPor, comentarios)
            VALUES (?, ?, ?, ?)
            """,
            (idLugar, fechaMedicion, medidaTomadaPor, comentarios)
        )
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("insertar_medicion: lastrowid fue None, algo salió mal.")
        return int(last_id)

# Traer una medicion por id
def traerMedicionPorId(idMedicion: int, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicion WHERE id = ?", (idMedicion,))
        row = cur.fetchone()
        return dict(row) if row else None

# Traer mediciones por Lugar
def traerMedicionesPorLugar(idLugar: int, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, fechaMedicion, comentarios FROM medicion WHERE idLugar = ?", (idLugar,))
        return [dict(row) for row in cur.fetchall()]

# Traer mediciones por Usuario
def traerMedicionesPorUsuario(idUsuario: int, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, fechaMedicion, comentarios FROM medicion WHERE medidaTomadaPor = ?", (idUsuario,))
        return [dict(row) for row in cur.fetchall()]

# Traer mediciones por Fecha
def traerMedicionesPorFecha(fechaMedicion: datetime, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, fechaMedicion, comentarios FROM medicion WHERE fechaMedicion = ?", (fechaMedicion,))
        return [dict(row) for row in cur.fetchall()]
    
# Traer mediciones por Lugar y Fecha
def traerMedicionesPorLugarYFecha(idLugar: int, fechaMedicion: datetime, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, fechaMedicion, comentarios FROM medicion WHERE idLugar = ? AND fechaMedicion = ?", (idLugar, fechaMedicion))
        return [dict(row) for row in cur.fetchall()]

# Traer todas las mediciones
def traerMediciones(db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicion")
        return [dict(row) for row in cur.fetchall()]

# Guardar el valor de una medición
def insertarValorMedido(idMedicion: int, idParametro: int, valor: float, estado: str, desviacion: str, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO valorMedida (idMedicion, idParametro, valor, estado, desviacion)
            VALUES (?, ?, ?, ?, ?)
        """, (idMedicion, idParametro, valor, estado, desviacion))
        return cur.lastrowid

# Traer los valores medidos de una medición
def traerValoresMedidosDeMedicion(idMedicion: int, db_path: Optional[str]=None):   
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT vm.idParametro, p.nombreParametro, p.unidad, vm.valor, vm.estado, vm.desviacion
            FROM valorMedida vm
            JOIN parametro p ON vm.idParametro = p.id
            WHERE vm.idMedicion = ?
        """, (idMedicion,))
        return [dict(row) for row in cur.fetchall()]

# Traer todos los valores medidos
def traerTodosLosValoresMedidos(db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT vm.idMedicion, vm.idParametro, p.nombreParametro, p.unidad, vm.valor, vm.estado, vm.desviacion
            FROM valorMedida vm
            JOIN parametro p ON vm.idParametro = p.id
        """)
        return [dict(row) for row in cur.fetchall()]


# --- Manejo de Valores de Referencia ---
# Agregar valores de referencia
def insertarValoresReferencia(idParametro: int, limiteMaxAceptable:float, limiteMaxWarning:float, db_path:Optional[str]=None) -> int:
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT id FROM valorReferencia
            WHERE idParametro = ?  
            """
        ,(idParametro,))
        row = cur.fetchone()
        
        if row is not None and row["id"] is not None:
            return int(row["id"])

        cur.execute(
            """
            INSERT INTO valorReferencia
            (idParametro, limiteMaxAceptable, limiteMaxWarning)
            VALUES(?, ?, ?)
            """,(idParametro, limiteMaxAceptable, limiteMaxWarning))
        
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)

# Traer los valores de referencia de un parametro
def traerValoresReferenciaPorParametro(idParametro: int, db_path: Optional[str] = None) -> Optional[ReferenciaParametro]:
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT limiteMaxAceptable, limiteMaxWarning FROM valorReferencia WHERE idParametro = ?",
            (idParametro,)
        )
        row = cur.fetchone()

        if row is None:
            return None

        return ReferenciaParametro(
            LimiteMax=row["limiteMaxAceptable"],
            LimiteWarning=row["limiteMaxWarning"]
        )

# Traer todos los valores de referencia
def traerTodosLosValoresReferencia(db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM valorReferencia")
        return [dict(row) for row in cur.fetchall()]

# Traer un valor de referencia por id
def traerValorReferenciaPorId(idValorReferencia: int, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM valorReferencia WHERE id = ?", (idValorReferencia,))
        row = cur.fetchone()
        return dict(row) if row else None


