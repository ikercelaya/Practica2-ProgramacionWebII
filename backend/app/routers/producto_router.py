"""Rutas de productos: /api/productos (CRUD; escritura sólo para admin)."""
from fastapi import APIRouter, Depends, File, Form, UploadFile, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_admin
from app.models.user import User
from app.schemas.producto import ProductoCreate, ProductoOut, ProductoUpdate
from app.services.producto_service import ProductoService
from app.utils.files import save_upload_file

router = APIRouter(prefix="/api/productos", tags=["Productos"])


@router.get("", response_model=list[ProductoOut])
def list_productos(name: str | None = None, db: Session = Depends(get_db)):
    """Listado público de productos, con filtro opcional por nombre (``?name=``)."""
    return ProductoService(db).list(name)


@router.post("", response_model=ProductoOut, status_code=status.HTTP_201_CREATED)
def create_producto(
    nombre: str = Form(...),
    precio: float = Form(...),
    imagen: UploadFile | None = File(default=None),
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Crea un producto (sólo admin). Recibe ``multipart/form-data`` con imagen opcional."""
    # Validación estricta de los campos del formulario mediante el esquema Pydantic.
    data = ProductoCreate(nombre=nombre, precio=precio)
    filename = save_upload_file(imagen) if imagen is not None else None
    return ProductoService(db).create(data, filename)


@router.put("/{producto_id}", response_model=ProductoOut)
def update_producto(
    producto_id: int,
    payload: ProductoUpdate,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Actualiza un producto existente (sólo admin)."""
    return ProductoService(db).update(producto_id, payload)


@router.delete("/{producto_id}")
def delete_producto(
    producto_id: int,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    """Elimina un producto (sólo admin)."""
    ProductoService(db).delete(producto_id)
    return {"message": "Producto eliminado"}
