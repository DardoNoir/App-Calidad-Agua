from datetime import datetime

from src.data.repository import (
    insertarLugar,
    traerLugares,
    insertarMedicion,
    insertarValorMedido,
    traerParametros,
    traerValoresReferenciaPorParametro,
    insertarParametro,
    insertarValoresReferencia,
    traerMediciones,
    traerUsuarioPorId
)

from src.analysis.evaluacion import EvaluarParametro

def probar_backend():
    print("=== PRUEBA BACKEND ===")

    print("Ingrese valor del Ph: ")
    valor=float(input())

    # Lugar
    idLugar = insertarLugar("Entre Rios", "Gualeguaychu", "Rio Gualeguaychu")
    lugares = traerLugares()
    for lugar in lugares:
     if lugar["id"] == idLugar:
        print("Lugar:", lugar)
    
    # Medición
    idMed = insertarMedicion(idLugar, datetime.now(), 1, "test")
    mediciones = traerMediciones()
    for medicion in mediciones:
     if medicion["id"] == idMed:
        usuario = traerUsuarioPorId(medicion["medidaTomadaPor"])
        print("Medición:", medicion)
        print("Tomada por:", usuario)

    # Parámetro
    par = insertarParametro("0001","pH"," ")
    insertarValoresReferencia(par,limiteMaxAceptable=9.0, limiteMaxWarning=9.5, limiteMinAceptable=6.5, limiteMinWarning=6.0)
    parametros = traerParametros()
    for parametro in parametros:
     if parametro["id"] == par:
        print("Parámetro:", parametro)

    # Referencia
    ref = traerValoresReferenciaPorParametro(par)
    print("Referencia:", ref)

    # Evaluación
    estado, desvio = EvaluarParametro(valor, ref) 
    print("Evaluación:", estado)
    print("Desviación: ",desvio) 
    print("Valor medido:", valor)

    # Guardado
    insertarValorMedido(idMed, par, valor, estado, desvio)

if __name__ == "__main__":
    probar_backend()
