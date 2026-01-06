from src.charts.datasource import traerSeriesParametroPorLugar
from src.charts.timeseries import graficarParametro
from src.data.repository import(
    traerParametroPorId,
    traerValoresReferenciaPorParametro
)
import matplotlib.pyplot as plot 

serie = traerSeriesParametroPorLugar(idLugar=1, idParametro=4)

param = traerParametroPorId(4)
if param is None:
    raise ValueError("Parámetro inexistente")

ref = traerValoresReferenciaPorParametro(4)

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