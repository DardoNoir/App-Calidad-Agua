from src.analysis.subindices import calcular_subindice_parametro

from .db import connection
from typing import Optional
from psycopg2.extras import RealDictCursor

from src.utils.security import verify_password, hash_password
from src.utils.datetime import parse_fecha_str, ahora_str, parse_fecha_dt

from src.analysis.evaluacion import ReferenciaParametro, EvaluarParametro
from src.analysis.calculoIca import calcular_ica, clasificar_ica, ajustar_ponderaciones
from src.curves.curvas_service import asegurar_curva_cargada, recargar_curva, invalidar_curva

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
                    INSERT INTO usuario (nombre_usuario, password, rol) 
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
            SET nombre_usuario = %s, rol = %s, password = %s
            WHERE id = %s
        """
        ,(nombreUsuario, rol, pw_hash, idUsuario))

def actualizarUsuarioSinPassword(idUsuario, nombreUsuario, rol):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute(
            """
            UPDATE usuario
            SET nombre_usuario = %s, rol = %s
            WHERE id = %s
        """
        ,(nombreUsuario, rol, idUsuario))

def traerUsuarios():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM usuario ORDER BY id")
        return cur.fetchall()  

def traerUsuarioPorNombre(nombreUsuario: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM usuario WHERE nombre_usuario = %s", (nombreUsuario,))
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
            "UPDATE usuario SET ultimo_inicio = %s WHERE id = %s",
            (ahora, usuario["id"])
        )

    return usuario

def existeUsuario(nombre: str):
    user=traerUsuarioPorNombre(nombre)
    return user is not None

# ============================================================
#               MANEJO DE LUGARES
# ============================================================
def insertarLugar(provincia: str, ciudad: str, cuerpoAgua: str, zona: str, id_municipio: int):
    with connection() as conn:
        cur = getCursor(conn)
        
        cur.execute("""
            SELECT id FROM lugar
            WHERE provincia = %s AND ciudad = %s AND cuerpo_agua = %s AND zona = %s AND id_municipio = %s
        """, (provincia, ciudad, cuerpoAgua, zona, id_municipio))

        row = cur.fetchone()
        if row:
            return int(row["id"])
        
        cur.execute("""
            INSERT INTO lugar (provincia, ciudad, cuerpo_agua, zona, id_municipio)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (provincia, ciudad, cuerpoAgua, zona, id_municipio))

        row = cur.fetchone()
        if row:
            return int(row["id"])

def traerLugares():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM lugar ORDER BY provincia, ciudad, cuerpo_agua")
        return cur.fetchall()

