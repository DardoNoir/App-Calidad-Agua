from typing import Optional, Any
from datetime import datetime
from src.data.db import connection

def traerSeriesParametroPorLugar(
        idLugar: int,
        idParametro: int,
        fechaInicio: Optional[datetime] = None,
        fechaFin: Optional[datetime] = None,
        db_path: Optional[str] = None
        ):
    """
    Devuelve una serie temporal de un parámetro en un lugar.
    Estructura:
    [
        {fecha, valor}
    ]
    """
    query = """
    SELECT m.fechaMedicion AS fecha, m.valor AS valor
    FROM mediciones m
    JOIN valorMedida v ON m.idValorMedida = v.idValorMedida
    WHERE m.idLugar = ? AND v.idParametro = ?
    """
    params: list[Any] = [idLugar, idParametro]

    if fechaInicio:
        query += " AND m.fechaMedicion >= ?"
        params.append(fechaInicio)
    
    if fechaFin:
        query += " AND m.fechaMedicion <= ?"
        params.append(fechaFin)
    
    query += " ORDER BY m.fechaMedicion ASC"
    with connection(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]