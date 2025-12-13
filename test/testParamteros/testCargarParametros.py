from src.data.repository import (
    insertarParametro)

def cargarParametro():
    print("=== CARGAR NUEVO PARÁMETRO ===")
    print("Nombre del parámetro: ")
    nombre_parametro = input().strip() 
    print("Código del parámetro: ")
    codigo_parametro = input().strip() 
    print("Unidad de medida: ")
    unidad_medida = input().strip()
    
    insertarParametro(
        codigo=codigo_parametro, nombreParametro=nombre_parametro, unidad=unidad_medida)
    
    print(f"Parámetro '{nombre_parametro}' cargado exitosamente.")  