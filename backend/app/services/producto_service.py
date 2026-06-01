"""Lógica de negocio de productos."""
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.producto import Producto
from app.repositories.producto_repository import ProductoRepository
from app.schemas.producto import ProductoCreate, ProductoUpdate


class ProductoService:
    def __init__(self, db: Session) -> None:
        self.repo = ProductoRepository(db)

    def list(self, name_filter: str | None = None) -> list[Producto]:
        return self.repo.list(name_filter)

    def create(self, data: ProductoCreate, imagen: str | None) -> Producto:
        return self.repo.create(nombre=data.nombre, precio=data.precio, imagen=imagen)

    def update(self, producto_id: int, data: ProductoUpdate, imagen: str | None = None) -> Producto:
        producto = self.repo.get_by_id(producto_id)
        if producto is None:
            raise NotFoundError("Producto no encontrado")
        # ``exclude_unset`` => sólo se actualizan los campos enviados por el cliente.
        fields = data.model_dump(exclude_unset=True)
        # Si se ha subido una imagen nueva, se reemplaza el nombre de archivo guardado.
        if imagen is not None:
            fields["imagen"] = imagen
        return self.repo.update(producto, fields)

    def delete(self, producto_id: int) -> None:
        producto = self.repo.get_by_id(producto_id)
        if producto is None:
            raise NotFoundError("Producto no encontrado")
        self.repo.delete(producto)
