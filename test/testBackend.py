from datetime import datetime

from src.data.repository import (
    insertarLugar,
    insertarMedicion,
    insertarValorMedido,
    traerParametros,
    traerValoresReferencia,
    insertarParametro
)

from src.analysis.evaluacion import EvaluarParametro

def probar_backend():
    print("=== PRUEBA BACKEND ===")

    # Lugar
    idLugar = insertarLugar("Entre Rios", "Gualeguaychu", "Rio Gualeguaychu")
    print("Lugar:", idLugar)

    # Medición
    idMed = insertarMedicion(idLugar, datetime.now(), 1, "test")
    print("Medición:", idMed)

    # Parámetro
    par = insertarParametro("1111","PH","grs")
    print("Parametro: ",par)

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
    idVM = insertarValorMedido(idMed, param["id"], 7.5, estado, desvio)
    print("Valor medido:", idVM)

if __name__ == "__main__":
    probar_backend()
