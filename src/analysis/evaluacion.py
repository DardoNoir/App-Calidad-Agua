from typing import TypedDict, Optional

class ReferenciaParametro(TypedDict, total=False):
    """
    Representa los límites permitidos para un parámetro.
    Puede contener:
        - LimiteMax: valor máximo permitido antes de ser "Crítico"
        - LimiteWarning: valor máximo antes de entrar en advertencia ("Warning")
        - LimiteMin: valor mínimo permitido antes de ser "Crítico"
        - LimiteMinWarning: valor mínimo antes de entrar en advertencia ("Warning")
    """
    LimiteMax: Optional[float]
    LimiteWarning: Optional[float]
    limiteMin: Optional[float]
    limiteMinWarning: Optional[float]
    

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
    
    # Caso 0: No hay referencia disponible para el parámetro
    if referencia is None:
        return ("Sin referencia", "")

    limiteMax = referencia.get("LimiteMax")
    limiteWarning = referencia.get("LimiteWarning")
    limiteMin = referencia.get("limiteMin")
    limiteMinWarning = referencia.get("limiteMinWarning")

    # caso 1 está por debajo del mínimo de advertencia → Crítico
    if limiteMinWarning is not None and limiteMin is not None and valor < limiteMinWarning:
        desvio = abs(limiteMin - valor)
        mensaje = (
            f"Valor por debajo del mínimo aceptable ({limiteMin}). "
            f"Se desvía en {desvio:.2f}"
        )
        return ("Crítico", mensaje)

    # caso 2 está por debajo del mínimo permitido, pero no del de advertencia → Warning
    if limiteMin is not None and valor < limiteMin:
        desvio = abs(limiteMin - valor)
        mensaje = (
            f"Valor por debajo del mínimo aceptable ({limiteMin}). "
            f"Se desvía en {desvio:.2f}"
        )
        return ("Warning", mensaje)

    
    # Caso 3 está por encima del máximo permitido, pero no del de advertencia → Warning 
    if limiteMax is not None and valor > limiteMax and limiteWarning is not None and valor < limiteWarning:
        desvio = valor - limiteMax
        mensaje = (
            f"Valor supera el máximo aceptable ({limiteMax}). "
            f"Se desvía en {desvio:.2f}"
        )
        return ("Warning", mensaje)

    # Caso 4 está por encima del máximo de advertencia → Crítico
    if limiteWarning is not None and valor > limiteWarning and limiteMax is not None:
        desvio = valor - limiteMax
        mensaje = (
            f"Valor supera el nivel de advertencia ({limiteWarning}). "
            f"Se desvía en {desvio:.2f}"
        )
        return ("Crítico", mensaje)

    # Caso 4: Todo dentro de los valores normales
    return ("Aceptable", "")
