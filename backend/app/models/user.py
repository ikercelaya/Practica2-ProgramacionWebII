"""Modelo ORM de Usuario."""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(10), default="user", nullable=False)

    # Relación 1:N con las líneas del carrito; se borran en cascada con el usuario.
    cart_items: Mapped[list["CartItem"]] = relationship(  # noqa: F821
        back_populates="user",
        cascade="all, delete-orphan",
    )
