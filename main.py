from fastapi import FastAPI
from procesador import procesar_registro

app = FastAPI()

@app.post("/procesar")
def procesar(texto: str):
    salida1, salida2 = procesar_registro(texto)
    return {
        "salida1": salida1,
        "salida2": salida2
    }