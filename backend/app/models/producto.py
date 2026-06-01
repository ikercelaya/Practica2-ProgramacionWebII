"""Modelo ORM de Producto."""
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    precio: Mapped[float] = mapped_column(Float, nullable=False)
    # Nombre del archivo de imagen guardado en ``uploads/``; puede no existir.
    imagen: Mapped[str | None] = mapped_column(String(255), nullable=True)
