from src.data.repository import(
    traerParametros)

def listarParametros():
    paramteros = traerParametros()
    for p in paramteros:
        print(f"--- PARAMETRO ---")
        print(f"Id Parametro: ", p["id"])
        print(f"Código: ",p["codigo"])
        print(f"Nombre: ",p["nombreParametro"])
        print(f"Unidad: ",p["unidad"])


    input("Enter para terminar: ",)

if __name__ == "__main__":
    listarParametros()
