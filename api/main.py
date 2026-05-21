from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

builds = []

class Build(BaseModel):
    personaje: str
    atk: int
    crit_rate: float
    crit_dmg: float
    bonus: float
    multiplicador: float

@app.post("/calcular")
def calcular(build: Build):

    daño = (
        build.atk
        * (build.multiplicador / 100)
        * (1 + build.crit_dmg / 100)
        * (1 + build.bonus / 100)
    )

    resultado = {
        **build.dict(),
        "daño_final": round(daño, 2)
    }

    builds.append(resultado)

    return resultado

@app.get("/builds")
def obtener_builds():
    return builds