from fastapi import UploadFile
from minio import Minio
from minio.error import S3Error
import asyncio
import io
from typing import Protocol
from datetime import timedelta
import logging
from school_site.settings import settings

logger = logging.getLogger(__name__)


class FileServiceProtocol(Protocol):
    async def upload(self, path: str, file: UploadFile) -> bool:
        ...
    
    async def get_url(self, path: str) -> str:
         ...
    
        
    async def delete(self, file_id: str) -> bool:
         ...

    async def upload_html(self, path: str, html_text: str) -> bool:
        ...


class MinioFileService(FileServiceProtocol):
    def __init__(self, minio_client: Minio, bucket_name: str):
        self.client = minio_client
        self.bucket_name = bucket_name
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            raise Exception(f"Failed to create bucket: {e}")
        
    async def upload(self, path: str, file: UploadFile) -> bool:
        file_data = await file.read()
        await self._run_sync(
            self.client.put_object,
            self.bucket_name,
            path,
            io.BytesIO(file_data),
            len(file_data),
            file.content_type
        )
        return True
    
    async def upload_html(self, path: str, html_text: str) -> bool:
        """
        Загружает HTML-текст как файл в MinIO
        
        :param path: Путь/имя файла в MinIO (например, "lessons/abc123.html")
        :param html_text: HTML-контент
        :return: True при успехе
        """
        try:
            file_data = html_text.encode("utf-8")
            
            await self._run_sync(
                self.client.put_object,
                self.bucket_name,
                path,
                io.BytesIO(file_data),
                len(file_data),
                "text/html"
            )
            return True
        except Exception as e:
            logger.error(f"Failed to upload HTML to MinIO: {e}")
            return False
    

    async def get_url(self, path: str) -> str:
        original_url = await self._run_sync(
            self.client.presigned_get_object,
            self.bucket_name,
            path,
            timedelta(minutes=30)
        )    
        new_url = original_url.replace("http://minio:9000", f"{settings.frontend_url}/minio")

        return new_url
        

    async def delete(self, path: str) -> bool:
        """
        Удаляет изображение из MinIO по image_id (пути)
        
        :param image_id: Путь к объекту в MinIO (например, "products/123/photo.jpg")
        :return: True если удален, False если объект не найден
        """
        try:
            await self._run_sync(
                self.client.stat_object,
                self.bucket_name,
                path
            )
            await self._run_sync(
                self.client.remove_object,
                self.bucket_name,
                path
            )
            return True
        except S3Error as e:
            if e.code == 'NoSuchKey':
                return False  
            raise  

    async def _run_sync(self, func, *args):
        """Обертка для выполнения синхронных MinIO-операций в executor'е"""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, func, *args)
