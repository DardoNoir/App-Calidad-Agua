from typing import List, TypedDict

class subindice(TypedDict):
    idParametro: int
    subindice: float
    ponderacion: float

def ajustar_ponderaciones(ponderacionesBase: dict[int, float],
                          parametrosMedidos: List[int]) -> dict[int, float]:
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
    ica = 0.0
    for item in subindices:
        ica += item['subindice'] * item['ponderacion']
    return round(ica, 2)

def clasificar_ica(ica: float) -> str:
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