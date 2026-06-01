"""Repositorio de usuarios: encapsula todas las consultas SQL sobre ``User``."""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, user_id) -> User | None:
        if user_id is None:
            return None
        return self.db.get(User, user_id)

    def get_by_username(self, username: str) -> User | None:
        return self.db.scalar(select(User).where(User.username == username))

    def list(self) -> list[User]:
        return list(self.db.scalars(select(User).order_by(User.id)).all())

    def create(self, *, username: str, password: str, role: str) -> User:
        user = User(username=username, password=password, role=role)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: User, fields: dict) -> User:
        for key, value in fields.items():
            setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: User) -> None:
        self.db.delete(user)
        self.db.commit()
