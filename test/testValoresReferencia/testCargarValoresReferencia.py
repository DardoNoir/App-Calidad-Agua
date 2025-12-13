from src.data.repository import (
    insertarValoresReferencia,
    traerParametroPorNombre)

def pruebaCargarValoresReferencia():
    print("=== PRUEBA CARGAR VALORES DE REFERENCIA ===")

    nombre_parametro = input("Nombre del parámetro: ").strip()
    parametro = traerParametroPorNombre(nombre_parametro)
    if not parametro:
        print(f"No se encontró el parámetro con nombre '{nombre_parametro}'.")
        return
    limite_min_aceptable = float(input("Límite mínimo aceptable: ").strip())
    limite_max_aceptable = float(input("Límite máximo aceptable: ").strip())
    limite_min_warning = float(input("Límite mínimo de advertencia: ").strip())
    limite_max_warning = float(input("Límite máximo de advertencia: ").strip())
    normativa = input("Normativa asociada: ").strip()

    insertarValoresReferencia(
        idParametro=parametro["id"],limiteMaxAceptable=limite_max_aceptable,
        limiteMinAceptable=limite_min_aceptable, limiteMaxWarning=limite_max_warning,
        limiteMinWarning=limite_min_warning, normativa=normativa)
    
    print(f"Valores de referencia para '{nombre_parametro}' cargados exitosamente.")

if __name__ == "__main__":
    pruebaCargarValoresReferencia()
