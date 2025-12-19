from matplotlib.figure import Figure
from pathlib import Path

def guardar_figura(fig: Figure, ruta: Path) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(str(ruta), bbox_inches="tight")  # type: ignore[misc]
