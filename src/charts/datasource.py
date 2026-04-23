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
            m.fechaMedicion AS fecha,
            vm.valor AS valor
        FROM medicion m
        JOIN valorMedida vm
            ON m.id = vm.idMedicion
        WHERE
            m.idLugar = %s
            AND vm.idParametro = %s
    """

    params: list[Any] = [idLugar, idParametro]

    if fechaInicio is not None:
        query += " AND m.fechaMedicion >= %s"
        params.append(fechaInicio)

    if fechaFin is not None:
        query += " AND m.fechaMedicion <= %s    "
        params.append(fechaFin)

    query += " ORDER BY m.fechaMedicion ASC"

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
        m.fechaMedicion AS fecha,
        vm.valor AS valor
    FROM medicion m
    JOIN valorMedida vm
      ON m.id = vm.idMedicion
     AND vm.idParametro = %s
    WHERE m.idLugar = %s
    ORDER BY m.fechaMedicion ASC
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
