"""Repositorio del carrito: consultas SQL sobre ``CartItem``."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.cart import CartItem


class CartRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_for_user(self, user_id: int) -> list[CartItem]:
        return list(
            self.db.scalars(
                select(CartItem).where(CartItem.user_id == user_id).order_by(CartItem.id)
            ).all()
        )

    def get_item(self, user_id: int, producto_id: int) -> CartItem | None:
        return self.db.scalar(
            select(CartItem).where(
                CartItem.user_id == user_id,
                CartItem.producto_id == producto_id,
            )
        )

    def add(self, user_id: int, producto_id: int) -> None:
        item = self.get_item(user_id, producto_id)
        if item is not None:
            item.quantity += 1
        else:
            self.db.add(CartItem(user_id=user_id, producto_id=producto_id, quantity=1))
        self.db.commit()

    def remove(self, user_id: int, producto_id: int) -> None:
        item = self.get_item(user_id, producto_id)
        if item is not None:
            self.db.delete(item)
            self.db.commit()
