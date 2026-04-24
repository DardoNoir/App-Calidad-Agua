from datetime import datetime

# Formatos
FORMATO_USUARIO = "%d/%m/%Y %H:%M"
FORMATO_DB = "%Y-%m-%d %H:%M:%S"

def ahora_str():
    return datetime.now().strftime(FORMATO_DB)

def parse_fecha_str(fecha_str: str) -> str:
    dt = datetime.strptime(fecha_str, FORMATO_USUARIO)
    return dt.strftime(FORMATO_DB)

def format_fecha_display(fecha) -> str:
    if fecha is None:
        return ""

    if isinstance(fecha, datetime):
        dt = fecha

    elif isinstance(fecha, str):
        try:
            dt = datetime.strptime(fecha, FORMATO_DB)
        except ValueError:
            # Para casos con microsegundos
            dt = datetime.strptime(fecha, "%Y-%m-%d %H:%M:%S.%f")

    else:
        raise TypeError(f"Tipo de fecha no soportado: {type(fecha)}")

    return dt.strftime(FORMATO_USUARIO)

def parse_fecha_dt(fecha_str: str) -> datetime:
    return datetime.strptime(fecha_str, FORMATO_USUARIO)