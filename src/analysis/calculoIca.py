from typing import List, TypedDict

class subindice(TypedDict):
    idParametro: int
    subindice: float
    ponderacion: float

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