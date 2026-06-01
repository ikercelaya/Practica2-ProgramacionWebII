"""Configuración central de la aplicación.

Las variables de entorno (opcionalmente desde un archivo ``.env``) se cargan con
``pydantic-settings``, de modo que el resto de capas accedan a la configuración a
través de un único objeto ``settings`` tipado y validado.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración tipada de la aplicación leída del entorno / archivo .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Seguridad / JWT ---
    jwt_secret: str = "Clave"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    # --- Base de datos ---
    database_url: str = "sqlite:///./practica2.db"

    # --- Subida de imágenes de producto ---
    upload_dir: str = "uploads"

    # --- Servidor ---
    port: int = 3000

    # --- CORS: "*" o lista de orígenes separados por comas ---
    cors_origins: str = "*"


settings = Settings()
