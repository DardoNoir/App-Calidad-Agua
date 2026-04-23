from typing import Optional, Any, List
from datetime import datetime
from src.utils.datetime import FORMATO_DB
from src.data.db import connection
from src.data.repository import getCursor

def traerSeriesParametroPorLugar(
    idLugar: int,
    idParametro: int,
    fechaInicio: Optional[datetime] = None,
    fechaFin: Optional[datetime] = None,
    db_path: Optional[str] = None
):
    
    query = """
        SELECT
            m.fecha_medicion AS fecha,
            vm.valor AS valor
        FROM medicion m
        JOIN valor_medida vm
            ON m.id = vm.id_medicion
        WHERE
            m.id_lugar = %s
            AND vm.id_parametro = %s
    """

    params: list[Any] = [idLugar, idParametro]

    if fechaInicio is not None:
        query += " AND m.fecha_medicion >= %s"
        params.append(fechaInicio)

    if fechaFin is not None:
        query += " AND m.fecha_medicion <= %s    "
        params.append(fechaFin)

    query += " ORDER BY m.fecha_medicion ASC"

    with connection() as conn: 
        cursor = getCursor(conn)
        cursor.execute(query, params)

        filas = []
        for row in cursor.fetchall():
            filas.append({ 
                "fecha": datetime.strptime(row["fecha"], FORMATO_DB),
                "valor": row["valor"]
            })

        return filas 

def traerSerieCompletaParametroLugar(
    idLugar: int,
    idParametro: int,
):

    query = """
    SELECT
        m.fecha_medicion AS fecha,
        vm.valor AS valor
    FROM medicion m
    JOIN valor_medida vm
      ON m.id = vm.id_medicion
     AND vm.id_parametro = %s
    WHERE m.id_lugar = %s
    ORDER BY m.fecha_medicion ASC
    """

    with connection() as conn:
        cur = getCursor(conn)
        cur.execute(query, (idParametro, idLugar))

        return [
            {
                "fecha": datetime.strptime(row["fecha"], FORMATO_DB),
                "valor": row["valor"]
            }
            for row in cur.fetchall()
        ]
