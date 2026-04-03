from typing import Callable
import math


# =================================================
# SUBÍNDICES CONTINUOS SEGÚN GRÁFICOS DEL INFORME ICA
# =================================================


# -------------------------------------------------
# Oxígeno disuelto (% de saturación) – Gráfico 1
# -------------------------------------------------
def subindice_oxigeno_disuelto(od_sat: float) -> float:
    if od_sat <= 0:
        return 0.0

    if od_sat >= 100:
        return 100.0

    if od_sat <= 10:
        # 0 → 0 | 10 → 6
        return 0.6 * od_sat

    elif od_sat <= 40:
        # 10 → 6 | 40 → 30
        return 0.8 * od_sat - 2

    elif od_sat <= 90:
        # 40 → 30 | 90 → 90
        return 1.2 * od_sat - 18

    else:
        # 90 → 90 | 100 → 100
        return od_sat



# -------------------------------------------------
# DBO5 (mg/L) – Gráfico 2
# -------------------------------------------------
def subindice_dbo5(dbo: float) -> float:
    """
    dbo: Demanda Bioquímica de Oxígeno (mg/L)
    """
    if dbo <= 0:
        return 100.0
    if dbo > 30:
        return 2.05

    if dbo <= 5:
        return -2*dbo + 100
    elif dbo <= 10:
        return -4*dbo + 110
    elif dbo <= 20:
        return -3*dbo + 100
    else:
        return -2*dbo + 80



# -------------------------------------------------
# pH – Gráfico 3
# -------------------------------------------------
def subindice_ph(ph: float) -> float:
    if ph < 2:
        return 2.02
    if ph > 12:
        return 3.02

    if ph < 3:
        return 20*ph - 20
    elif ph < 4:
        return 20*ph - 40
    elif ph < 5:
        return 30*ph - 80
    elif ph < 6:
        return 20*ph
    elif ph <= 8:
        return -10*(ph - 7)**2 + 100
    elif ph <= 9:
        return -30*ph + 340
    elif ph <= 10:
        return -30*ph + 300
    elif ph <= 11:
        return -20*ph + 240
    else:
        return 3.02



# -------------------------------------------------
# Turbidez (NTU) – Gráfico 4
# -------------------------------------------------
def subindice_turbidez(ntu: float) -> float:
    if ntu <= 10:
        return 100.0
    elif ntu <= 50:
        return 100.0 - 1.5 * (ntu - 10)
    elif ntu <= 200:
        return max(0.0, 40.0 - 0.4 * (ntu - 50))
    else:
        return 0.0


# -------------------------------------------------
# Color (UPC) – Gráfico 5
# -------------------------------------------------
def subindice_color(color: float) -> float:
    if color <= 50:
        return 100.0
    elif color <= 150:
        return 100.0 - 0.6 * (color - 50)
    elif color <= 250:
        return max(0.0, 20.0 - 0.2 * (color - 150))
    else:
        return 0.0


# -------------------------------------------------
# Transparencia (cm) – Gráfico 6
# -------------------------------------------------
def subindice_transparencia(cm: float) -> float:
    if cm <= 10:
        return 0.0
    elif cm <= 35:
        return 4.0 * (cm - 10)
    else:
        return min(100.0, 80.0 + 0.4 * (cm - 35))


# -------------------------------------------------
# Coliformes totales (NMP/100 ml) – Gráfico 7
# -------------------------------------------------
def subindice_coliformes_totales(ct: float) -> float:
    if ct <= 0:
        return 100.0

    if ct < 100:
        return 98.0

    if ct <= 1000:
        # 100 → 98 | 1000 → 70
        return -28 * math.log10(ct) + 154

    if ct <= 10000:
        # 1000 → 70 | 10000 → 10
        return -60 * math.log10(ct) + 250

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

    if clave in _SUBINDICES:
        return round(_SUBINDICES[clave](valor), 2)

    raise ValueError(
        f"El parámetro '{nombre_parametro}' no participa del ICA"
    )
