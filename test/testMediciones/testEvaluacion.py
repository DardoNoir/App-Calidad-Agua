import src.data.repository
import src.analysis.evaluacion

def pruebaMedicionCompleta():
    print("=== PRUEBA MEDICIÓN COMPLETA ===")

    parametros = src.data.repository.traerParametros()
    if not parametros:
        print("No hay parámetros disponibles para la medición.")
        return
    
    for parametro in parametros:
        print(f"Ingrese valor para el parámetro {parametro['nombreParametro']} ({parametro['unidad']}): ")
        try:
            valor = float(input())
        except ValueError:
            print("Valor inválido. Por favor, ingrese un número.")
            continue    

        idParametro = parametro["id"]
        ref = src.data.repository.traerValoresReferenciaPorParametro(idParametro)
        if not ref:
            print(f"No hay valores de referencia para el parámetro {parametro['nombreParametro']}.")
            continue
        
        estado, desvio = src.analysis.evaluacion.EvaluarParametro(valor, ref)
        print(f"Evaluación para {parametro['nombreParametro']}: Estado = {estado}, Desviación = {desvio}")

if __name__ == "__main__":
    pruebaMedicionCompleta()