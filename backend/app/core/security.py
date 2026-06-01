"""Funciones de seguridad: hashing de contraseñas (bcrypt) y emisión/validación de JWT.

Se aísla aquí toda la criptografía para que servicios y dependencias no dependan
directamente de las librerías concretas (bcrypt / PyJWT).
"""
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import settings

# bcrypt sólo considera los primeros 72 bytes de la contraseña y, desde la
# versión 4, lanza error si se superan. Truncamos de forma explícita y segura.
_BCRYPT_MAX_BYTES = 72


def hash_password(plain_password: str) -> str:
    """Devuelve el hash bcrypt (con sal) de una contraseña en texto plano."""
    password_bytes = plain_password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
    return bcrypt.hashpw(password_bytes, bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Comprueba una contraseña en texto plano contra su hash bcrypt almacenado."""
    try:
        password_bytes = plain_password.encode("utf-8")[:_BCRYPT_MAX_BYTES]
        return bcrypt.checkpw(password_bytes, hashed_password.encode("utf-8"))
    except (ValueError, TypeError):
        return False


def create_access_token(*, user_id: int, username: str, role: str) -> str:
    """Genera un JWT firmado con la información mínima del usuario.

    El payload reproduce el contrato de la Práctica 1: ``{id, username, role}``.
    El frontend decodifica el token para conocer el rol y el nombre de usuario.
    """
    now = datetime.now(timezone.utc)
    payload = {
        "id": user_id,
        "username": username,
        "role": role,
        "iat": now,
        "exp": now + timedelta(minutes=settings.jwt_expire_minutes),
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_access_token(token: str) -> dict:
    """Valida y decodifica un JWT.

    Lanza ``jwt.ExpiredSignatureError`` si ha expirado o ``jwt.PyJWTError`` si es
    inválido; las dependencias de autenticación traducen esos errores a 403.
    """
    return jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
