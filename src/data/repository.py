from .db import connection
from src.utils.security import hash_password
from typing import Optional
from datetime import datetime
from src.analysis.evaluacion import ReferenciaParametro, EvaluarParametro
from src.utils.security import verify_password, hash_password
from src.utils.datetime import parse_fecha_str
from src.analysis.calculoIca import calcular_ica, clasificar_ica, ajustar_ponderaciones
from src.analysis.subindices import calcular_subindice_parametro

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
    
def actualizarUsuario(idUsuario, nombreUsuario, password, rol, db_path:Optional[str]=None):
    pw_hash = hash_password(password)

    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE usuario
            SET nombreUsuario = ?, rol = ?, password = ?
            WHERE id = ?
        """
        ,(nombreUsuario, password, rol, idUsuario))

def actualizarUsuarioSinPassword(idUsuario, nombreUsuario, rol, db_path:Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE usuario
            SET nombreUsuario = ?, rol = ?
            WHERE id = ?
        """
        ,(nombreUsuario, rol, idUsuario))


def traerUsuarios(db_path: Optional[str]=None):
    """
    Devuelve una lista con todos los usuarios del sistema.
    Cada usuario se devuelve como un diccionario {'id':..., 'nombreUsuario':..., 'rol':...}
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM usuario")
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
        cur.execute("SELECT * FROM usuario WHERE id = ?", (id,))
        row = cur.fetchone()
        return dict(row) if row else None

def autenticarUsuario(nombreUsuario: str, password: str, db_path=None):
    usuario = traerUsuarioPorNombre(nombreUsuario, db_path)
    if not usuario:
        return None

    if not verify_password(password, usuario["password"]):
        print("Contraseña incorrecta")
        return None

    ahora = datetime.now()

    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            "UPDATE usuario SET ultimoInicio = ? WHERE id = ?",
            (ahora, usuario["id"])
        )

    return usuario

def existeUsuario(nombre: str, db_path: Optional[str]=None):
    user=traerUsuarioPorNombre(nombre, db_path)
    return user is not None

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

def traerParametroPorNombre(nombreParametro: str, db_path: Optional[str]=None):
    """
    Devuelve un parámetro según su nombre.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM parametro WHERE nombreParametro = ?", (nombreParametro,))
        row = cur.fetchone()
        return dict(row) if row else None

def existeParametro(nombreParametro: str, db_path: Optional[str]=None):
    parametro=traerParametroPorNombre(nombreParametro, db_path)
    return parametro is not None

def actualizarParametro(idParametro: int, codigo: str, nombreParametro: str, unidad: str, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE parametro SET codigo = ?, nombreParametro = ?, unidad = ?
            WHERE id = ?
        """, (codigo, nombreParametro, unidad, idParametro))

# ============================================================
#               MANEJO DE MEDICIONES
# ============================================================
def insertarMedicion(idLugar: int, fechaMedicion: str, medidaTomadaPor: int, comentarios: str, db_path: Optional[str] = None) -> int:
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

def traerMedicionesPorFecha(fechaMedicion: str, db_path: Optional[str]=None):
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

def traerMedicionesPorLugarYFecha(idLugar: int, fechaMedicion: str, db_path: Optional[str]=None):
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

def actualizarICAMedicion(idMedicion: int, ica: float, clasificacionICA: str, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE medicion
            SET ica = ?, clasificacionICA = ?
            WHERE id = ?
        """, (ica, clasificacionICA, idMedicion))

def guardarMedicionCompleta(
        provincia: str,
        ciudad: str,
        cuerpoAgua: str,
        fechaMedicion,
        usuarioId: int,
        comentarios: str,
        valores: dict[int, float],
        db_path: Optional[str]=None
):
    """
    valores = {idParametro: valor}
    """
    # Lugar
    idLugar = insertarLugar(provincia, ciudad, cuerpoAgua)

    # Medición
    fecha = parse_fecha_str(fechaMedicion)
    idMedicion = insertarMedicion(idLugar, fecha, usuarioId, comentarios)


    subindices = []
    parametrosMedidos = []

    # Valores evaluados
    for idParametro, valor in valores.items():
        referencia_dict = traerValoresReferenciaPorParametro(idParametro, db_path)
        referencia = ReferenciaParametro(**referencia_dict) if referencia_dict else None
        estado, desviacion = EvaluarParametro(valor, referencia)

        insertarValorMedido(
            idMedicion,
            [{"idParametro": idParametro}],
            valor,
            estado,
            desviacion,
            db_path)
        
        try:
            parametro = traerParametroPorId(idParametro, db_path)
            if parametro is None:
            # Inconsistencia grave: valor medido sin parámetro
                continue
            sub = calcular_subindice_parametro(parametro["nombreParametro"], valor)

            subindices.append({
                "idParametro": idParametro,
                "subindice": sub
            })
            parametrosMedidos.append(idParametro)
        except ValueError:
            pass

    ponderacionesDb = traerPonderacionesParametroActivas(db_path)
    ponderacionBase = {p["idParametro"]:p["ponderacion"] for p in ponderacionesDb}
    
    ponderaciones_ajustadas = ajustar_ponderaciones(ponderacionBase, parametrosMedidos)

    listaICA = []
    for item in subindices:
        idParam = item["idParametro"]
        listaICA.append({
            "idParametro": idParam,
            "subindice": item["subindice"],
            "ponderacion": ponderaciones_ajustadas[idParam]
        })

    ica = calcular_ica(listaICA)
    clas=clasificar_ica(ica)
    
    actualizarICAMedicion(idMedicion,ica,clas)

    return idMedicion

