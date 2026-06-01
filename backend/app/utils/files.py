"""Guardado de imágenes de producto subidas vía ``multipart/form-data``."""
import os
import uuid

from fastapi import UploadFile

from app.core.config import settings


def save_upload_file(file: UploadFile) -> str:
    """Guarda el archivo con un nombre único y devuelve dicho nombre.

    El nombre se almacena en la columna ``imagen`` del producto y el archivo se
    sirve estáticamente desde ``/uploads/<nombre>``.
    """
    os.makedirs(settings.upload_dir, exist_ok=True)
    _, ext = os.path.splitext(file.filename or "")
    filename = f"{uuid.uuid4().hex}{ext.lower()}"
    destination = os.path.join(settings.upload_dir, filename)
    with open(destination, "wb") as buffer:
        buffer.write(file.file.read())
    return filename
