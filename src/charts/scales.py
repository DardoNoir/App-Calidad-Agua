
from typing import TypedDict, List

class ParametroGrafico(TypedDict):
    idParametro: int
    nombreParametro: str
    unidad: str

def parametros_compatibles(parametros: List[ParametroGrafico]) -> bool:
    """
    Retorna True si todos los parámetros usan la misma unidad.
    """
    if not parametros:
        return False

    unidades = {p["unidad"] for p in parametros}
    return len(unidades) == 1
