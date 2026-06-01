"""Esquemas del Carrito.

El frontend envía ``{ "productId": <id> }`` y espera recibir cada línea como
``{ "productId": { ...producto... }, "quantity": <int> }`` (producto "populado").
"""
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.producto import ProductoOut


class CartAddRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # Acepta la clave ``productId`` del frontend y la expone como ``producto_id``.
    producto_id: int = Field(validation_alias="productId", ge=1)


class CartItemOut(BaseModel):
    productId: ProductoOut
    quantity: int
