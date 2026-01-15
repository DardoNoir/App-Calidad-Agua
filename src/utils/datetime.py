from datetime import datetime

FORMATO = "%d/%m/%Y %H:%M"

def ahora_str():
    return datetime.now().strftime(FORMATO)

def parse_fecha_str(fecha_str: str) -> str:
    # Valida y devuelve mismo formato
    return datetime.strptime(fecha_str, FORMATO).strftime(FORMATO)