def traerMedicionesConDetalleLugar(db_path: Optional[str]=None):
    """
    Devuelve las mediciones con información del lugar y usuario.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                m.id,
                m.fechaMedicion,
                u.nombreUsuario AS tomadaPor,
                m.ica,
                m.clasificacionICA,
                m.comentarios,
                m.cargadaSistema,
                l.provincia,
                l.ciudad,
                l.cuerpoAgua,
                l.id as idLugar
            FROM medicion m
            JOIN lugar l ON m.idLugar = l.id
            JOIN usuario u ON m.medidaTomadaPor = u.id
            ORDER BY m.fechaMedicion DESC
        """)
        return [dict(row) for row in cur.fetchall()]

def traerMedicionesFiltradas(provincia=None, ciudad=None, cuerpoAgua=None, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        query = """
            SELECT 
                m.id,
                m.fechaMedicion,
                u.nombreUsuario AS tomadaPor,
                m.ica,
                m.clasificacionICA,
                m.comentarios,
                m.cargadaSistema,
                l.provincia,
                l.ciudad,
                l.cuerpoAgua
            FROM medicion m
            JOIN lugar l ON m.idLugar = l.id
            JOIN usuario u ON m.medidaTomadaPor = u.id
            WHERE 1=1
        """
        params = []

        if provincia:
            query += " AND l.provincia = ?"
            params.append(provincia)
        if ciudad:
            query += " AND l.ciudad = ?"
            params.append(ciudad)
        if cuerpoAgua:
            query += " AND l.cuerpoAgua = ?"
            params.append(cuerpoAgua)

        query += " ORDER BY m.fechaMedicion DESC"

        cur.execute(query, params)


        return [dict(row) for row in cur.fetchall()]

# ============================================================
#           MANEJO DE VALORES MEDIDOS
# ============================================================
def insertarValorMedido(
    idMedicion: int,
    parametros: list[dict[str, int]],
    valor: float,
    estado: str,
    desviacion: str,
    db_path: Optional[str] = None
) -> list[int]:

    with connection(db_path) as conn:
        cur = conn.cursor()

        ids_insertados: list[int] = []

        for p in parametros:
            cur.execute("""
                INSERT INTO valorMedida (idMedicion, idParametro, valor, estado, desviacion)
                VALUES (?, ?, ?, ?, ?)
                """, (idMedicion, p["idParametro"], valor, estado, desviacion))

            if cur.lastrowid is not None:
                ids_insertados.append(cur.lastrowid)

        return ids_insertados

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

def insertarValoresReferencia(idParametro: int, limiteMaxAceptable: float, limiteMaxWarning: float,
                              limiteMinAceptable: float, limiteMinWarning:float,
                              normativa: str,  db_path: Optional[str]=None) -> int:
    """
    Inserta los valores de referencia para un parámetro:
        - Limite máximo aceptable
        - Límite de advertencia
        - Límite mínimo aceptable
        - Limite mínimo de advertencia
    Si ya existe un registro para ese parámetro → devuelve su ID.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM valorReferencia WHERE idParametro = ?", (idParametro,))
        row = cur.fetchone()

        if row is not None:
            return int(row["id"])

        cur.execute("""
            INSERT INTO valorReferencia (idParametro, limiteMaxAceptable, limiteMaxWarning,
                     limiteMinAceptable, limiteMinWarning, normativa)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (idParametro, limiteMaxAceptable, limiteMaxWarning, 
              limiteMinAceptable, limiteMinWarning, normativa))

         # cur.lastrowid NUNCA es None cuando hay INSERT, pero lo tipamos igual
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)

def traerValoresReferenciaPorParametro(idParametro: int, db_path: Optional[str] = None):
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
            SELECT *
            FROM valorReferencia
            WHERE idParametro = ?
        """, (idParametro,))
        row = cur.fetchone()
        return dict(row) if row else None
    
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

def valoresReferenciaCargados(idParametro: int, db_path: Optional[str]=None):
    referencia=traerValoresReferenciaPorParametro(idParametro, db_path)
    return referencia is not None

def actualizarValoresReferencia(idParametro: int, limiteMaxAceptable: float, limiteMaxWarning: float,
                              limiteMinAceptable: float, limiteMinWarning:float, normativa: str, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE valorReferencia SET limiteMaxAceptable = ?, limiteMaxWarning = ?,
                     limiteMinAceptable = ?, limiteMinWarning = ?, normativa = ?
                     WHERE idParametro = ?
        """, (limiteMaxAceptable, limiteMaxWarning, limiteMinAceptable, limiteMinWarning, normativa, idParametro))

# ============================================================
#           MANEJO DE PONDERACIONES
# ============================================================
def insertarPonderacionParametro(idParametro: int, ponderacion: float, db_path: Optional[str]=None) -> int:
    """
    Inserta una ponderación para un parámetro específico.
    - idParametro: ID del parámetro
    - ponderacion: valor entre 0 y 1
    Devuelve el ID del registro insertado.
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ponderacionParametro (idParametro, ponderacion)
            VALUES (?, ?)
        """, (idParametro, ponderacion))

         # cur.lastrowid NUNCA es None cuando hay INSERT, pero lo tipamos igual
        last_id = cur.lastrowid
        if last_id is None:
            raise RuntimeError("Error inesperado: lastrowid es None")

        return int(last_id)

def actualizarPonderacion(idParametro: int, ponderacion: float, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE ponderacionParametro SET ponderacion = ? WHERE id = ?
        """,
        (ponderacion, idParametro))

def traerPonderacionesParametroActivas(db_path: Optional[str]=None):    
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT *
            FROM ponderacionParametro
            WHERE activo = 1
        """)
        return [dict(row) for row in cur.fetchall()]
    
def traerPonderacionParametro(idParametro: int, db_path: Optional[str]=None):
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM ponderacionParametro WHERE idParametro = ?", (idParametro,))
        row = cur.fetchone()
        return dict(row) if row else None