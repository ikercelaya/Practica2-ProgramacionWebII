"""Esquemas de Producto.

``ProductoOut`` serializa la clave primaria como ``_id`` para mantener el contrato
JSON que espera el frontend (heredado de MongoDB en la Práctica 1).
"""
from pydantic import BaseModel, ConfigDict, Field


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    precio: float = Field(ge=0)


class ProductoCreate(ProductoBase):
    """Datos validados para crear un producto."""


class ProductoUpdate(BaseModel):
    """Actualización parcial: sólo se aplican los campos presentes."""

    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    precio: float | None = Field(default=None, ge=0)


class ProductoOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    # Se lee del atributo ``id`` del ORM y se serializa como ``_id``.
    id: int = Field(serialization_alias="_id")
    nombre: str
    precio: float
    imagen: str | None = None
