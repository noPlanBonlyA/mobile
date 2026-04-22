from minio import Minio
from school_site.settings import settings

def get_minio_client() -> Minio:
    """Создает и возвращает MinIO-клиент."""
    return Minio(
        endpoint=settings.minio.endpoint,
        access_key=settings.minio.access_key,
        secret_key=settings.minio.secret_key,
        secure=settings.minio.secure
    )