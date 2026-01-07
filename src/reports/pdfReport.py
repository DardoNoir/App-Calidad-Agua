from typing import Optional, List
from pathlib import Path
#from tempfile import TemporaryDirectory
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable

from src.data.repository import(
    traerLugarPorId,
    traerMedicionPorId,
    traerUsuarioPorId,
    traerValoresMedidosDeMedicion,
    #traerValoresReferenciaPorParametro,
)

from src.reports.tables import crearTablaValoresMedidos

"""
from src.charts.timeseries import graficarParametro
from src.charts.exporter import guardar_figura
"""


def generarReporte(idMedicion: int, rutaGuardar: Path, db_path: Optional[str] = None) -> Path:
    medicion = traerMedicionPorId(idMedicion, db_path)
    if medicion is None:
        raise RuntimeError("Medición no encontrada")

    lugar = traerLugarPorId(medicion["idLugar"], db_path)
    if lugar is None:
        raise RuntimeError("Lugar no encontrado")

    usuario = traerUsuarioPorId(medicion["medidaTomadaPor"], db_path)
    if usuario is None:
        raise RuntimeError("Usuario no encontrado")
    valores = traerValoresMedidosDeMedicion(idMedicion, db_path)
    if not valores:
        raise RuntimeError("La medición no tiene valores cargados")

    doc = SimpleDocTemplate(str(rutaGuardar))
    styles = getSampleStyleSheet()
    elementos: List[Flowable] = []

    elementos.append(Paragraph(f"Reporte de Medición: {medicion['id']}", styles['Title']))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph(f"Lugar: {lugar['provincia']} - {lugar['ciudad']} - {lugar['cuerpoAgua']}",
        styles["Normal"]))
    elementos.append(Paragraph(f"Fecha de Medición: {medicion['fechaMedicion']}", styles["Normal"]))
    elementos.append(Paragraph(f"Medida Tomada Por: {usuario['nombreUsuario']}", styles["Normal"]))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Valores Medidos:", styles['Heading2']))
    tabla_valores = crearTablaValoresMedidos(valores)

    elementos.append(tabla_valores)
    elementos.append(Spacer(1, 12))

    doc.build(elementos)
    return rutaGuardar
