"""Repositorio de productos: encapsula las consultas SQL sobre ``Producto``."""
from sqlalchemy import delete, func, select
from sqlalchemy.orm import Session

from app.models.cart import CartItem
from app.models.producto import Producto


class ProductoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, producto_id) -> Producto | None:
        if producto_id is None:
            return None
        return self.db.get(Producto, producto_id)

    def list(self, name_filter: str | None = None) -> list[Producto]:
        stmt = select(Producto).order_by(Producto.id)
        if name_filter:
            # Filtro por nombre, insensible a mayúsculas (equivalente al original).
            stmt = stmt.where(func.lower(Producto.nombre).like(f"%{name_filter.lower()}%"))
        return list(self.db.scalars(stmt).all())

    def create(self, *, nombre: str, precio: float, imagen: str | None) -> Producto:
        producto = Producto(nombre=nombre, precio=precio, imagen=imagen)
        self.db.add(producto)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def update(self, producto: Producto, fields: dict) -> Producto:
        for key, value in fields.items():
            setattr(producto, key, value)
        self.db.commit()
        self.db.refresh(producto)
        return producto

    def delete(self, producto: Producto) -> None:
        # Limpia las líneas de carrito que referencian al producto antes de borrarlo.
        self.db.execute(delete(CartItem).where(CartItem.producto_id == producto.id))
        self.db.delete(producto)
        self.db.commit()
