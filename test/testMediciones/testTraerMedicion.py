from src.data.repository import(
    traerValoresMedidosDeMedicion
)

def traerValores():
    
    idMed=int(input("Ingresar Medición: "))
    medidas=traerValoresMedidosDeMedicion(idMedicion=idMed)
    
    print(f"--- Valores de la medición {idMed}---")
    for medida in medidas:
        print("Paramtero: ",medida["nombreParametro"], "Valor: ", medida["valor"],medida["unidad"])

if __name__ == "__main__":
    traerValores()