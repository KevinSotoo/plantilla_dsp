from fastapi import FastAPI, Request, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from pathlib import Path

from models import Producto, Categoria
from operations import (
    crear_producto, listar_productos, obtener_producto, eliminar_producto,
    crear_categoria, listar_categorias, obtener_categoria, eliminar_categoria
)
from connection_db import get_session
from create_tables import init_db

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOADS_DIR = "static/uploads"
Path(UPLOADS_DIR).mkdir(parents=True, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")

@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def index(request: Request, db=Depends(get_session)):
    productos = listar_productos(db)
    categorias = listar_categorias(db)
    return templates.TemplateResponse("index.html", {"request": request, "productos": productos, "categorias": categorias})

@app.post("/producto/", response_model=Producto)
async def crear_producto_endpoint(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    precio: float = Form(...),
    image: Optional[UploadFile] = File(None),
    db=Depends(get_session)
):
    imagen_path = None
    if image:
        file_location = f"{UPLOADS_DIR}/{image.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(await image.read())
        imagen_path = file_location
    producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio, imagen_path=imagen_path)
    return crear_producto(db, producto)

@app.get("/producto/", response_model=List[Producto])
def listar_productos_endpoint(db=Depends(get_session)):
    return listar_productos(db)

@app.delete("/producto/{nombre}", response_model=dict)
def eliminar_producto_endpoint(nombre: str, db=Depends(get_session)):
    return eliminar_producto(db, nombre)

@app.post("/categoria/", response_model=Categoria)
def crear_categoria_endpoint(categoria: Categoria, db=Depends(get_session)):
    return crear_categoria(db, categoria)

@app.get("/categoria/", response_model=List[Categoria])
def listar_categorias_endpoint(db=Depends(get_session)):
    return listar_categorias(db)

@app.delete("/categoria/{nombre}", response_model=dict)
def eliminar_categoria_endpoint(nombre: str, db=Depends(get_session)):
    return eliminar_categoria(db, nombre)