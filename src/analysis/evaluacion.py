from typing import TypedDict, Optional

class ReferenciaParametro(TypedDict,total=False):
    LimiteMax:Optional[float]
    LimiteWarning:Optional[float]
    
def EvaluarParametro(valor: float, referencia: Optional[ReferenciaParametro] | None):
    if referencia is None:
        return ("Sin referencia", "")

    limiteMax = referencia.get("LimiteMax")
    limiteWarning = referencia.get("LimiteWarning")

    if limiteMax is not None and valor > limiteMax:
        desvio = valor - limiteMax
        mensaje = (
            f"Valor supera el máximo aceptable ({limiteMax}). "
            f"Se desvía en {desvio}"
        )
        return ("Fuera de norma", mensaje)

    if limiteWarning is not None and valor > limiteWarning:
        return ("Warning", f"Valor supera el nivel de advertencia ({limiteWarning})")

    return ("Normal", "")
