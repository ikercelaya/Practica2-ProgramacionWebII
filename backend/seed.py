"""Script de inicialización de datos (seed).

Crea los usuarios de prueba (admin/admin123 y user/user123) y unos productos de
ejemplo. Es idempotente: no duplica datos si ya existen.

Uso:
    python seed.py
"""
from sqlalchemy import select

from app.core.database import SessionLocal, init_db
from app.core.security import hash_password
from app.models.producto import Producto
from app.models.user import User


def seed() -> None:
    init_db()
    db = SessionLocal()
    try:
        if db.scalar(select(User).limit(1)) is None:
            db.add_all(
                [
                    User(username="admin", password=hash_password("admin123"), role="admin"),
                    User(username="user", password=hash_password("user123"), role="user"),
                ]
            )
            db.commit()
            print("Usuarios de prueba creados: admin/admin123 (admin), user/user123 (user)")
        else:
            print("Ya existen usuarios. Se omite el seed de usuarios.")

        if db.scalar(select(Producto).limit(1)) is None:
            db.add_all(
                [
                    Producto(nombre="Teclado mecánico", precio=79.99, imagen=None),
                    Producto(nombre="Ratón inalámbrico", precio=29.50, imagen=None),
                    Producto(nombre="Monitor 27\" 4K", precio=329.00, imagen=None),
                    Producto(nombre="Auriculares Bluetooth", precio=59.95, imagen=None),
                ]
            )
            db.commit()
            print("Productos de ejemplo creados.")
        else:
            print("Ya existen productos. Se omite el seed de productos.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
