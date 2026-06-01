"""Rutas del carrito: /api/cart (requieren usuario autenticado)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import get_current_user
from app.models.cart import CartItem
from app.models.user import User
from app.schemas.cart import CartAddRequest, CartItemOut
from app.schemas.producto import ProductoOut
from app.services.cart_service import CartService

router = APIRouter(prefix="/api/cart", tags=["Carrito"])


def _serialize(items: list[CartItem]) -> list[CartItemOut]:
    """Transforma las líneas ORM al formato {productId: {...}, quantity} del frontend."""
    return [
        CartItemOut(productId=ProductoOut.model_validate(item.producto), quantity=item.quantity)
        for item in items
    ]


@router.get("", response_model=list[CartItemOut])
def get_cart(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return _serialize(CartService(db).get_cart(current_user.id))


@router.post("/add", response_model=list[CartItemOut])
def add_to_cart(
    payload: CartAddRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _serialize(CartService(db).add(current_user.id, payload.producto_id))


@router.delete("/{producto_id}", response_model=list[CartItemOut])
def remove_from_cart(
    producto_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _serialize(CartService(db).remove(current_user.id, producto_id))
