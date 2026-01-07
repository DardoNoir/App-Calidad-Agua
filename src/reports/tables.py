from typing import List, Any, Dict
from reportlab.platypus import Table, TableStyle, Flowable
from reportlab.lib import colors    




def crearTablaValoresMedidos(valores: List[Dict[str, Any]]) -> Flowable:
    data: List[List[Any]] = [
        ["Parámetro", "Valor Medido", "Unidad", "Estado", "Desviación"]
    ]

    for valor in valores:
        data.append([
            valor["nombreParametro"],
            valor["valor"],
            valor["unidad"],
            valor["estado"],
            valor["desviacion"]
        ])

    table = Table(data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("GRID", (0,0), (-1,-1), 1, colors.black),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (1,1), (-2,-1), "CENTER"),
        ("ALIGN", (-1,1), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0,0), (-1,0), 8),
    ]))

    return table
