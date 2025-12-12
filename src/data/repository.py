from .db import connection
from src.utils.security import hash_password
from typing import Optional
from datetime import datetime
from src.analysis.evaluacion import ReferenciaParametro

# ============================================================
#                 MANEJO DE USUARIOS
# ============================================================

def crearUsuario(nombreUsuario: str, password: str, rol: str, db_path: Optional[str]=None):
    """
    Crea un nuevo usuario en la base de datos.
    - Recibe nombreUsuario, password y rol ('Administrador' o 'Usuario')
    - Hashea la contraseña antes de guardarla
    - Devuelve el ID del usuario creado
    """
    pw_hash = hash_password(password)  # Se transforma la contraseña en un hash seguro
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO usuario (nombreUsuario, password, rol) VALUES (?, ?, ?)",
            (nombreUsuario, pw_hash, rol)
        )
        return cur.lastrowid  # ID del usuario recién creado


def traerUsuarios(db_path: Optional[str]=None):
    """
    Devuelve una lista con todos los usuarios del sistema.
    Cada usuario se devuelve como un diccionario {'id':..., 'nombreUsuario':..., 'rol':...}
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, nombreUsuario, rol FROM usuario")
        return [dict(row) for row in cur.fetchall()]  # Convierte filas a dict


def traerUsuarioPorNombre(nombreUsuario: str, db_path: Optional[str]=None):
    """
    Trae todos los datos de un usuario buscado por su nombre.
    Devuelve un dict o None si no existe.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario WHERE nombreUsuario = ?", (nombreUsuario,))
        row = cur.fetchone()
        return dict(row) if row else None


def traerUsuarioPorId(id: int, db_path: Optional[str]=None):
    """
    Devuelve el usuario cuyo id coincide.
    Solo trae el nombre del usuario.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT nombreUsuario FROM usuario WHERE id = ?", (id,))
        row = cur.fetchone()
        return dict(row) if row else None


# ============================================================
#               MANEJO DE LUGARES
# ============================================================

def insertarLugar(provincia: str, ciudad: str, cuerpoAgua: str, db_path: Optional[str] = None) -> int:
    """
    Inserta un nuevo lugar en la tabla 'lugar'.
    - Si el lugar (provincia, ciudad, cuerpoAgua) ya existe → devuelve su ID
    - Si no existe → lo crea y devuelve el nuevo ID
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        
        # Verifica si ya existe
        cur.execute("""
            SELECT id FROM lugar
            WHERE provincia = ? AND ciudad = ? AND cuerpoAgua = ?
        """, (provincia, ciudad, cuerpoAgua))

        row = cur.fetchone()
        if row is not None:
            return int(row["id"])  # Si existe devuelve el ID
        
        # Si no existe, lo inserta
        cur.execute("""
            INSERT INTO lugar (provincia, ciudad, cuerpoAgua)
            VALUES (?, ?, ?)
        """, (provincia, ciudad, cuerpoAgua))

         # cur.lastrowid NUNCA es None cuando hay INSERT, pero lo tipamos igual
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)


def traerLugares(db_path: Optional[str]=None):
    """
    Devuelve todos los lugares ordenados por provincia, ciudad y cuerpo de agua.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM lugar ORDER BY provincia, ciudad, cuerpoAgua")
        return [dict(row) for row in cur.fetchall()]


def traerLugarPorId(idLugar: int, db_path: Optional[str]=None):
    """
    Devuelve un lugar según su ID, o None si no existe.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM lugar WHERE id = ?", (idLugar,))
        row = cur.fetchone()
        return dict(row) if row else None


# ============================================================
#               MANEJO DE PARÁMETROS
# ============================================================

def insertarParametro(codigo: str, nombreParametro: str, unidad: str, db_path: Optional[str] = None) -> int:
    """
    Inserta un nuevo parámetro (ej: pH, Turbiedad, DBO, etc.)
    - Si ya existe con ese código/nombre/unidad → devuelve su ID
    - Si no existe → lo crea
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id FROM parametro
            WHERE codigo = ? AND nombreParametro = ? AND unidad = ?
        """, (codigo, nombreParametro, unidad))

        row = cur.fetchone()
        if row is not None:
            return int(row["id"])

        # Insertar nuevo parámetro
        cur.execute("""
            INSERT INTO parametro (codigo, nombreParametro, unidad)
            VALUES (?, ?, ?)
        """, (codigo, nombreParametro, unidad))

         # cur.lastrowid NUNCA es None cuando hay INSERT, pero lo tipamos igual
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)


def traerParametros(db_path: Optional[str]=None):
    """
    Devuelve la lista completa de parámetros registrados.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM parametro")
        return [dict(row) for row in cur.fetchall()]


def traerParametroPorId(idParametro: int, db_path: Optional[str]=None):
    """
    Devuelve un parámetro según su ID.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM parametro WHERE id = ?", (idParametro,))
        row = cur.fetchone()
        return dict(row) if row else None


# ============================================================
#               MANEJO DE MEDICIONES
# ============================================================

def insertarMedicion(idLugar: int, fechaMedicion: datetime, medidaTomadaPor: int, comentarios: str, db_path: Optional[str] = None) -> int:
    """
    Inserta una nueva medición realizada en un lugar.
    - idLugar: lugar donde se tomó
    - fechaMedicion
    - medidaTomadaPor: ID del usuario
    - comentarios: texto libre del operador
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO medicion (idLugar, fechaMedicion, medidaTomadaPor, comentarios)
            VALUES (?, ?, ?, ?)
        """, (idLugar, fechaMedicion, medidaTomadaPor, comentarios))

         # cur.lastrowid NUNCA es None cuando hay INSERT, pero lo tipamos igual
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)


