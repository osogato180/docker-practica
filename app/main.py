from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import Base, engine, SessionLocal
from models import Producto

app = FastAPI()

Base.metadata.create_all(bind=engine)


class ProductoCreate(BaseModel):
    nombre: str
    precio: float


@app.get("/")
def root():
    return {"message": "API funcionando"}


@app.get("/productos")
def listar_productos():

    db: Session = SessionLocal()

    productos = db.query(Producto).all()

    return productos


@app.post("/productos")
def crear_producto(producto: ProductoCreate):

    db: Session = SessionLocal()

    nuevo = Producto(
        nombre=producto.nombre,
        precio=producto.precio
    )

    db.add(nuevo)

    db.commit()

    db.refresh(nuevo)

    return nuevo


@app.put("/productos/{producto_id}")
def actualizar_producto(
    producto_id: int,
    producto: ProductoCreate
):

    db: Session = SessionLocal()

    prod = db.query(Producto).filter(
        Producto.id == producto_id
    ).first()

    if not prod:
        return {"error": "No existe"}

    prod.nombre = producto.nombre
    prod.precio = producto.precio

    db.commit()

    return prod


@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int):

    db: Session = SessionLocal()

    prod = db.query(Producto).filter(
        Producto.id == producto_id
    ).first()

    if not prod:
        return {"error": "No existe"}

    db.delete(prod)

    db.commit()

    return {"message": "Eliminado"}
