"""Excepciones de dominio.

La lógica de negocio lanza estas excepciones sin saber nada de HTTP. Los
manejadores globales (``error_handlers.py``) las traducen a códigos de estado y
a un cuerpo JSON unificado.
"""


class AppError(Exception):
    """Excepción base de la aplicación (errores controlados de negocio)."""

    default_status: int = 500
    default_message: str = "Error interno del servidor"

    def __init__(self, message: str | None = None, status_code: int | None = None) -> None:
        self.message = message or self.default_message
        self.status_code = status_code or self.default_status
        super().__init__(self.message)


class NotFoundError(AppError):
    default_status = 404
    default_message = "Recurso no encontrado"


class ConflictError(AppError):
    default_status = 409
    default_message = "El recurso ya existe"


class UnauthorizedError(AppError):
    default_status = 401
    default_message = "No autorizado"


class ForbiddenError(AppError):
    default_status = 403
    default_message = "Acceso prohibido"


class ValidationAppError(AppError):
    default_status = 422
    default_message = "Datos no válidos"
