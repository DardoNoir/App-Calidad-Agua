from typing import Dict, List, Tuple
from scipy.interpolate import PchipInterpolator
import numpy as np


class CurvaSubindice:
    def __init__(self, puntos: List[Tuple[float, float]]):
        if len(puntos) < 2:
            raise ValueError("Se necesitan al menos 2 puntos para interpolar.")

        # Ordenar por valor medido
        puntos = sorted(puntos, key=lambda x: x[0])

        self.x = np.array([p[0] for p in puntos])
        self.y = np.array([p[1] for p in puntos])

        # Interpolador tipo PCHIP (monótono, sin oscilaciones)
        self.interpolador = PchipInterpolator(self.x, self.y, extrapolate=True)

    def calcular(self, valor: float) -> float:
        resultado = float(self.interpolador(valor))

        # Limitar entre 0 y 100 por seguridad
        return round(max(0.0, min(100.0, resultado)), 2)


# =====================================================
# REGISTRO GLOBAL DE CURVAS
# =====================================================

_CURVAS: Dict[str, CurvaSubindice] = {}


def registrar_curva(nombre_parametro: str,
                    puntos: List[Tuple[float, float]]):
    """
    Registra una curva de subíndice para un parámetro.
    """
    clave = nombre_parametro.strip().lower()
    _CURVAS[clave] = CurvaSubindice(puntos)


def calcular_subindice_parametro(nombre_parametro: str,
                                 valor: float) -> float:
    clave = nombre_parametro.strip().lower()

    if clave not in _CURVAS:
        raise ValueError(f"No hay curva definida para '{nombre_parametro}'")

    return _CURVAS[clave].calcular(valor)