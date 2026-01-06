from src.data.repository import (
    traerValoresMedidosDeMedicion,
    traerPonderacionesParametroActivas,
    actualizarICAMedicion,
)

from src.analysis.calculoIca import (
    calcular_ica,
    clasificar_ica,
    ajustar_ponderaciones
)
from src.analysis.subindices import calcular_subindice_parametro

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
    # 2. Traer ponderaciones base (FIJAS)
    # -------------------------------------------------
    ponderaciones = traerPonderacionesParametroActivas()
    if not ponderaciones:
        print("No hay ponderaciones configuradas")
        return

    ponderaciones_base = {
        p["idParametro"]: p["ponderacion"]
        for p in ponderaciones
    }

    # -------------------------------------------------
    # 3. Detectar parámetros medidos
    # -------------------------------------------------
    parametros_medidos = [
        v["idParametro"]
        for v in valores
        if v["idParametro"] in ponderaciones_base
    ]

    if not parametros_medidos:
        print("Ningún parámetro medido participa del ICA")
        return

    # -------------------------------------------------
    # 4. Ajustar ponderaciones (redistribución)
    # -------------------------------------------------
    try:
        ponderaciones_ajustadas = ajustar_ponderaciones(
            ponderaciones_base,
            parametros_medidos
        )
    except ValueError as e:
        print(str(e))
        return

    # -------------------------------------------------
    # 5. Construcción de subíndices
    # -------------------------------------------------
    subindices: List[SubIndiceICA] = []

    print("\n--- Subíndices (ponderaciones ajustadas) ---")

    for v in valores:
        idParametro = v["idParametro"]
        nombre = v["nombreParametro"]
        valor = v["valor"]

        if idParametro not in ponderaciones_ajustadas:
            print(f"Parámetro {nombre} no participa del ICA")
            continue

        try:
            sub = calcular_subindice_parametro(nombre, valor)
        except ValueError as e:
            print(str(e))
            continue

        ponderacion = ponderaciones_ajustadas[idParametro]

        subindices.append({
            "idParametro": idParametro,
            "subindice": sub,
            "ponderacion": ponderacion
        })

        print(
            f"{nombre} → "
            f"Valor: {valor} | "
            f"Subíndice: {sub} | "
            f"Ponderación ajustada: {ponderacion:.3f}"
        )

    if not subindices:
        print("No se pudo calcular ningún subíndice")
        return

    # -------------------------------------------------
    # 6. Cálculo ICA
    # -------------------------------------------------
    ica = calcular_ica(subindices)
    clasificacion = clasificar_ica(ica)

    # -------------------------------------------------
    # 7. Persistencia
    # -------------------------------------------------
    actualizarICAMedicion(
        idMedicion=idMedicion,
        ica=ica,
        clasificacionICA=clasificacion
    )

    # -------------------------------------------------
    # 8. Resultado
    # -------------------------------------------------
    print("\n=== RESULTADO ICA ===")
    print(f"ICA: {ica:.2f}")
    print(f"Clasificación: {clasificacion}")
    print("✔ ICA calculado y guardado correctamente")


if __name__ == "__main__":
    testCalcularICA()
