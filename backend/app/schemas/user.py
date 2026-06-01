"""Esquemas de Usuario.

Nunca se expone el campo ``password`` en las respuestas (``UserOut``). La clave
primaria se serializa como ``_id`` para mantener el contrato del frontend.
"""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=6, max_length=128)
    role: Literal["user", "admin"] = "user"


class UserUpdate(BaseModel):
    """Actualización parcial de usuario; la contraseña es opcional."""

    username: str | None = Field(default=None, min_length=3, max_length=50)
    role: Literal["user", "admin"] | None = None
    password: str | None = Field(default=None, min_length=6, max_length=128)


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(serialization_alias="_id")
    username: str
    role: str


class UserBrief(BaseModel):
    """Resumen del usuario devuelto al crearlo."""

    username: str
    role: str


class UserCreatedResponse(BaseModel):
    message: str
    user: UserBrief
