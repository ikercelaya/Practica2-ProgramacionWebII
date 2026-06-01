"""Manejo global de excepciones.

Centraliza la traducción de cualquier error (de dominio, de validación de
Pydantic o inesperado) a una respuesta HTTP JSON con una forma unificada::

    {"error": "<mensaje legible>", "status_code": <int>, "detail": <opcional>}

El campo ``error`` mantiene la compatibilidad con el frontend de la Práctica 1,
que lee ``data.error`` o ``data.message`` para mostrar el toast de error.
"""
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.core.exceptions import AppError


def _error_body(message: str, status_code: int, detail=None) -> dict:
    body: dict = {"error": message, "status_code": status_code}
    if detail is not None:
        body["detail"] = detail
    return body


def _first_validation_message(errors: list[dict]) -> str:
    """Construye un mensaje legible a partir del primer error de validación."""
    if not errors:
        return "Datos no válidos"
    first = errors[0]
    loc = [str(part) for part in first.get("loc", []) if part not in ("body", "query", "path")]
    field = ".".join(loc) if loc else "datos"
    return f"{field}: {first.get('msg', 'valor no válido')}"


def register_exception_handlers(app: FastAPI) -> None:
    """Registra todos los manejadores globales de excepciones en la app."""

    @app.exception_handler(AppError)
    async def _handle_app_error(_: Request, exc: AppError):
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(exc.message, exc.status_code),
        )

    @app.exception_handler(RequestValidationError)
    async def _handle_request_validation(_: Request, exc: RequestValidationError):
        errors = jsonable_encoder(exc.errors())
        return JSONResponse(
            status_code=422,
            content=_error_body(_first_validation_message(errors), 422, errors),
        )

    @app.exception_handler(ValidationError)
    async def _handle_pydantic_validation(_: Request, exc: ValidationError):
        errors = jsonable_encoder(exc.errors())
        return JSONResponse(
            status_code=422,
            content=_error_body(_first_validation_message(errors), 422, errors),
        )

    @app.exception_handler(StarletteHTTPException)
    async def _handle_http_exception(_: Request, exc: StarletteHTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=_error_body(str(exc.detail), exc.status_code),
        )

    @app.exception_handler(Exception)
    async def _handle_unexpected(_: Request, exc: Exception):  # noqa: ARG001
        return JSONResponse(
            status_code=500,
            content=_error_body("Error interno del servidor", 500),
        )
