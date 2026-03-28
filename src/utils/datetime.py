from datetime import datetime

# Formatos
FORMATO_USUARIO = "%d/%m/%Y %H:%M"
FORMATO_DB = "%Y-%m-%d %H:%M:%S"

def ahora_str():
    return datetime.now().strftime(FORMATO_DB)

def parse_fecha_str(fecha_str: str) -> str:
    """
    Convierte de formato usuario → formato DB
    """
    dt = datetime.strptime(fecha_str, FORMATO_USUARIO)
    return dt.strftime(FORMATO_DB)

def format_fecha_display(fecha_str: str) -> str:
    try:
        dt = datetime.strptime(fecha_str, FORMATO_DB)
    except ValueError:
        dt = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S.%f")

    return dt.strftime(FORMATO_USUARIO)
def parse_fecha_dt(fecha_str: str) -> datetime:
    return datetime.strptime(fecha_str, FORMATO_USUARIO)