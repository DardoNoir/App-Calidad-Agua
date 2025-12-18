from src.data.repository import (
    insertarPonderacionParametro,
    traerParametroPorNombre,
)

def cargarPonderaciones():
    print("=== PRUEBA CARGAR PONDERACIONES ===")

    nombreParametro = input("Parametro a Ponderar: ").strip()
    parametro = traerParametroPorNombre(nombreParametro)
    if not parametro:
        print(f"No se encontró el parámetro con nombre '{nombreParametro}'.")
        return

    valor = float(input(f"Ingrese Ponderación de {nombreParametro}: "))
    if valor < 0 or valor > 1:
        print(f"Ponderación NO valida")
        return
    
    insertarPonderacionParametro(parametro["id"],valor)
    print(f"Ponderación de '{nombreParametro}' cargada exitosamente.")

if __name__ == "__main__":
    cargarPonderaciones()