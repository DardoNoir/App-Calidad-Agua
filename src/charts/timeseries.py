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
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y %H:%M"))

    max_ok = min_ok = min_warn = max_warn = None
    if referencia is not None:
        max_ok = referencia.get("limiteMaxAceptable")
        min_ok = referencia.get("limiteMinAceptable")
        min_warn = referencia.get("limiteMinWarning")
        max_warn = referencia.get("limiteMaxWarning")

    if isinstance(max_ok, float):
        ax.axhline(y=max_ok, linestyle="--", color="green", label="Máximo aceptable")

    if isinstance(min_ok, float):
        ax.axhline(y=min_ok, linestyle="--", color="green", label="Mínimo aceptable")

    if isinstance(min_warn, float):
        ax.axhline(y=min_warn, linestyle=":", color="red", label="Mínimo advertencia")

    if isinstance(max_warn, float):
        ax.axhline(y=max_warn, linestyle=":", color="red", label="Máximo advertencia")


    ax.set_xlabel("Fecha de Medición")
    ax.set_ylabel(f"{nombreParametro} ({unidad})")
    ax.set_title(f"{nombreParametro} {titulo}")
    ax.legend()
    ax.grid(True)

    fig.autofmt_xdate(rotation=30)

    return fig


def grafico_parametros_combinados(
    series: list[dict[str, Any]],
    unidad: str,
    titulo: str
):
    
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