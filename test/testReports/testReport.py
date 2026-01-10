from pathlib import Path
from src.reports.pdfReport import generarReporte

if __name__ == "__main__":
    
    ruta = Path("reporte_prueba.pdf")

    generarReporte(
        idMedicion=2,
        rutaGuardar=ruta
    )

    print("PDF generado en:", ruta.resolve())


