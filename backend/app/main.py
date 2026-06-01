"""Punto de entrada de la aplicación FastAPI (fábrica de la app).

Aquí se ensamblan todas las piezas: CORS, archivos estáticos, routers, manejo
global de excepciones e inicialización de la base de datos. No contiene lógica de
negocio: cada responsabilidad vive en su capa correspondiente.
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import init_db
from app.core.error_handlers import register_exception_handlers
from app.routers.auth_router import router as auth_router
from app.routers.cart_router import router as cart_router
from app.routers.producto_router import router as producto_router
from app.routers.user_router import router as user_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Práctica 2 PWII - API Tienda (Python / FastAPI)",
        description=(
            "Backend en Python con arquitectura en capas (routers → services → "
            "repositories → models), autenticación JWT, validación con Pydantic, "
            "manejo global de excepciones y persistencia en SQLite (SQLAlchemy)."
        ),
        version="2.0.0",
    )

    # --- CORS (el frontend Svelte corre en otro origen, p. ej. localhost:5173) ---
    if settings.cors_origins.strip() == "*":
        origins = ["*"]
    else:
        origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # --- Archivos estáticos: imágenes de producto en /uploads/<archivo> ---
    os.makedirs(settings.upload_dir, exist_ok=True)
    app.mount("/uploads", StaticFiles(directory=settings.upload_dir), name="uploads")

    # --- Rutas de la API ---
    app.include_router(auth_router)
    app.include_router(producto_router)
    app.include_router(user_router)
    app.include_router(cart_router)

    # --- Manejo global de excepciones (respuestas de error unificadas) ---
    register_exception_handlers(app)

    # --- Crear las tablas si no existen ---
    init_db()

    return app


app = create_app()
