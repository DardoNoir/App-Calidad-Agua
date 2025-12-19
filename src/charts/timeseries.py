# pyright: reportUnknownMemberType=false
# pyright: reportUnknownVariableType=false
# pyright: reportUnknownArgumentType=false

from typing import Optional, Sequence, Any
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.axes import Axes

from src.analysis.evaluacion import ReferenciaParametro


def graficarParametro(
    fechas: Sequence[datetime],
    valores: Sequence[float],
    nombreParametro: str,
    unidad: str,
    referencia: Optional[ReferenciaParametro] = None,
    titulo: str = ""
) -> Figure:
    """
    Devuelve una figura matplotlib con:
    - Serie temporal del parámetro
    - Límites de referencia (si existen)
    """

    fig: Figure
    ax: Axes
    fig, ax = plt.subplots()

    # Convertir fechas a formato matplotlib (para tipado correcto)
    fechas_mpl = mdates.date2num(fechas)

    ax.plot(fechas_mpl, valores, marker="o", label=nombreParametro)

    if referencia is not None:
        limite_max = referencia.get("LimiteMax")
        if isinstance(limite_max, float):
            ax.axhline(
                y=limite_max,
                linestyle="--",
                label="Máximo Aceptable"
            )

        limite_min = referencia.get("LimiteMin")
        if isinstance(limite_min, float):
            ax.axhline(
                y=limite_min,
                linestyle="--",
                label="Mínimo Aceptable"
            )

        min_warning = referencia.get("limiteMinWarning")
        if isinstance(min_warning, float):
            ax.axhline(
                y=min_warning,
                linestyle=":",
                label="Mínimo Advertencia"
            )

        max_warning = referencia.get("limiteMaxWarning")
        if isinstance(max_warning, float):
            ax.axhline(
                y=max_warning,
                linestyle=":",
                label="Máximo Advertencia"
            )

    ax.set_xlabel("Fecha de Medición")
    ax.set_ylabel(f"{nombreParametro} ({unidad})")
    ax.set_title(f"{nombreParametro} {titulo}")
    ax.legend()
    ax.grid(True)

    fig.autofmt_xdate()

    return fig

def grafico_parametros_combinados(
    series: list[dict[str, Any]],
    unidad: str,
    titulo: str
):
    """
    series = [
      {
        "nombre": "Nitratos",
        "fechas": [...],
        "valores": [...]
      }
    ]
    """
    fig = plt.figure()

    for s in series:
        plt.plot(
            s["fechas"],
            s["valores"],
            marker="o",
            label=s["nombre"]
        )

    plt.xlabel("Fecha")
    plt.ylabel(unidad)
    plt.title(titulo)
    plt.legend()
    plt.grid(True)

    return fig
