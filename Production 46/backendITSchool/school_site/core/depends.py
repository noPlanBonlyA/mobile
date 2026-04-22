from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .services.files import FileServiceProtocol, MinioFileService
from .clients.minio import get_minio_client

def get_image_service(bucket_name: str) -> FileServiceProtocol:
    """Глобальная зависимость для получения сервиса изображений."""
    client = get_minio_client() 
    return MinioFileService(client, bucket_name)

def get_scheduler() -> AsyncIOScheduler:
    return AsyncIOScheduler()