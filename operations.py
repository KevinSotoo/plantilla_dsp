from typing import List, Optional
from sqlmodel import Session, select
from models import Producto, Categoria

# CRUD Producto
def crear_producto(db: Session, producto: Producto) -> Producto:
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto

def listar_productos(db: Session) -> List[Producto]:
    return db.exec(select(Producto)).all()

def obtener_producto(db: Session, nombre: str) -> Optional[Producto]:
    return db.exec(select(Producto).where(Producto.nombre == nombre)).first()

def eliminar_producto(db: Session, nombre: str) -> dict:
    producto = obtener_producto(db, nombre)
    if producto:
        db.delete(producto)
        db.commit()
        return {"mensaje": "Producto eliminado correctamente"}
    return {"error": "Producto no encontrado"}

# CRUD Categoria
def crear_categoria(db: Session, categoria: Categoria) -> Categoria:
    db.add(categoria)
    db.commit()
    db.refresh(categoria)
    return categoria

def listar_categorias(db: Session) -> List[Categoria]:
    return db.exec(select(Categoria)).all()

def obtener_categoria(db: Session, nombre: str) -> Optional[Categoria]:
    return db.exec(select(Categoria).where(Categoria.nombre == nombre)).first()

def eliminar_categoria(db: Session, nombre: str) -> dict:
    categoria = obtener_categoria(db, nombre)
    if categoria:
        db.delete(categoria)
        db.commit()
        return {"mensaje": "Categoría eliminada correctamente"}
    return {"error": "Categoría no encontrada"}