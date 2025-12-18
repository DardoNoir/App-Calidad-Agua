from src.data.repository import(
    traerTodosLosValoresReferencia,
    traerParametroPorId)

def listarValoresReferencia():
    referencias = traerTodosLosValoresReferencia()

    for ref in referencias:
        parametro = traerParametroPorId(ref["idParametro"])

        if parametro is None:
            print(f"⚠️ Parámetro no encontrado (ID {ref['idParametro']})")
            continue

        print(f"--- Valores de Referencia ---")
        print(f"Id Parametro: {ref['idParametro']}")
        print(f"Nombre: {parametro['nombreParametro']}")
        print(f"Máximo Aceptable: {ref['limiteMaxAceptable']}")
        print(f"Mínimo Aceptable: {ref['limiteMinAceptable']}")
        print(f"Máximo Advertencia: {ref['limiteMaxWarning']}")
        print(f"Mínimo Advertencia: {ref['limiteMinWarning']}")

    input("Enter para terminar: ")


if __name__ == "__main__":
    listarValoresReferencia()