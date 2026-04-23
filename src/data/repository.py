from .db import connection
from typing import Optional
from psycopg2.extras import RealDictCursor

from src.utils.security import verify_password, hash_password
from src.utils.datetime import parse_fecha_str, ahora_str

from src.analysis.evaluacion import ReferenciaParametro, EvaluarParametro
from src.analysis.calculoIca import calcular_ica, clasificar_ica, ajustar_ponderaciones
from src.analysis.subindices import calcular_subindice_parametro, registrar_curva, _CURVAS

# ============================================================
#                 HELPERS
# ============================================================
def getCursor(conn):
    return conn.cursor(cursor_factory=RealDictCursor)

# ============================================================
#                 MANEJO DE USUARIOS
# ============================================================
def crearUsuario(nombreUsuario: str, password: str, rol: str):
    pw_hash = hash_password(password)  
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
                    INSERT INTO usuario (nombreUsuario, password, rol) 
                    VALUES (%s, %s, %s)
                    RETURNING id""",
            (nombreUsuario, pw_hash, rol)
        )
        row = cur.fetchone()

def actualizarUsuario(idUsuario, nombreUsuario, password, rol):
    pw_hash = hash_password(password)

    with connection() as conn:
        cur = getCursor(conn)
        cur.execute(
            """
            UPDATE usuario
            SET nombreUsuario = %s, rol = %s, password = %s
            WHERE id = %s
        """
        ,(nombreUsuario, rol, pw_hash, idUsuario))

def actualizarUsuarioSinPassword(idUsuario, nombreUsuario, rol):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute(
            """
            UPDATE usuario
            SET nombreUsuario = %s, rol = %s
            WHERE id = %s
        """
        ,(nombreUsuario, rol, idUsuario))

def traerUsuarios():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM usuario")
        return cur.fetchall()  

def traerUsuarioPorNombre(nombreUsuario: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM usuario WHERE nombreUsuario = %s", (nombreUsuario,))
        return cur.fetchone() 

def traerUsuarioPorId(id: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM usuario WHERE id = %s", (id,))
        return cur.fetchone()

def autenticarUsuario(nombreUsuario: str, password: str):
    usuario = traerUsuarioPorNombre(nombreUsuario)
    if not usuario:
        return None

    if not verify_password(password, usuario["password"]):
        print("Contraseña incorrecta")
        return None

    ahora = ahora_str()

    with connection() as conn:
        cur = getCursor(conn)
        cur.execute(
            "UPDATE usuario SET ultimoInicio = %s WHERE id = %s",
            (ahora, usuario["id"])
        )

    return usuario

def existeUsuario(nombre: str):
    user=traerUsuarioPorNombre(nombre)
    return user is not None

# ============================================================
#               MANEJO DE LUGARES
# ============================================================
def insertarLugar(provincia: str, ciudad: str, cuerpoAgua: str, zona: str):
    with connection() as conn:
        cur = getCursor(conn)
        
        # Verificar existencia
        cur.execute("""
            SELECT id FROM lugar
            WHERE provincia = %s AND ciudad = %s AND cuerpoAgua = %s AND zona = %s
        """, (provincia, ciudad, cuerpoAgua, zona))

        row = cur.fetchone()
        if row:
            return int(row["id"])
        
        # Si no existe, insertar
        cur.execute("""
            INSERT INTO lugar (provincia, ciudad, cuerpoAgua, zona)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (provincia, ciudad, cuerpoAgua, zona))

        row = cur.fetchone()
        if row:
            return int(row["id"])

def traerLugares():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM lugar ORDER BY provincia, ciudad, cuerpoAgua")
        return cur.fetchall()

