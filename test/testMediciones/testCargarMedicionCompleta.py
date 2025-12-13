from datetime import datetime

from src.data.repository import (
    traerUsuarioPorId,
    insertarLugar,
    traerLugares,
    traerParametros,
    insertarMedicion,
    insertarValorMedido,
    traerValoresReferenciaPorParametro,
)

from src.analysis.evaluacion import EvaluarParametro

from typing import TypedDict


class ValorMedido(TypedDict):
    idParametro: int
    nombre: str
    valor: float


class ValorEvaluado(ValorMedido):
    estado: str
    desviacion: str

def testCargarMedicionCompleta():
    print("=== CARGAR MEDICIÓN COMPLETA ===")

    # -------------------------------------------------
    # Usuario
    # -------------------------------------------------
    usuarioId = 1  # hardcodeado para el test
    usuario = traerUsuarioPorId(usuarioId)

    if not usuario:
        raise ValueError("Usuario no encontrado")

    print(f"Usuario que carga la medición: {usuario['nombreUsuario']}")

    # -------------------------------------------------
    # Lugar
    # -------------------------------------------------
    input("Presione Enter para cargar un cuerpo de agua...")

    provincia = input("Provincia: ").strip()
    ciudad = input("Ciudad: ").strip()
    cuerpoAgua = input("Cuerpo de agua: ").strip()

    insertarLugar(provincia, ciudad, cuerpoAgua)

    lugarId = None
    for lugar in traerLugares():
        if (
            lugar["provincia"] == provincia
            and lugar["ciudad"] == ciudad
            and lugar["cuerpoAgua"] == cuerpoAgua
        ):
            lugarId = lugar["id"]
            break

    if lugarId is None:
        raise RuntimeError("No se pudo obtener el ID del lugar")

    # -------------------------------------------------
    # Fecha
    # -------------------------------------------------
    fechaMedicion = datetime.now()
    print(f"Fecha y hora de la medición: {fechaMedicion}")

    # -------------------------------------------------
    # 1. Recolección de valores
    # -------------------------------------------------
    parametros = traerParametros()
    if not parametros:
        raise RuntimeError("No hay parámetros cargados en el sistema")

    valores_medidos: list[ValorMedido] = []

    print("\n--- Ingreso de valores ---")
    for parametro in parametros:
        try:
            valor = float(
                input(
                    f"Parametro: {parametro["nombreParametro"]}({parametro['unidad']}): "
                )
            )
        except ValueError:
            print("Valor inválido. Se omite el parámetro.")
            continue

        valores_medidos.append(
            {
                "idParametro": parametro["id"],
                "nombre": parametro["nombreParametro"],
                "valor": valor,
            }
        )

    if not valores_medidos:
        print("No se ingresaron valores. Operación cancelada.")
        return

    # -------------------------------------------------
    # 2. Evaluación
    # -------------------------------------------------
    valores_evaluados: list[ValorEvaluado] = []

    print("\n--- Evaluación ---")
    for v in valores_medidos:
        ref = traerValoresReferenciaPorParametro(v["idParametro"])

        estado, desvio = EvaluarParametro(v["valor"], ref)

        valores_evaluados.append(
            {
                "idParametro": v["idParametro"],
                "nombre": v["nombre"],
                "valor": v["valor"],
                "estado": estado,
                "desviacion": desvio,
            }
        )

        print(
            f"Parámetro {v['nombre']} → "
            f"Estado: {estado} | Desvío: {desvio}"
        )

    # -------------------------------------------------
    # 3. Persistencia
    # -------------------------------------------------
    print("\n--- Guardando medición ---")

    medicionId = insertarMedicion(
        idLugar=lugarId,
        fechaMedicion=fechaMedicion,
        medidaTomadaPor=usuarioId,
        comentarios="test carga completa",
    )

    for v in valores_evaluados:
        insertarValorMedido(
            medicionId,
            [{"idParametro": v["idParametro"]}],
            v["valor"],
            v["estado"],
            v["desviacion"],
        )

    print("\n✔ Medición completa cargada exitosamente")
    print(f"ID de medición: {medicionId}")


if __name__ == "__main__":
    testCargarMedicionCompleta()
