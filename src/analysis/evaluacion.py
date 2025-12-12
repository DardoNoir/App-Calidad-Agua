from typing import TypedDict, Optional

class ReferenciaParametro(TypedDict, total=False):
    """
    Representa los límites permitidos para un parámetro.
    Puede contener:
        - LimiteMax: valor máximo permitido antes de ser "Fuera de norma"
        - LimiteWarning: valor máximo antes de entrar en advertencia ("Warning")
    """
    LimiteMax: Optional[float]
    LimiteWarning: Optional[float]
    

def EvaluarParametro(valor: float, referencia: Optional[ReferenciaParametro] | None):
    """
    Evalúa el estado de un valor medido comparándolo con los límites de referencia.
    
    Reglas:
    ------------------------------------
    1. Si no existe referencia → ("Sin referencia", "")

    2. Si hay limiteMax y valor > limiteMax:
         estado = "Fuera de norma"
         desviacion = cuánto se pasó del límite máximo

    3. Si hay limiteWarning y valor > limiteWarning:
         estado = "Warning"

    4. Si no supera ningún límite:
         estado = "Normal"
    """
    
    # Caso 1: No hay referencia disponible para el parámetro
    if referencia is None:
        return ("Sin referencia", "")

    limiteMax = referencia.get("LimiteMax")
    limiteWarning = referencia.get("LimiteWarning")

    # Caso 2: Está pasado del máximo permitido → Crítico
    if limiteMax is not None and valor > limiteMax and limiteWarning is not None and valor < limiteWarning:
        desvio = valor - limiteMax
        mensaje = (
            f"Valor supera el máximo aceptable ({limiteMax}). "
            f"Se desvía en {desvio:.2f}"
        )
        return ("Warning", mensaje)

    # Caso 3: Supera el warning pero no el máximo
    if limiteWarning is not None and valor > limiteWarning and limiteMax is not None:
        desvio = valor - limiteMax
        mensaje = (
            f"Valor supera el nivel de advertencia ({limiteWarning}). "
            f"Se desvía en {desvio:.2f}"
        )
        return ("Crítico", mensaje)

    # Caso 4: Todo dentro de los valores normales
    return ("Normal", "")
