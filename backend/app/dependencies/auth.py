"""Dependencias de autenticación/autorización basadas en JWT.

Reproducen el comportamiento del middleware de la Práctica 1:
  * sin cabecera ``Authorization``       -> 401
  * token ausente / inválido / expirado  -> 403
  * usuario autenticado pero sin rol admin -> 403 ("Solo admin")
"""
import jwt
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import ForbiddenError, UnauthorizedError
from app.core.security import decode_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository


def _extract_bearer_token(request: Request) -> str:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise UnauthorizedError("Token no proporcionado")  # 401
    parts = auth_header.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    raise ForbiddenError("Token inválido")  # 403 (cabecera mal formada)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> User:
    """Devuelve el usuario autenticado a partir del token Bearer, o lanza 401/403."""
    token = _extract_bearer_token(request)
    try:
        payload = decode_access_token(token)
    except jwt.ExpiredSignatureError as exc:
        raise ForbiddenError("Token expirado") from exc
    except jwt.PyJWTError as exc:
        raise ForbiddenError("Token inválido") from exc

    user = UserRepository(db).get_by_id(payload.get("id"))
    if user is None:
        raise ForbiddenError("Token inválido")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Exige que el usuario autenticado tenga rol ``admin``; si no, lanza 403."""
    if current_user.role != "admin":
        raise ForbiddenError("Solo admin")
    return current_user
