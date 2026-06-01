"""Lógica de negocio de autenticación: registro y login."""
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, UnauthorizedError
from app.core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, RegisterRequest


class AuthService:
    def __init__(self, db: Session) -> None:
        self.users = UserRepository(db)

    def register(self, data: RegisterRequest) -> None:
        """Registra un usuario nuevo con rol ``user`` (como en la Práctica 1)."""
        if self.users.get_by_username(data.username):
            raise ConflictError("El nombre de usuario ya está en uso")
        self.users.create(
            username=data.username,
            password=hash_password(data.password),
            role="user",
        )

    def login(self, data: LoginRequest) -> str:
        """Valida credenciales y devuelve un JWT firmado, o lanza 401."""
        user = self.users.get_by_username(data.username)
        if user is None or not verify_password(data.password, user.password):
            raise UnauthorizedError("Credenciales inválidas")
        return create_access_token(user_id=user.id, username=user.username, role=user.role)
