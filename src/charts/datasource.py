from typing import Optional, Any, List
from datetime import datetime
from sqlite3 import Row

from src.data.db import connection


def traerSeriesParametroPorLugar(
    idLugar: int,
    idParametro: int,
    fechaInicio: Optional[datetime] = None,
    fechaFin: Optional[datetime] = None,
    db_path: Optional[str] = None
) -> List[dict[str, Any]]:
    
    query = """
        SELECT
            m.fechaMedicion AS fecha,
            vm.valor AS valor
        FROM medicion m
        JOIN valorMedida vm
            ON m.id = vm.idMedicion
        WHERE
            m.idLugar = ?
            AND vm.idParametro = ?
    """

    params: list[Any] = [idLugar, idParametro]

    if fechaInicio is not None:
        query += " AND m.fechaMedicion >= ?"
        params.append(fechaInicio)

    if fechaFin is not None:
        query += " AND m.fechaMedicion <= ?"
        params.append(fechaFin)

    query += " ORDER BY m.fechaMedicion ASC"

    with connection(db_path) as conn:
        conn.row_factory = Row  
        cursor = conn.cursor()
        cursor.execute(query, params)

        filas = []
        for row in cursor.fetchall():
            filas.append({ # type: ignore
                "fecha": datetime.strptime(row["fecha"], "%d/%m/%Y %H:%M"),
                "valor": row["valor"]
            })

        return filas # type: ignore


def traerSerieCompletaParametroLugar(idLugar: int, idParametro: int, db_path: Optional[str] = None) -> List[dict[str, Any]]:
    query = """
    SELECT
        m.fechaMedicion AS fecha,
        vm.valor AS valor
    FROM medicion m
    JOIN valorMedida vm
      ON m.id = vm.idMedicion
     AND vm.idParametro = ?
    WHERE m.idLugar = ?
    ORDER BY m.fechaMedicion ASC
    """
    with connection(db_path) as conn:
        cur = conn.cursor()
        cur.execute(query, (idParametro, idLugar))
        return [
            {"fecha": datetime.fromisoformat(r["fecha"]),
             "valor": r["valor"]}
            for r in cur.fetchall()
        ]

