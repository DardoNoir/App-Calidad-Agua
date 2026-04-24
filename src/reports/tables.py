from typing import List, Any, Dict
from reportlab.platypus import Table, TableStyle, Paragraph, Flowable
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors  
from src.utils.datetime import format_fecha_display

def crearTablaValoresMedidos(valores: List[Dict[str, Any]]) -> Flowable: 
    styles = getSampleStyleSheet() 
    normal = styles["Normal"] 
    normal.wordWrap = "CJK"  

    acomodar = styles["Normal"]
    acomodar.wordWrap = None  

    alinearDerecha = styles["Normal"].clone("alinearDerecha")
    alinearDerecha.alignment = 2  # RIGHT


    data = [
        [ Paragraph("<b>Parámetro</b>", normal), 
         Paragraph("<b>Valor Medido</b>", normal), 
         Paragraph("<b>Unidad</b>", normal), 
         Paragraph("<b>Estado</b>", normal), 
         Paragraph("<b>Desviación</b>", normal), 
         ] 
    ] 
    
    for valor in valores: 
        data.append([ Paragraph(str(valor["nombre_parametro"]), acomodar), 
                     Paragraph(str(valor["valor"]), alinearDerecha), 
                     Paragraph(str(valor["unidad"] or "-"), normal), 
                     Paragraph(str(valor["estado"]), normal), 
                     Paragraph(str(valor["desviacion"] or "-"), normal), 
                ]) 
        
    table = Table( 
        data, colWidths=[80, 80, 70, 70, 200],
        repeatRows=1, 
        hAlign="LEFT" ) 
    
    table.setStyle(TableStyle([ 
        ("GRID", (0,0), (-1,-1), 0.5, colors.black), 
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey), 
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"), 
        ("ALIGN", (1,1), (-2,-1), "CENTER"), 
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"), 
        ("BOTTOMPADDING", (0,0), (-1,-1), 6), 
        ("TOPPADDING", (0,0), (-1,-1), 6), ])) 
    
    return table


def color_por_ica(ica: float) -> str:
    if ica >= 91:
        return "blue"
    elif ica >= 71:
        return "green"
    elif ica >= 51:
        return "gold"
    elif ica >= 26:
        return "orange"
    else:
        return "red"

def crearTablaICA(ica: float | None, clasificacionIca: str | None) -> Flowable:
    
    if ica is None:
        valor_ica = "No calculado"
        color = "grey"
        clasificacion = "No calculada"
    else:
        valor_ica = f"{ica:.2f}"
        color = color_por_ica(ica)
        clasificacion = clasificacionIca or "Sin clasificar"

    data = [
        ["Índice de Calidad del Agua (ICA)", valor_ica],
        ["Clasificación", clasificacion]
    ]

    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (1,0), (1,0), "CENTER"),
        ("ALIGN", (1,1), (1,1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
        ("TEXTCOLOR", (1,1), (1,1), getattr(colors, color))
    ]))

    return table



from datetime import datetime

def formatoFecha(fecha: Any) -> str:
    try:
        return format_fecha_display(fecha)
    except:
        return "Fecha inválida"



def crearTablaDatosGenerales(
    lugar: str,
    fecha: str,
    usuario: str
) -> Flowable:
    styles = getSampleStyleSheet()

    etiqueta = styles["Normal"]
    etiqueta.fontName = "Helvetica-Bold"

    valor = styles["Normal"]

    data = [
        [Paragraph("Lugar:", etiqueta), Paragraph(lugar, valor)],
        [Paragraph("Fecha de Medición:", etiqueta), Paragraph(fecha, valor)],
        [Paragraph("Medida Tomada Por:", etiqueta), Paragraph(usuario, valor)],
    ]

    table = Table(
        data,
        colWidths=[130, 350],
        hAlign="LEFT"
    )

    table.setStyle(TableStyle([
        ("ALIGN", (0,0), (0,-1), "RIGHT"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 6),
    ]))

    return table