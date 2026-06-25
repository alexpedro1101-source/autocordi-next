from fastapi import FastAPI
from pydantic import BaseModel
from procesador import procesar_registro

app = FastAPI()

# ✔️ RUTA PRINCIPAL (ESTO ARREGLA EL ERROR)
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "API funcionando correctamente",
        "endpoint": "/procesar"
    }

# ✔️ MODELO JSON
class Input(BaseModel):
    texto: str

# ✔️ ENDPOINT PRINCIPAL
@app.post("/procesar")
def procesar(data: Input):
    salida1, salida2 = procesar_registro(data.texto)

    return {
        "salida1": salida1,
        "salida2": salida2
    }