from src.data.repository import (
    traerValoresMedidosDeMedicion,
    traerPonderacionesParametroActivas,
    actualizarICAMedicion,
)

from src.analysis.calculoIca import calcular_ica, clasificar_ica

from typing import TypedDict, List


class SubIndiceICA(TypedDict):
    idParametro: int
    subindice: float
    ponderacion: float


def testCalcularICA():
    print("=== PRUEBA CÁLCULO ICA ===")

    # -------------------------------------------------
    # 1. Selección de medición
    # -------------------------------------------------
    try:
        idMedicion = int(input("Ingrese ID de la medición: "))
    except ValueError:
        print("ID inválido")
        return

    valores = traerValoresMedidosDeMedicion(idMedicion)
    if not valores:
        print("La medición no tiene valores asociados")
        return

    # -------------------------------------------------
    # 2. Traer ponderaciones activas
    # -------------------------------------------------
    ponderaciones = traerPonderacionesParametroActivas()
    if not ponderaciones:
        print("No hay ponderaciones configuradas")
        return

    for p in ponderaciones:
        for v in valores:
            if p["idParametro"] == v["idParametro"]:
                print(f"Parámetro {v['nombreParametro']} tiene ponderación {p['ponderacion']}")
                print(f"Mantiene el valor de la ponderación? (s/n): ", end="")
                respuesta = input().strip().lower()
                if respuesta == "n":
                    try:
                        nueva_ponderacion = float(input("Ingrese nueva ponderación: "))
                        p["ponderacion"] = nueva_ponderacion
                    except ValueError:
                        print("Ponderación inválida, se mantiene la anterior.")
                break

    ponderacionesPorParametro = {
        p["idParametro"]: p["ponderacion"] for p in ponderaciones
    }

    # -------------------------------------------------
    # 3. Construcción de subíndices
    # -------------------------------------------------
    subindices: List[SubIndiceICA] = []

    print("\n--- Subíndices ---")
    for v in valores:
        idParametro = v["idParametro"]

        if idParametro not in ponderacionesPorParametro:
            print(
                f"Parámetro {v['nombreParametro']} no participa del ICA"
            )
            continue

        sub = int(input(f"Ingrese subíndice calculado para {v['nombreParametro']}: "))

        ponderacion = ponderacionesPorParametro[idParametro]

        subindices.append({
            "idParametro": idParametro,
            "subindice": sub,
            "ponderacion": ponderacion
        })

        print(
            f"{v['nombreParametro']} → "
            f"Valor: {v['valor']} | Sub: {sub} | Ponderación: {ponderacion}"
        )

    if not subindices:
        print("No se pudo calcular ningún subíndice")
        return

    # -------------------------------------------------
    # 4. Cálculo ICA
    # -------------------------------------------------
    ica = calcular_ica(subindices)
    clasificacion = clasificar_ica(ica)

    # -------------------------------------------------
    # 5. Persistencia
    # -------------------------------------------------
    actualizarICAMedicion(
        idMedicion=idMedicion,
        ica=ica,
        clasificacionICA=clasificacion
    )

    # -------------------------------------------------
    # 6. Resultado
    # -------------------------------------------------
    print("\n=== RESULTADO ICA ===")
    print(f"ICA: {ica}")
    print(f"Clasificación: {clasificacion}")
    print("✔ ICA calculado y guardado correctamente")


if __name__ == "__main__":
    testCalcularICA()
