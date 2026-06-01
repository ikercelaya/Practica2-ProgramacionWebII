"""Lógica de negocio del carrito de la compra."""
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.cart import CartItem
from app.repositories.cart_repository import CartRepository
from app.repositories.producto_repository import ProductoRepository


class CartService:
    def __init__(self, db: Session) -> None:
        self.repo = CartRepository(db)
        self.productos = ProductoRepository(db)

    def get_cart(self, user_id: int) -> list[CartItem]:
        return self.repo.list_for_user(user_id)

    def add(self, user_id: int, producto_id: int) -> list[CartItem]:
        if self.productos.get_by_id(producto_id) is None:
            raise NotFoundError("Producto no encontrado")
        self.repo.add(user_id, producto_id)
        return self.repo.list_for_user(user_id)

    def remove(self, user_id: int, producto_id: int) -> list[CartItem]:
        self.repo.remove(user_id, producto_id)
        return self.repo.list_for_user(user_id)
