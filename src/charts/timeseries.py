from typing import Optional, Sequence, Any
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.figure import Figure
from matplotlib.axes import Axes
from decimal import Decimal

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

    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m/%Y %H:%M"))

    max_ok = min_ok = min_warn = max_warn = None
    if referencia is not None:
        max_ok = referencia.get("limite_max_aceptable")
        min_ok = referencia.get("limite_min_aceptable")
        min_warn = referencia.get("limite_min_warning")
        max_warn = referencia.get("limite_max_warning")

    def add_line(y, style, color, label):
        if isinstance(y, (int, float, Decimal)):
            handles, labels = ax.get_legend_handles_labels()
            label_final = label if label not in labels else ""
            ax.axhline(
                y=float(y),
                linestyle = style,
                color = color,
                label = label_final,
            )

    add_line(max_ok, "--", "green", "Máximo Aceptable")
    add_line(min_ok, "--", "green", "Mínimo Aceptable")
    add_line(max_warn, ":", "red", "Máximo Advertencia")
    add_line(min_warn, ":", "red", "Mínimo Advertencia")

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