def traerMedicionPorId(idMedicion: int, db_path: Optional[str]=None):
    """
    Trae una medición por su ID.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicion WHERE id = ?", (idMedicion,))
        row = cur.fetchone()
        return dict(row) if row else None


def traerMedicionesPorLugar(idLugar: int, db_path: Optional[str]=None):
    """
    Devuelve todas las mediciones tomadas en un lugar específico.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, fechaMedicion, comentarios
            FROM medicion
            WHERE idLugar = ?
        """, (idLugar,))
        return [dict(row) for row in cur.fetchall()]


def traerMedicionesPorUsuario(idUsuario: int, db_path: Optional[str]=None):
    """
    Devuelve las mediciones cargadas por un usuario.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, fechaMedicion, comentarios
            FROM medicion
            WHERE medidaTomadaPor = ?
        """, (idUsuario,))
        return [dict(row) for row in cur.fetchall()]


def traerMedicionesPorFecha(fechaMedicion: datetime, db_path: Optional[str]=None):
    """
    Devuelve las mediciones tomadas en una fecha exacta.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, fechaMedicion, comentarios
            FROM medicion
            WHERE fechaMedicion = ?
        """, (fechaMedicion,))
        return [dict(row) for row in cur.fetchall()]


def traerMedicionesPorLugarYFecha(idLugar: int, fechaMedicion: datetime, db_path: Optional[str]=None):
    """
    Devuelve las mediciones tomadas en un lugar y fecha específicos.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, fechaMedicion, comentarios
            FROM medicion
            WHERE idLugar = ? AND fechaMedicion = ?
        """, (idLugar, fechaMedicion))
        return [dict(row) for row in cur.fetchall()]


def traerMediciones(db_path: Optional[str]=None):
    """
    Devuelve todas las mediciones existentes.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM medicion")
        return [dict(row) for row in cur.fetchall()]


# ---------- Valores puntuales medidos en cada medición -------------

def insertarValorMedido(idMedicion: int, idParametro: int, valor: float, estado: str, desviacion: str, db_path: Optional[str]=None):
    """
    Inserta un valor medido para una medición:
    Ejemplo:
        idMedicion = 12   (medición del día)
        idParametro = 3   (pH)
        valor = 8.2
        estado = "Warning"
        desviacion = "Valor supera el warning..."
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO valorMedida (idMedicion, idParametro, valor, estado, desviacion)
            VALUES (?, ?, ?, ?, ?)
        """, (idMedicion, idParametro, valor, estado, desviacion))
        return cur.lastrowid


def traerValoresMedidosDeMedicion(idMedicion: int, db_path: Optional[str]=None):
    """
    Trae todos los valores (pH, DBO, etc.) que pertenecen a una medición específica.
    Hace JOIN con la tabla 'parametro' para devolver nombreParametro y unidad.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT vm.idParametro, p.nombreParametro, p.unidad,
                   vm.valor, vm.estado, vm.desviacion
            FROM valorMedida vm
            JOIN parametro p ON vm.idParametro = p.id
            WHERE vm.idMedicion = ?
        """, (idMedicion,))
        return [dict(row) for row in cur.fetchall()]


def traerTodosLosValoresMedidos(db_path: Optional[str]=None):
    """
    Devuelve todos los valores medidos de todas las mediciones.
    Incluye información del parámetro.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT vm.idMedicion, vm.idParametro,
                   p.nombreParametro, p.unidad,
                   vm.valor, vm.estado, vm.desviacion
            FROM valorMedida vm
            JOIN parametro p ON vm.idParametro = p.id
        """)
        return [dict(row) for row in cur.fetchall()]


# ============================================================
#           MANEJO DE VALORES DE REFERENCIA
# ============================================================

def insertarValoresReferencia(idParametro: int, limiteMaxAceptable: float, limiteMaxWarning: float, db_path: Optional[str]=None) -> int:
    """
    Inserta los valores de referencia para un parámetro:
        - Limite máximo aceptable
        - Límite de advertencia
    Si ya existe un registro para ese parámetro → devuelve su ID.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM valorReferencia WHERE idParametro = ?", (idParametro,))
        row = cur.fetchone()

        if row is not None:
            return int(row["id"])

        cur.execute("""
            INSERT INTO valorReferencia (idParametro, limiteMaxAceptable, limiteMaxWarning)
            VALUES (?, ?, ?)
        """, (idParametro, limiteMaxAceptable, limiteMaxWarning))

         # cur.lastrowid NUNCA es None cuando hay INSERT, pero lo tipamos igual
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)


def traerValoresReferenciaPorParametro(idParametro: int, db_path: Optional[str] = None) -> Optional[ReferenciaParametro]:
    """
    Devuelve los valores de referencia para un parámetro específico.
    Retorna un TypedDict con:
        - LimiteMax
        - LimiteWarning
    o None si no hay referencia para ese parámetro.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT limiteMaxAceptable, limiteMaxWarning
            FROM valorReferencia
            WHERE idParametro = ?
        """, (idParametro,))

        row = cur.fetchone()
        if row is None:
            return None

        return ReferenciaParametro(
            LimiteMax=row["limiteMaxAceptable"],
            LimiteWarning=row["limiteMaxWarning"]
        )


def traerTodosLosValoresReferencia(db_path: Optional[str]=None):
    """
    Devuelve una lista con todas las referencias registradas.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM valorReferencia")
        return [dict(row) for row in cur.fetchall()]


def traerValorReferenciaPorId(idValorReferencia: int, db_path: Optional[str]=None):
    """
    Devuelve una referencia según su ID.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM valorReferencia WHERE id = ?", (idValorReferencia,))
        row = cur.fetchone()
        return dict(row) if row else None
