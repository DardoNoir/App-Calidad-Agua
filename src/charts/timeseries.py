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

    fig: Figure
    ax: Axes
    fig, ax = plt.subplots(figsize=(8, 5))

    fechas_mpl = mdates.date2num(fechas)

    ax.plot(
        fechas_mpl,
        valores,
        marker="o",
        label=nombreParametro
    )

    # 👉 FORMATO DE FECHA
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y"))

    if referencia is not None:
        limite_max = referencia.get("LimiteMax")
        if isinstance(limite_max, float):
            ax.axhline(
                y=limite_max,
                linestyle="--",
                color="green",
                label="Máximo Aceptable"
            )

        # ⚠️ BUG CORREGIDO (ver punto 2)
        limite_min = referencia.get("limiteMin")
        if isinstance(limite_min, float):
            ax.axhline(
                y=limite_min,
                linestyle="--",
                color="green",
                label="Mínimo Aceptable"
            )

        min_warning = referencia.get("limiteMinWarning")
        if isinstance(min_warning, float):
            ax.axhline(
                y=min_warning,
                linestyle=":",
                color="red",
                label="Mínimo Advertencia"
            )

        max_warning = referencia.get("LimiteWarning")
        if isinstance(max_warning, float):
            ax.axhline(
                y=max_warning,
                linestyle=":",
                color="red",
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
