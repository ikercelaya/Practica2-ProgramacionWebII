"""Rutas de usuarios: /api/users (CRUD completo, sólo para admin)."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.auth import require_admin
from app.models.user import User
from app.schemas.user import UserCreate, UserCreatedResponse, UserOut, UserUpdate
from app.services.user_service import UserService

router = APIRouter(prefix="/api/users", tags=["Usuarios"])


@router.get("", response_model=list[UserOut])
def list_users(_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    return UserService(db).list()


@router.post("", response_model=UserCreatedResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreate,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    user = UserService(db).create(payload)
    return {
        "message": "Usuario creado con éxito",
        "user": {"username": user.username, "role": user.role},
    }


@router.put("/{user_id}", response_model=UserOut)
def update_user(
    user_id: int,
    payload: UserUpdate,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return UserService(db).update(user_id, payload)


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    _admin: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    UserService(db).delete(user_id)
    return {"message": "Usuario eliminado"}
