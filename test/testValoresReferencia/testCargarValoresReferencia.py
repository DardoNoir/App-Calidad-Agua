from src.data.repository import (
    insertarValoresReferencia,
    traerParametroPorNombre)

def pruebaCargarValoresReferencia():
    print("=== PRUEBA CARGAR VALORES DE REFERENCIA ===")

    print("Nombre del parámetro: ")
    nombre_parametro = input().strip()
    parametro = traerParametroPorNombre(nombre_parametro)
    if not parametro:
        print(f"No se encontró el parámetro con nombre '{nombre_parametro}'.")
        return
    print("Límite máximo aceptable: ")
    limite_max_aceptable = float(input().strip())
    print("Límite mínimo aceptable: ")
    limite_min_aceptable = float(input().strip())
    print("Límite máximo de advertencia: ")
    limite_max_warning = float(input().strip())
    print("Límite mínimo de advertencia: ")
    limite_min_warning = float(input().strip())
    print("Normativa asociada: ")
    normativa = input().strip()

    insertarValoresReferencia(
        idParametro=parametro["id"],limiteMaxAceptable=limite_max_aceptable,
        limiteMinAceptable=limite_min_aceptable, limiteMaxWarning=limite_max_warning,
        limiteMinWarning=limite_min_warning, normativa=normativa)
    
    print(f"Valores de referencia para '{nombre_parametro}' cargados exitosamente.")
