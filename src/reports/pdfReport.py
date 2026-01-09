from typing import Optional, List
from pathlib import Path
from tempfile import TemporaryDirectory
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable, Image, PageBreak
import matplotlib.pyplot as plt


from src.data.repository import(
    traerLugarPorId,
    traerMedicionPorId,
    traerUsuarioPorId,
    traerValoresMedidosDeMedicion,
    traerValoresReferenciaPorParametro,
)

from src.reports.tables import (
    crearTablaValoresMedidos,
    formatoFecha,
    crearTablaICA,
    crearTablaDatosGenerales
)

from src.charts.datasource import traerSerieCompletaParametroLugar

from src.charts.timeseries import graficarParametro
from src.charts.exporter import guardar_figura



def generarReporte(idMedicion: int, rutaGuardar: Path, db_path: Optional[str] = None) -> Path:
    # Genera un reporte PDF para una medición específica.
    # Datos de la medición y sus valores
    medicion = traerMedicionPorId(idMedicion, db_path)
    if medicion is None:
        raise RuntimeError("Medición no encontrada")
    
    valores = traerValoresMedidosDeMedicion(idMedicion, db_path)
    if not valores:
        raise RuntimeError("La medición no tiene valores cargados")

    # Datos del lugar 
    lugar = traerLugarPorId(medicion["idLugar"], db_path)
    if lugar is None:
        raise RuntimeError("Lugar no encontrado")
    # Datos del usuario
    usuario = traerUsuarioPorId(medicion["medidaTomadaPor"], db_path)
    if usuario is None:
        raise RuntimeError("Usuario no encontrado")
    
    # Formatear fecha
    fecha = formatoFecha(medicion["fechaMedicion"])
    
    # Crear documento PDF
    doc = SimpleDocTemplate(str(rutaGuardar))
    styles = getSampleStyleSheet()
    elementos: List[Flowable] = []

    # Título y datos generales
    elementos.append(Paragraph(f"Reporte de Medición: {medicion['id']}", styles['Title']))
    elementos.append(Spacer(1, 12))

    tabla_info = crearTablaDatosGenerales(
        lugar=f"{lugar['provincia']} - {lugar['ciudad']} - {lugar['cuerpoAgua']}",
        fecha=fecha,
        usuario=f"{usuario['nombreUsuario']}")
    elementos.append(tabla_info)
    elementos.append(Spacer(1, 12))

    # Tabla de valores medidos
    elementos.append(Paragraph("Valores Medidos:", styles['Heading2']))
    tabla_valores = crearTablaValoresMedidos(valores)

    elementos.append(tabla_valores)
    elementos.append(Spacer(1, 12))

    # Gráficos de parámetros
    elementos.append(PageBreak())
    elementos.append(Paragraph("Gráficos de Parámetros:", styles['Heading2']))
    with TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

    for valor in valores:
        idParametro = valor["idParametro"]
        nombreParametro = valor["nombreParametro"]
        unidad = valor["unidad"]

        # Traer serie histórica
        series = traerSerieCompletaParametroLugar(
            medicion["idLugar"],
            idParametro,
            db_path
        )
        if not series:
            continue  # No hay datos históricos para este parámetro
        
        fechas = [s["fecha"] for s in series if s["valor"] is not None]
        valores_historicos = [float(s["valor"]) for s in series if s["valor"] is not None]

        referencia = traerValoresReferenciaPorParametro(idParametro, db_path)
        
        fig = graficarParametro(
                fechas=fechas,
                valores=valores_historicos,
                nombreParametro=nombreParametro,
                unidad=unidad,
                referencia=referencia,
                titulo=f"en {lugar['cuerpoAgua']}"
            )

        rutaImagen = tmpdir / f"parametro_{nombreParametro}.png"
        guardar_figura(fig, rutaImagen)
        plt.close(fig)
        elementos.append(Paragraph(f"Parámetro: {nombreParametro}", styles['Heading3']))
        elementos.append(Image(str(rutaImagen), width=400, height=250))
        elementos.append(PageBreak())

    # Índice de Calidad del Agua (ICA)
    
    elementos.append(Paragraph("Índice de Calidad del Agua:", styles['Heading2']))
    tablaIca = crearTablaICA(
        medicion["ica"],
        medicion["clasificacionICA"]
    )
    elementos.append(tablaIca)
    elementos.append(Spacer(1, 12))

    # Construir el PDF
    doc.build(elementos)
    return rutaGuardar
