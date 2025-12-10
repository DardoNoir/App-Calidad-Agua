from datetime import datetime

from src.data.repository import (
    insertarLugar,
    traerLugar,
    insertarMedicion,
    insertarValorMedido,
    traerParametros,
    traerValoresReferencia,
    insertarParametro,
    insertarValoresReferencia,
    traerMedicion,
    traerUsuarioPorId
)

from src.analysis.evaluacion import EvaluarParametro

def probar_backend():
    print("=== PRUEBA BACKEND ===")

    # Lugar
    idLugar = insertarLugar("Entre Rios", "Gualeguaychu", "Rio Gualeguaychu")
    lugares = traerLugar()
    lugar = lugares[0]
    print("Lugar",lugar)

    # Medición
    idMed = insertarMedicion(idLugar, datetime.now(), 1, "test")
    mediciones = traerMedicion()
    medicion = mediciones[0]
    usuario = traerUsuarioPorId(1)
    print("Medicion: ", medicion)
    print("Tomada por: ", usuario)

    # Parámetro
    par = insertarParametro("0001","pH"," ")
    insertarValoresReferencia(par,limiteMaxAceptable=9.0, limiteMaxWarning=9.5)
    
    parametros = traerParametros()
    param = parametros[0]
    print("Parametro:", param)

    # Referencia
    ref = traerValoresReferencia(param["id"])
    print("Referencia:", ref)

    # Evaluación
    estado, desvio = EvaluarParametro(7.5, ref)
    print("Evaluación:", estado, desvio)

    # Guardado
    insertarValorMedido(idMed, param["id"], 7.5, estado, desvio)
    print("Valor medido:", 7.5)

if __name__ == "__main__":
    probar_backend()
