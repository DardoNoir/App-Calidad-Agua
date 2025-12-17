from typing import Callable


# Subindice ICA del pH
def subindice_ph(valor_ph: float) -> float:
    if 6.5 <= valor_ph <= 8.5:
        return 100.0    
    elif 6.0 <= valor_ph < 6.5 or 8.5 < valor_ph <= 9.0:
        return 70.0
    else:
        return 30.0
    
# Subindice ICA del Oxígeno Disuelto
def subindice_oxigeno_disuelto(valor_od: float) -> float:
    if 5.0 <= valor_od <= 12.0:
        return 100.0
    elif 4.0 <= valor_od < 5.0 or 12.0 < valor_od <= 15.0:
        return 70.0
    else:
        return 30.0 

# Subindice ICA de DBO5
def subindice_dbo5(valor_dbo5: float) -> float:
    if 2.9 <= valor_dbo5 <= 3.1:
        return 100.0
    elif 2.75 <= valor_dbo5 < 2.9 or 3.1 < valor_dbo5 <= 3.25:
        return 70.0
    else:
        return 30.0
    
# Subindice ICA de Sólidos Coliformes Totales
def subindice_coliformes_totales(valor_ct: float) -> float:
    if 4800.0 <= valor_ct <= 5200.0:
        return 100.0
    elif 4500.0 <= valor_ct < 4800.0 or 5200.0 < valor_ct <= 5500.0:
        return 70.0
    else:
        return 30.0

_SUBINDICES: dict[str, Callable[[float], float]] = {
    "ph": subindice_ph,
    "pH": subindice_ph,

    "oxígeno disuelto": subindice_oxigeno_disuelto,
    "oxigeno disuelto": subindice_oxigeno_disuelto,
    "od": subindice_oxigeno_disuelto,

    "dbo": subindice_dbo5,
    "dbo5": subindice_dbo5,

    "coliformes totales": subindice_coliformes_totales,
    "sólidos coliformes totales": subindice_coliformes_totales,
}


def calcular_subindice_parametro(nombre_parametro: str, valor: float) -> float:
    """
    Calcula el subíndice ICA (0–100) para un parámetro dado.

    Lanza ValueError si el parámetro no participa del ICA.
    """

    clave = nombre_parametro.strip().lower()

    for nombre, funcion in _SUBINDICES.items():
        if clave == nombre.lower():
            return funcion(valor)

    raise ValueError(
        f"El parámetro '{nombre_parametro}' no tiene "
        "subíndice ICA definido"
    )