def traerLugarPorId(idLugar: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM lugar WHERE id = %s", (idLugar,))
        return cur.fetchone()

def traerLugaresPorUsuario(idUsuario: int):
    with connection() as conn:
        cur = getCursor(conn)

        usuario = traerUsuarioPorId(idUsuario)
        if usuario is None:
            raise Exception("Error al cargar usuario")

        if usuario["rol"] == "Administrador" and usuario["id_municipio"] is None:
            cur.execute(
                """
                SELECT * FROM lugar
                ORDER BY provincia, ciudad, cuerpo_agua, zona
                """)
            return cur.fetchall()

        cur.execute(
            """
            SELECT * FROM lugar
            WHERE id_municipio = %s
            ORDER BY provincia, ciudad, cuerpo_agua, zona
            """, (usuario["id_municipio"],))
        return cur.fetchall()
# ============================================================
#               MANEJO DE PARÁMETROS
# ============================================================
def insertarParametro(codigo: str, nombreParametro: str, unidad: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT id FROM parametro
            WHERE codigo = %s AND nombre_parametro = %s AND unidad = %s
        """, (codigo, nombreParametro, unidad))

        row = cur.fetchone()
        if row:
            return int(row["id"])  

        cur.execute("""
            INSERT INTO parametro (codigo, nombre_parametro, unidad)
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
        cur.execute("SELECT * FROM parametro ORDER BY id")
        return cur.fetchall()
    
def traerParametroPorId(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM parametro WHERE id = %s", (idParametro,))
        return cur.fetchone()

def traerParametroPorNombre(nombreParametro: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM parametro WHERE nombre_parametro = %s", (nombreParametro,))
        return cur.fetchone()

def existeParametro(nombreParametro: str):
    parametro=traerParametroPorNombre(nombreParametro)
    return parametro is not None

def actualizarParametro(idParametro: int, codigo: str, nombreParametro: str, unidad: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            UPDATE parametro SET codigo = %s, nombre_parametro = %s, unidad = %s
            WHERE id = %s
        """, (codigo, nombreParametro, unidad, idParametro))

# ============================================================
#               MANEJO DE MEDICIONES
# ============================================================
def insertarMedicion(idLugar: int, fechaMedicion: str, medidaTomadaPor: int, comentarios: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            INSERT INTO medicion (id_lugar, fecha_medicion, medida_tomada_por, comentarios)
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
            WHERE id_lugar = %s
        """, (idLugar,))
        return cur.fetchall()

def traerMedicionesPorUsuario(idUsuario: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT *
            FROM medicion
            WHERE medida_tomada_por = %s
        """, (idUsuario,))
        return cur.fetchall()
    
def traerMedicionesPorFecha(fechaMedicion: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT *
            FROM medicion
            WHERE fecha_medicion = %s
        """, (fechaMedicion,))
        return cur.fetchall()

def traerMedicionesPorLugarYFecha(idLugar: int, fechaMedicion: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT id, fecha_medicion, comentarios
            FROM medicion
            WHERE id_lugar = %s AND fecha_medicion = %s
        """, (idLugar, fechaMedicion))
        return cur.fetchall()

def traerMediciones():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM medicion ORDER BY fecha_medicion DESC")
        return cur.fetchall()

def actualizarICAMedicion(idMedicion: int, ica: float, clasificacionICA: str):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            UPDATE medicion
            SET ica = %s, clasificacion_ica = %s
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
    
    # Usuario
    usuario = traerUsuarioPorId(usuarioId)
    if usuario is None:
        raise ValueError("Usuario no encontrado")
    
    # Lugar
    idLugar = insertarLugar(provincia, ciudad, cuerpoAgua, zona, usuario["id_municipio"])
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
            [{"id_parametro": (idParametro)}],
            valor,
            estado,
            desviacion)
        
        try:
            asegurar_curva_cargada(idParametro)
            sub = calcular_subindice_parametro(idParametro, valor)
        
            if sub is None:
                continue

            subindices.append({
                "id_parametro": idParametro,
                "subindice": sub
            })

            parametrosMedidos.append(idParametro)

        except Exception as e:
            continue

    ponderacionesDb = traerPonderacionesParametroActivas()
    ponderacionBase = {p["id_parametro"]:p["ponderacion"] for p in ponderacionesDb}
    
    ponderaciones_ajustadas = ajustar_ponderaciones(ponderacionBase, parametrosMedidos)

    listaICA = []
    for item in subindices: 
        listaICA.append({
            "id_parametro": item["id_parametro"],
            "subindice": item["subindice"],
            "ponderacion": ponderaciones_ajustadas[item["id_parametro"]]
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
                m.fecha_medicion,
                u.nombre_usuario AS tomada_por,
                m.ica,
                m.clasificacion_ica,
                m.comentarios,
                m.cargada_sistema,
                l.provincia,
                l.ciudad,
                l.cuerpo_agua,
                l.id as idLugar
            FROM medicion m
            JOIN lugar l ON m.id_lugar = l.id
            JOIN usuario u ON m.medida_tomada_por = u.id
            ORDER BY m.fecha_medicion DESC
        """)
        return cur.fetchall()

def traerMedicionesFiltradas(id_usuario: int, provincia=None, ciudad=None, cuerpoAgua=None, zona=None):
    with connection() as conn:
        cur = getCursor(conn)
        query = """
            SELECT 
                m.id,
                m.fecha_medicion,
                u.nombre_usuario AS tomada_por,
                m.ica,
                m.clasificacion_ica,
                m.comentarios,
                m.cargada_sistema,
                l.provincia,
                l.ciudad,
                l.cuerpo_agua,
                l.zona
            FROM medicion m
            JOIN lugar l ON m.id_lugar = l.id
            JOIN usuario u ON m.medida_tomada_por = u.id
            WHERE 1=1
        """
        params = []
        usuario = traerUsuarioPorId(id_usuario)
        if usuario is None:
            raise ValueError("Error usuario no encontrado")

        if usuario["rol"] != "Administrador" or usuario["id_municipio"] is not None:
            query += "AND l.id_municipio = %s"
            params.append(usuario["id_municipio"])
        if provincia:
            query += " AND l.provincia = %s"
            params.append(provincia)
        if ciudad:
            query += " AND l.ciudad = %s"
            params.append(ciudad)
        if cuerpoAgua:
            query += " AND l.cuerpo_agua = %s"
            params.append(cuerpoAgua)
        if zona:
            query += " AND l.zona = %s"
            params.append(zona)

        query += " ORDER BY m.fecha_medicion ASC"

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
                INSERT INTO valor_medida (id_medicion, id_parametro, valor, estado, desviacion)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
                """, (idMedicion, p["id_parametro"], valor, estado, desviacion))
            
            id_insertado = cur.fetchone()
            if id_insertado:
                ids_insertados.append(int(id_insertado["id"]))

        return ids_insertados

def traerValoresMedidosDeMedicion(idMedicion: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT vm.id_parametro, p.nombre_parametro, p.unidad,
                   vm.valor, vm.estado, vm.desviacion
            FROM valor_medida vm
            JOIN parametro p ON vm.id_parametro = p.id
            WHERE vm.id_medicion = %s
        """, (idMedicion,))
        return cur.fetchall()

def traerTodosLosValoresMedidos():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT vm.id_medicion, vm.id_parametro,
                   p.nombre_parametro, p.unidad,
                   vm.valor, vm.estado, vm.desviacion
            FROM valor_medida vm
            JOIN parametro p ON vm.id_parametro = p.id
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
        cur.execute("SELECT id FROM valor_referencia WHERE id_parametro = %s", (idParametro,))
        
        row = cur.fetchone()
        if row:
            return int(row["id"])

        cur.execute("""
            INSERT INTO valor_referencia (id_parametro, limite_max_aceptable, limite_max_warning,
                     limite_min_aceptable, limite_min_warning, normativa, rango_posible_min, rango_posible_max)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id        
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
            FROM valor_referencia
            WHERE id_parametro = %s
        """, (idParametro,))
        return cur.fetchone()
    
def traerTodosLosValoresReferencia():
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM valor_referencia")
        return cur.fetchall()

def traerValorReferenciaPorId(idValorReferencia: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM valor_referencia WHERE id = %s", (idValorReferencia,))
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
            UPDATE valor_referencia SET limite_max_aceptable = %s, limite_max_warning = %s,
                     limite_min_aceptable = %s, limite_min_warning = %s, normativa = %s, rango_posible_min = %s, rango_posible_max = %s  
                     WHERE id_parametro = %s
        """, (limiteMaxAceptable, limiteMaxWarning, limiteMinAceptable, limiteMinWarning, normativa, rangoPosibleMin, rangoPosibleMax, idParametro))

# ============================================================
#           MANEJO DE PONDERACIONES
# ============================================================
def insertarPonderacionParametro(idParametro: int, ponderacion: float):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            INSERT INTO ponderacion_parametro (id_parametro, ponderacion)
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
            UPDATE ponderacion_parametro SET ponderacion = %s WHERE id_parametro = %s
        """,
        (ponderacion, idParametro))

def traerPonderacionesParametroActivas():    
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT *
            FROM ponderacion_parametro
            WHERE activo = 1
        """)
        return cur.fetchall()
    
def traerPonderacionParametro(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("SELECT * FROM ponderacion_parametro WHERE id_parametro = %s", (idParametro,))
        return cur.fetchone()


# ============================================================
#           MANEJO DE SUBINDICES
# ============================================================
def insertarValor(idParametro: int, valor: float, subindice: float):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            INSERT INTO curva_subindice (id_parametro, valor, subindice)
            VALUES (%s, %s, %s)
        """, (idParametro, valor, subindice))

def eliminarValor(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            DELETE FROM curva_subindice
            WHERE id_parametro = %s
        """, (idParametro,))

def traerSubindices(idParametro: int):
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            SELECT valor, subindice
            FROM curva_subindice
            WHERE id_parametro = %s
            ORDER BY valor
        """, (idParametro,))
        return cur.fetchall()
    
def guardarCurvas(idParametro: int, puntos: list[tuple[float, float]]):
    valores_x = [p[0] for p in puntos]
    if len(set(valores_x)) != len(valores_x):            
        raise ValueError("Los valores de 'valor' deben ser únicos para cada punto de la curva.")
    
    with connection() as conn:
        cur = getCursor(conn)
        cur.execute("""
            DELETE FROM curva_subindice
            WHERE id_parametro = %s
        """, (idParametro,))
        
        for valor, subindice in puntos:
            cur.execute("""
                INSERT INTO curva_subindice (id_parametro, valor, subindice)
                VALUES (%s, %s, %s)
            """, (idParametro, valor, subindice))

    recargar_curva(idParametro)




