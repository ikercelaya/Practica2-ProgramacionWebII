"""Configuración de SQLAlchemy: motor, fábrica de sesiones y utilidades de BD.

Esta es la única pieza que conoce los detalles del motor de persistencia. Las
capas superiores (repositorios) reciben una ``Session`` y nunca crean el motor.
"""
from collections.abc import Generator

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


class Base(DeclarativeBase):
    """Clase base declarativa de la que heredan todos los modelos ORM."""


_is_sqlite = settings.database_url.startswith("sqlite")
_connect_args = {"check_same_thread": False} if _is_sqlite else {}

engine = create_engine(settings.database_url, connect_args=_connect_args)

# ``expire_on_commit=False`` evita recargas tras hacer commit, de modo que los
# objetos siguen siendo utilizables al serializar la respuesta HTTP.
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


if _is_sqlite:

    @event.listens_for(Engine, "connect")
    def _enable_sqlite_foreign_keys(dbapi_connection, connection_record):  # noqa: ANN001, ARG001
        """Activa la integridad referencial en SQLite (desactivada por defecto)."""
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()


def get_db() -> Generator[Session, None, None]:
    """Dependencia de FastAPI: entrega una sesión por petición y la cierra al final."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Crea las tablas declaradas. Importa los modelos para registrarlos en la metadata."""
    import app.models  # noqa: F401  (registra los modelos en Base.metadata)

    Base.metadata.create_all(bind=engine)