def traerLugarPorId(idLugar: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM lugar WHERE id = %s", (idLugar,))
        return cur.fetchone()

# ============================================================
#               MANEJO DE PARÁMETROS
# ============================================================
def insertarParametro(codigo: str, nombreParametro: str, unidad: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT id FROM parametro
            WHERE codigo = %s AND nombreParametro = %s AND unidad = %s
        """, (codigo, nombreParametro, unidad))

        row = cur.fetchone()
        if row:
            return int(row["id"])  

        cur.execute("""
            INSERT INTO parametro (codigo, nombreParametro, unidad)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (codigo, nombreParametro, unidad))

        row = cur.fetchone()
        if row:
            return int(row["id"])
        
        raise ValueError("Error al insertar parámetro")

def traerParametros():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM parametro")
        return cur.fetchall()
    
def traerParametroPorId(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM parametro WHERE id = %s", (idParametro,))
        return cur.fetchone()

def traerParametroPorNombre(nombreParametro: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM parametro WHERE nombreParametro = %s", (nombreParametro,))
        return cur.fetchone()

def existeParametro(nombreParametro: str):
    parametro=traerParametroPorNombre(nombreParametro)
    return parametro is not None

def actualizarParametro(idParametro: int, codigo: str, nombreParametro: str, unidad: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            UPDATE parametro SET codigo = %s, nombreParametro = %s, unidad = %
            WHERE id = %s
        """, (codigo, nombreParametro, unidad, idParametro))

# ============================================================
#               MANEJO DE MEDICIONES
# ============================================================
def insertarMedicion(idLugar: int, fechaMedicion: str, medidaTomadaPor: int, comentarios: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            INSERT INTO medicion (idLugar, fechaMedicion, medidaTomadaPor, comentarios)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (idLugar, fechaMedicion, medidaTomadaPor, comentarios))
        row = cur.fetchone()
        if row:
            return int(row["id"])

def traerMedicionPorId(idMedicion: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM medicion WHERE id = %s", (idMedicion,))
        return cur.fetchone()

def traerMedicionesPorLugar(idLugar: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT *
            FROM medicion
            WHERE idLugar = %s
        """, (idLugar,))
        return cur.fetchall()

def traerMedicionesPorUsuario(idUsuario: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT *
            FROM medicion
            WHERE medidaTomadaPor = %s
        """, (idUsuario,))
        return cur.fetchall()
    
def traerMedicionesPorFecha(fechaMedicion: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT *
            FROM medicion
            WHERE fechaMedicion = %s
        """, (fechaMedicion,))
        return cur.fetchall()

def traerMedicionesPorLugarYFecha(idLugar: int, fechaMedicion: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT id, fechaMedicion, comentarios
            FROM medicion
            WHERE idLugar = %s AND fechaMedicion = %s
        """, (idLugar, fechaMedicion))
        return cur.fetchall()

def traerMediciones():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM medicion")
        cur.fetchall()

def actualizarICAMedicion(idMedicion: int, ica: float, clasificacionICA: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            UPDATE medicion
            SET ica = %s, clasificacionICA = %s
            WHERE id = %s
        """, (ica, clasificacionICA, idMedicion))

def guardarMedicionCompleta(
        provincia: str,
        ciudad: str,
        cuerpoAgua: str,
        fechaMedicion,
        usuarioId: int,
        comentarios: str,
        valores: dict[int, float],
        zona: str,
):
    # Lugar
    idLugar = insertarLugar(provincia, ciudad, cuerpoAgua, zona)
    if idLugar is None:
        raise ValueError("Error al insertar lugar")

    # Medición
    fecha = parse_fecha_str(fechaMedicion)
    idMedicion = insertarMedicion(idLugar, fecha, usuarioId, comentarios)
    if idMedicion is None:
        raise ValueError("Error al insertar medición")

    subindices = []
    parametrosMedidos = []

    # Valores evaluados
    for idParametro, valor in valores.items():
        referencia_dict = traerValoresReferenciaPorParametro(idParametro)
        referencia = ReferenciaParametro(**referencia_dict) if referencia_dict else None
        
        estado, desviacion = EvaluarParametro(valor, referencia)

        insertarValorMedido(
            idMedicion,
            [{"idParametro": (idParametro)}],
            valor,
            estado,
            desviacion)
        
        try:
            par = traerParametroPorId(idParametro)
            if par:
                sub = calcular_subindice_parametro(par["nombreParametro"], valor)
            else:
                continue

            if sub is None:
                continue

            subindices.append({
                "idParametro": idParametro,
                "subindice": sub
            })

            parametrosMedidos.append(idParametro)

        except Exception as e:
            continue

    ponderacionesDb = traerPonderacionesParametroActivas()
    ponderacionBase = {p["idParametro"]:p["ponderacion"] for p in ponderacionesDb}
    
    ponderaciones_ajustadas = ajustar_ponderaciones(ponderacionBase, parametrosMedidos)

    listaICA = []
    for item in subindices: 
        listaICA.append({
            "idParametro": item["idParametro"],
            "subindice": item["subindice"],
            "ponderacion": ponderaciones_ajustadas[item["idParametro"]]
        })

    ica = calcular_ica(listaICA)
    clas=clasificar_ica(ica)
    
    actualizarICAMedicion(idMedicion,ica,clas)

    return idMedicion

def traerMedicionesConDetalleLugar():
    with connection() as conn:
        cur = getCursor(conn)
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
        return cur.fetchall()

def traerMedicionesFiltradas(provincia=None, ciudad=None, cuerpoAgua=None, zona=None):
    with connection() as conn:
        cur = getCursor(conn)
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
                l.cuerpoAgua,
                l.zona
            FROM medicion m
            JOIN lugar l ON m.idLugar = l.id
            JOIN usuario u ON m.medidaTomadaPor = u.id
            WHERE 1=1
        """
        params = []

        if provincia:
            query += " AND l.provincia = %s"
            params.append(provincia)
        if ciudad:
            query += " AND l.ciudad = %s"
            params.append(ciudad)
        if cuerpoAgua:
            query += " AND l.cuerpoAgua = %s"
            params.append(cuerpoAgua)
        if zona:
            query += " AND l.zona = %s"
            params.append(zona)

        query += " ORDER BY m.fechaMedicion ASC"

        cur.execute(query, params)

        return cur.fetchall()

# ============================================================
#           MANEJO DE VALORES MEDIDOS
# ============================================================
def insertarValorMedido(
    idMedicion: int,
    parametros: list[dict[str, int]],
    valor: float,
    estado: str,
    desviacion: str
):

    with connection() as conn:
        cur = getCursor(conn)

        ids_insertados: list[int] = []

        for p in parametros:
            cur.execute("""
                INSERT INTO valorMedida (idMedicion, idParametro, valor, estado, desviacion)
                VALUES (%s, %s, %s, %s, %s),
                RETURNING id
                """, (idMedicion, p["idParametro"], valor, estado, desviacion))
            
            id_insertado = cur.fetchone()
            if id_insertado:
                ids_insertados.append(int(id_insertado["id"]))

        return ids_insertados

def traerValoresMedidosDeMedicion(idMedicion: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT vm.idParametro, p.nombreParametro, p.unidad,
                   vm.valor, vm.estado, vm.desviacion
            FROM valorMedida vm
            JOIN parametro p ON vm.idParametro = p.id
            WHERE vm.idMedicion = %s
        """, (idMedicion,))
        return cur.fetchall()

def traerTodosLosValoresMedidos():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT vm.idMedicion, vm.idParametro,
                   p.nombreParametro, p.unidad,
                   vm.valor, vm.estado, vm.desviacion
            FROM valorMedida vm
            JOIN parametro p ON vm.idParametro = p.id
        """)
        return cur.fetchall()

# ============================================================
#           MANEJO DE VALORES DE REFERENCIA
# ============================================================
def insertarValoresReferencia(idParametro: int, limiteMaxAceptable: float, limiteMaxWarning: float,
                              limiteMinAceptable: float, limiteMinWarning:float,
                              normativa: str, rangoPosibleMin: float, rangoPosibleMax: float):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT id FROM valorReferencia WHERE idParametro = %s", (idParametro,))
        
        row = cur.fetchone()
        if row:
            return int(row["id"])

        cur.execute("""
            INSERT INTO valorReferencia (idParametro, limiteMaxAceptable, limiteMaxWarning,
                     limiteMinAceptable, limiteMinWarning, normativa, rangoPosibleMin, rangoPosibleMax)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (idParametro, limiteMaxAceptable, limiteMaxWarning, 
              limiteMinAceptable, limiteMinWarning, normativa, rangoPosibleMin, rangoPosibleMax))

        row = cur.fetchone()
        if row:
            return int(row["id"])

        raise ValueError("Error al insertar valor de referencia")

def traerValoresReferenciaPorParametro(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT *
            FROM valorReferencia
            WHERE idParametro = %s
        """, (idParametro,))
        return cur.fetchone()
    
def traerTodosLosValoresReferencia():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM valorReferencia")
        return cur.fetchall()

def traerValorReferenciaPorId(idValorReferencia: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM valorReferencia WHERE id = %s", (idValorReferencia,))
        return cur.fetchone()

def valoresReferenciaCargados(idParametro: int):
    referencia=traerValoresReferenciaPorParametro(idParametro)
    return referencia is not None

def actualizarValoresReferencia(idParametro: int, limiteMaxAceptable: float, limiteMaxWarning: float,
                              limiteMinAceptable: float, limiteMinWarning:float, normativa: str,
                              rangoPosibleMin: float, rangoPosibleMax: float):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            UPDATE valorReferencia SET limiteMaxAceptable = %s, limiteMaxWarning = %s,
                     limiteMinAceptable = %s, limiteMinWarning = %s, normativa = %s, rangoPosibleMin = %s, rangoPosibleMax = %s  
                     WHERE idParametro = %s
        """, (limiteMaxAceptable, limiteMaxWarning, limiteMinAceptable, limiteMinWarning, normativa, rangoPosibleMin, rangoPosibleMax, idParametro))

# ============================================================
#           MANEJO DE PONDERACIONES
# ============================================================
def insertarPonderacionParametro(idParametro: int, ponderacion: float):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            INSERT INTO ponderacionParametro (idParametro, ponderacion)
            VALUES (%s, %s)
            RETURNING id
        """, (idParametro, ponderacion))

        row = cur.fetchone()
        if row:
            return int(row["id"])

        raise ValueError("Error al insertar ponderación")

def actualizarPonderacion(idParametro: int, ponderacion: float):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute(
            """
            UPDATE ponderacionParametro SET ponderacion = %s WHERE id = %s
        """,
        (ponderacion, idParametro))

def traerPonderacionesParametroActivas():    
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT *
            FROM ponderacionParametro
            WHERE activo = 1
        """)
        return cur.fetchall()
    
def traerPonderacionParametro(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM ponderacionParametro WHERE idParametro = %s", (idParametro,))
        return cur.fetchone()


# ============================================================
#           MANEJO DE SUBINDICES
# ============================================================
def insertarValor(idParametro: int, valor: float, subindice: float):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            INSERT INTO curvaSubindice (idParametro, valor, subindice)
            VALUES (%s, %s, %s)
        """, (idParametro, valor, subindice))

def eliminarValor(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            DELETE FROM curvaSubindice
            WHERE idParametro = %s
        """, (idParametro,))

def traerSubindices(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT valor, subindice
            FROM curvaSubindice
            WHERE idParametro = %s
            ORDER BY valor
        """, (idParametro,))
        return cur.fetchall()
    
def cargar_curvas_desde_db():
    parametros = traerParametros()

    for p in parametros:
        with connection() as conn:
            cur = getCursor(conn)
            cur.execute("""
                SELECT valor, subindice
                FROM curvaSubindice
                WHERE idParametro = %s
                ORDER BY valor
            """, (p["id"],))
            puntos = cur.fetchall()
            if len(puntos) > 2:
                lista_puntos = [(pt["valor"], pt["subindice"]) for pt in puntos]
                registrar_curva(p["nombreParametro"], lista_puntos)