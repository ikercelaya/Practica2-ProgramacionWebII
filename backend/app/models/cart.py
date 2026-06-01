"""Modelo ORM de línea de carrito (relación usuario - producto con cantidad)."""
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class CartItem(Base):
    __tablename__ = "cart_items"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    producto_id: Mapped[int] = mapped_column(
        ForeignKey("productos.id", ondelete="CASCADE"), nullable=False
    )
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)

    user: Mapped["User"] = relationship(back_populates="cart_items")  # noqa: F821
    producto: Mapped["Producto"] = relationship()  # noqa: F821
