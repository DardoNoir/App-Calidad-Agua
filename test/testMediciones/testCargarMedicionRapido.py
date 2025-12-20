from datetime import datetime

from src.data.repository import (
    traerUsuarioPorId,
    traerLugarPorId,
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
    print("=== CARGAR MEDICIÓN ===")

    # -------------------------------------------------
    # Usuario
    # -------------------------------------------------
    usuario = traerUsuarioPorId(1)

    if not usuario:
        raise ValueError("Usuario no encontrado")

    print(f"Usuario que carga la medición: {usuario['nombreUsuario']}")

    # -------------------------------------------------
    # Lugar
    # -------------------------------------------------
    lugar = traerLugarPorId(1)

    if lugar is None:
        raise RuntimeError("No se pudo obtener el ID del lugar")
    
    print(f"Río a Medir: {lugar["cuerpoAgua"]}")

   # -------------------------------------------------
# Fecha
# -------------------------------------------------
    print("\n--- Fecha de la medición ---")
    print("Formato permitido:")
    print("  - DD/MM/AAAA")
    print("  - DD/MM/AAAA HH:MM")
    print("Presione ENTER para usar la fecha actual\n")

    fecha_input = input("Ingrese fecha de medición: ").strip()

    if not fecha_input:
        fechaMedicion = datetime.now()
    else:
        try:
            if len(fecha_input) == 10:
                # DD/MM/AAAA
                fechaMedicion = datetime.strptime(fecha_input, "%d/%m/%Y")
            else:
                # DD/MM/AAAA HH:MM
                fechaMedicion = datetime.strptime(fecha_input, "%d/%m/%Y %H:%M")
        except ValueError:
            raise ValueError(
            "Formato de fecha inválido. Use DD/MM/AAAA o DD/MM/AAAA HH:MM"
        )

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
        idLugar=lugar["id"],
        fechaMedicion=fechaMedicion,
        medidaTomadaPor=1,
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
