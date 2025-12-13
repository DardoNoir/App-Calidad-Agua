from datetime import datetime
from src.data.repository import (
    traerUsuarioPorId,
    insertarLugar,
    traerLugares,
    traerParametros,
    insertarMedicion,
    insertarValorMedido,
    traerValoresReferenciaPorParametro,
)
from src.analysis.evaluacion import EvaluarParametro

def testCargarMedicionCompleta():
    print("--- CARGAR MEDICION ---")
    # Datos de la medición
    
    # Usuario que carga la medición
    usuarioId = 1 # Tomamos este para evitar el login
    nombreUsuario = traerUsuarioPorId(usuarioId)
    print(f"Usuario que carga la medición: {nombreUsuario})")

    # Lugar de la medición
    l = None
    input("Presione Enter para cargar un Cuerpo de Agua...")
    provincia=input("Provincia: ").strip()
    ciudad=input("Ciudad: ").strip() 
    cuerpoAgua=input("Cuerpo de agua: ").strip()
    insertarLugar(provincia, ciudad, cuerpoAgua)
    Lugares = traerLugares()
    for lugar in Lugares:
        if (lugar["provincia"] == provincia and lugar["ciudad"] == ciudad 
            and lugar["cuerpoAgua"] == cuerpoAgua):
            l = lugar["id"]
            break
    
    if l is None:
        raise ValueError("No se pudo obtener el ID del lugar recién creado")

    # Fecha y hora de la medición
    fechaMedicion = datetime.now()
    print(f"Fecha y hora de la medición: {fechaMedicion}")
    
    # Parametros a medir
    parametros = traerParametros()
    for parametro in parametros:
        print(f"Ingrese valor para el parámetro {parametro['nombreParametro']} ({parametro['unidad']}): ")
        try:
            valor = float(input())
        except ValueError:
            print("Valor inválido. Por favor, ingrese un número.")
            continue 

        ref = traerValoresReferenciaPorParametro(parametro["id"])
        if not ref:
            print(f"No hay valores de referencia para el parámetro {parametro['nombreParametro']}.")
            continue    

        estado, desvio = EvaluarParametro(valor, ref)
        print(f"Evaluación para {parametro['nombreParametro']}: Estado = {estado}, Desviación = {desvio}")
        input("Presione Enter para continuar...")

        # Insertar la medición y el valor medido
        medicionId = insertarMedicion(l, fechaMedicion, usuarioId, comentarios="test carga completa")
        insertarValorMedido(medicionId,[{"idParametro": parametro["id"]}],valor,estado,desvio)

    print("Medición completa cargada exitosamente.")

if __name__ == "__main__":
    testCargarMedicionCompleta()