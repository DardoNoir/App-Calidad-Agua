from typing import List, TypedDict

class subindice(TypedDict):
    idParametro: int
    subindice: float
    ponderacion: float

def ajustar_ponderaciones(ponderacionesBase: dict[int, float],
                          parametrosMedidos: List[int]) -> dict[int, float]:
    """
    Redistribuye las ponderaciones de los parámetros no medidos
    entre los parámetros medidos, manteniendo suma total = 1.

    ponderaciones_base: {idParametro: ponderacion}
    parametros_medidos: [idParametro, ...]

    Retorna:
        dict {idParametro: ponderacion_ajustada}
    """
    medidos = set(parametrosMedidos)
    todos = set(ponderacionesBase.keys())
    noMedidos = todos - medidos

    if not medidos:
        raise ValueError("No hay parámetros para calcular el ICA.")

    sumaNoMedidos = sum(ponderacionesBase[idParam] for idParam in noMedidos)

    extraPorParametro = sumaNoMedidos / len(medidos)
    ponderacionesAjustadas: dict[int, float] = {}

    for idParam in medidos:
        ponderacionesAjustadas[idParam] = ponderacionesBase[idParam] + extraPorParametro

    return ponderacionesAjustadas



def calcular_ica(subindices: List[subindice]) -> float:
    """
    Calcula el Índice de Calidad del Agua (ICA) basado en los subíndices y ponderaciones proporcionadas.

    Parámetros:
    subindices (List[subindice]): Lista de diccionarios que contienen 'idParametro', 'subindice' y 'ponderacion'.

    Retorna:
    float: El valor calculado del ICA.
    """
    ica = 0.0
    for item in subindices:
        ica += item['subindice'] * item['ponderacion']
    return round(ica, 2)

def clasificar_ica(ica: float) -> str:
    """
    Clasifica el Índice de Calidad del Agua (ICA) en categorías cualitativas.

    Parámetros:
    ica (float): El valor del ICA a clasificar.

    Retorna:
    str: La clasificación cualitativa del ICA.
    """
    if ica >= 91:
        return "Excelente"
    elif ica >= 71:
        return "Buena"
    elif ica >= 51:
        return "Media"  
    elif ica >= 25:
        return "Mala"
    else:
        return "Muy Mala"