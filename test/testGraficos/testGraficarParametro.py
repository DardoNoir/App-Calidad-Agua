from src.charts.datasource import traerSeriesParametroPorLugar
from src.charts.timeseries import graficarParametro
from src.data.repository import(
    traerParametroPorId,
    traerValoresReferenciaPorParametro
)
import matplotlib.pyplot as plot 

serie = traerSeriesParametroPorLugar(idLugar=2, idParametro=1)

param = traerParametroPorId(1)
if param is None:
    raise ValueError("Parámetro inexistente")

ref = traerValoresReferenciaPorParametro(1)

fig = graficarParametro(
    fechas=[s["fecha"] for s in serie],
    valores=[s["valor"]for s in serie],
    nombreParametro=param["nombreParametro"],
    unidad=param["unidad"],
    referencia=ref,
    titulo="– Río Uruguay"
)

plot.show()  # type: ignore[reportUnknownMemberType]
print("Terminado")