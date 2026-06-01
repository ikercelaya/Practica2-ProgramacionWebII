"""Lógica de negocio de usuarios (gestión por parte del administrador)."""
from sqlalchemy.orm import Session

from app.core.exceptions import ConflictError, NotFoundError
from app.core.security import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    def __init__(self, db: Session) -> None:
        self.repo = UserRepository(db)

    def list(self) -> list[User]:
        return self.repo.list()

    def create(self, data: UserCreate) -> User:
        if self.repo.get_by_username(data.username):
            raise ConflictError("El nombre de usuario ya está en uso")
        return self.repo.create(
            username=data.username,
            password=hash_password(data.password),
            role=data.role,
        )

    def update(self, user_id: int, data: UserUpdate) -> User:
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Usuario no encontrado")

        fields = data.model_dump(exclude_unset=True)

        # La contraseña sólo se actualiza (y se hashea) si se envía no vacía.
        new_password = fields.pop("password", None)
        if new_password:
            fields["password"] = hash_password(new_password)

        # Si cambia el nombre de usuario, comprobar que no colisione con otro.
        new_username = fields.get("username")
        if (
            new_username
            and new_username != user.username
            and self.repo.get_by_username(new_username)
        ):
            raise ConflictError("El nombre de usuario ya está en uso")

        return self.repo.update(user, fields)

    def delete(self, user_id: int) -> None:
        user = self.repo.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Usuario no encontrado")
        self.repo.delete(user)
