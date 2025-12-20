from src.charts.datasource import traerSeriesParametroPorLugar
from src.charts.timeseries import grafico_parametros_combinados
from src.data.repository import traerParametroPorId

import matplotlib.pyplot as plot


def test_grafico_parametros_combinados():
    idLugar = 1

    # Parámetros a combinar (deben tener la MISMA unidad)
    parametros_ids = [2, 4]  # ejemplo: Nitratos, Nitritos, Fosfatos

    series = []
    unidad = None

    for idParametro in parametros_ids:
        serie = traerSeriesParametroPorLugar(
            idLugar=idLugar,
            idParametro=idParametro
        )

        if not serie:
            print(f"⚠ No hay datos para el parámetro {idParametro}")
            continue

        param = traerParametroPorId(idParametro)
        if param is None:
            raise ValueError(f"Parámetro {idParametro} inexistente")

        # Validar que todos tengan la misma unidad
        if unidad is None:
            unidad = param["unidad"]
        elif unidad != param["unidad"]:
            raise ValueError(
                f"Unidad incompatible: {param['nombreParametro']} "
                f"({param['unidad']}) ≠ {unidad}"
            )

        series.append( # type: ignore
            {
                "nombre": param["nombreParametro"],
                "fechas": [s["fecha"] for s in serie],
                "valores": [s["valor"] for s in serie],
            }
        )

    if not series:
        raise RuntimeError("No hay series válidas para graficar")

    fig = grafico_parametros_combinados( # type: ignore
        series=series, # type: ignore
        unidad=unidad, # type: ignore
        titulo="Parámetros combinados – Río Uruguay"
    )

    plot.show()  # type: ignore[reportUnknownMemberType]
    print("✔ Gráfico combinado terminado")


if __name__ == "__main__":
    test_grafico_parametros_combinados()
