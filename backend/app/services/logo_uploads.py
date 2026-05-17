from uuid import UUID

from fastapi import UploadFile

from app.core.config import settings


def save_logo_upload(file: UploadFile, organization_id: UUID) -> str:
    ext = ""
    if file.filename:
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    filename = f"logo_{organization_id}.{ext}" if ext else f"logo_{organization_id}"
    filepath = f"{settings.upload_dir}/{filename}"
    content = file.file.read()
    if len(content) > settings.max_logo_upload_bytes:
        raise ValueError("El archivo excede el tamaño máximo permitido de 2 MB.")
    with open(filepath, "wb") as f:
        f.write(content)
    return filepath
