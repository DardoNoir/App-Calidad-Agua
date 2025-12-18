from typing import Callable


# =================================================
# SUBÍNDICES SEGÚN GRÁFICOS DEL INFORME ICA
# =================================================

# -------------------------------------------------
# Oxígeno disuelto 
# -------------------------------------------------
def subindice_oxigeno_disuelto(valor: float) -> float:
    if valor >= 7.0:
        return 100.0
    elif valor >= 6.0:
        return 80.0
    elif valor >= 5.0:
        return 60.0
    elif valor >= 4.0:
        return 30.0
    elif valor >= 3.0:
        return 10.0
    else:
        return 0.0


# -------------------------------------------------
# DBO5 (mg/L) – Gráfico 2
# -------------------------------------------------
def subindice_dbo5(dbo5: float) -> float:
    if dbo5 <= 3:
        return 100.0
    elif dbo5 <= 6:
        return 80.0
    elif dbo5 <= 10:
        return 60.0
    elif dbo5 <= 20:
        return 30.0
    elif dbo5 <= 30:
        return 10.0
    else:
        return 0.0


# -------------------------------------------------
# pH – Gráfico 3
# -------------------------------------------------
def subindice_ph(ph: float) -> float:
    if 7.0 <= ph <= 8.5:
        return 90.0
    elif 6.5 <= ph < 7.0 or 8.5 < ph <= 9.0:
        return 70.0
    elif 6.0 <= ph < 6.5 or 9.0 < ph <= 9.5:
        return 40.0
    else:
        return 0.0


# -------------------------------------------------
# Turbidez (NTU) – Gráfico 4
# -------------------------------------------------
def subindice_turbidez(ntu: float) -> float:
    if ntu <= 10:
        return 100.0
    elif ntu <= 50:
        return 50.0
    elif ntu <= 100:
        return 30.0
    elif ntu <= 200:
        return 10.0
    else:
        return 0.0


# -------------------------------------------------
# Color (UPC) – Gráfico 5
# -------------------------------------------------
def subindice_color(color: float) -> float:
    if color <= 50:
        return 100.0
    elif color <= 100:
        return 70.0
    elif color <= 150:
        return 40.0
    elif color <= 200:
        return 20.0
    else:
        return 0.0


# -------------------------------------------------
# Transparencia (cm) – Gráfico 6
# -------------------------------------------------
def subindice_transparencia(cm: float) -> float:
    if cm >= 50:
        return 90.0
    elif cm >= 30:
        return 60.0
    elif cm >= 20:
        return 40.0
    elif cm >= 10:
        return 20.0
    else:
        return 0.0


# -------------------------------------------------
# Coliformes totales (NMP/100 ml) – Gráfico 7
# -------------------------------------------------
def subindice_coliformes_totales(nmp: float) -> float:
    if nmp <= 100:
        return 100.0
    elif nmp <= 500:
        return 80.0
    elif nmp <= 1000:
        return 70.0
    elif nmp <= 5000:
        return 30.0
    elif nmp <= 10000:
        return 10.0
    else:
        return 0.0


# =================================================
# DISPATCHER
# =================================================

_SUBINDICES: dict[str, Callable[[float], float]] = {
    "oxígeno disuelto": subindice_oxigeno_disuelto,
    "oxigeno disuelto": subindice_oxigeno_disuelto,
    "od": subindice_oxigeno_disuelto,

    "dbo5": subindice_dbo5,
    "dbo": subindice_dbo5,

    "ph": subindice_ph,

    "turbidez": subindice_turbidez,

    "color": subindice_color,

    "transparencia": subindice_transparencia,

    "coliformes totales": subindice_coliformes_totales,
}


def calcular_subindice_parametro(nombre_parametro: str, valor: float) -> float:
    clave = nombre_parametro.strip().lower()

    for nombre, funcion in _SUBINDICES.items():
        if clave == nombre:
            return funcion(valor)

    raise ValueError(
        f"El parámetro '{nombre_parametro}' no participa del ICA"
    )
