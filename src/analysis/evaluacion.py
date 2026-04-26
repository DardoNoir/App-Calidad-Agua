from typing import TypedDict, Optional


class ReferenciaParametro(TypedDict, total=False):
    limite_min_aceptable: Optional[float]
    limite_max_aceptable: Optional[float]
    limite_min_warning: Optional[float]
    limite_max_warning: Optional[float]
   


def EvaluarParametro(valor: float, referencia: Optional[ReferenciaParametro] | None):
    if not referencia:
        return ("Sin referencia", "")

    limiteMin = referencia.get("limite_min_aceptable")
    limiteMax = referencia.get("limite_max_aceptable")
    limiteMinWarning = referencia.get("limite_min_warning")
    limiteMaxWarning = referencia.get("limite_max_warning")
    
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
