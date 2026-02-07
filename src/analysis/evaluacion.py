from typing import TypedDict, Optional


class ReferenciaParametro(TypedDict, total=False):
    limiteMinAceptable: Optional[float]
    limiteMaxAceptable: Optional[float]
    limiteMinWarning: Optional[float]
    limiteMaxWarning: Optional[float]


def EvaluarParametro(valor: float, referencia: Optional[ReferenciaParametro] | None):
    """
    Estados posibles:
    - Crítico
    - Warning
    - Aceptable
    - Sin referencia
    """

    if not referencia:
        return ("Sin referencia", "")

    limiteMin = referencia.get("limiteMinAceptable")
    limiteMax = referencia.get("limiteMaxAceptable")
    limiteMinWarning = referencia.get("limiteMinWarning")
    limiteMaxWarning = referencia.get("limiteMaxWarning")

    # ===== CRÍTICOS =====
    if limiteMinWarning is not None and valor < limiteMinWarning:
        desvio = limiteMinWarning - valor
        return (
            "Crítico",
            f"Valor por debajo del mínimo crítico ({limiteMinWarning}). "
            f"Desvío: {desvio:.2f}"
        )

    if limiteMaxWarning is not None and valor > limiteMaxWarning:
        desvio = valor - limiteMaxWarning
        return (
            "Crítico",
            f"Valor por encima del máximo crítico ({limiteMaxWarning}). "
            f"Desvío: {desvio:.2f}"
        )

    # ===== WARNING =====
    if limiteMin is not None and valor < limiteMin:
        desvio = limiteMin - valor
        return (
            "Warning",
            f"Valor por debajo del mínimo aceptable ({limiteMin}). "
            f"Desvío: {desvio:.2f}"
        )

    if limiteMax is not None and valor > limiteMax:
        desvio = valor - limiteMax
        return (
            "Warning",
            f"Valor por encima del máximo aceptable ({limiteMax}). "
            f"Desvío: {desvio:.2f}"
        )

    # ===== ACEPTABLE =====
    return ("Aceptable", "")
