from src.data.repository import (
    insertarParametro)

def cargarParametro():
    print("=== CARGAR NUEVO PARÁMETRO ===")
    nombre_parametro = input("Nombre del parámetro: ").strip()
    codigo_parametro = input("Código del parámetro: ").strip()
    unidad_medida = input("Unidad de medida: ").strip()
    
    insertarParametro(
        codigo=codigo_parametro, nombreParametro=nombre_parametro, unidad=unidad_medida)
    
    print(f"Parámetro '{nombre_parametro}' cargado exitosamente.")  

if __name__ == "__main__":
    cargarParametro()