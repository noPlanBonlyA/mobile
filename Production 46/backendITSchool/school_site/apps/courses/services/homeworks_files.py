from fastapi import UploadFile
import logging
from typing import Protocol, Optional
from uuid import UUID, uuid4
from pydantic import HttpUrl
from school_site.core.utils.exceptions import ImageUploadError
from ..schemas import (
    FileHomeworkCreateSchema,
    FileHomeworkCreateDBSchema,
    FileHomeworkUpdateSchema,
    FileHomeworkUpdateDBSchema,
    FileHomeworkReadSchema
)
from ..repositories.homework_files import FileHomeworkRepositoryProtocol
from school_site.core.services.files import FileServiceProtocol

logger = logging.getLogger(__name__)


class FileHomeworkServiceProtocol(Protocol):
    async def create(self, file_create: FileHomeworkCreateSchema, file: UploadFile) -> FileHomeworkReadSchema:
        ...

    async def get(self, file_id: UUID) -> FileHomeworkReadSchema:
        ...

    async def update(self, file_id: UUID, file_update: FileHomeworkUpdateSchema, file: UploadFile) -> FileHomeworkReadSchema:
        ...

    async def get_file_url(self, path: str) -> HttpUrl:
        ...

    async def delete(self, file_id: UUID) -> bool:
        ...


class FileHomeworkService(FileHomeworkServiceProtocol):
    def __init__(
        self,
        file_repository: FileHomeworkRepositoryProtocol,
        file_service: FileServiceProtocol
    ):
        self.file_repository = file_repository
        self.file_service = file_service

    async def create(self, file_create: FileHomeworkCreateSchema, file: UploadFile) -> FileHomeworkReadSchema:
        path = self._generate_file_path(file.filename)
        is_file_uploaded = await self.file_service.upload(path, file)
        
        if not is_file_uploaded:
            raise ImageUploadError()

        db_file = FileHomeworkCreateDBSchema(
            name=file_create.name,
            path=path
        )
        created_file = await self.file_repository.create(db_file)
        file_url = await self.get_file_url(created_file.path)

        return FileHomeworkReadSchema(
            id=created_file.id,
            name=created_file.name,
            url=file_url
        )

    async def get(self, file_id: UUID) -> FileHomeworkReadSchema:
        db_file = await self.file_repository.get(file_id)
        file_url = await self.get_file_url(db_file.path)

        return FileHomeworkReadSchema(
            id=db_file.id,
            name=db_file.name,
            url=file_url,
            created_at=db_file.created_at,
            updated_at=db_file.updated_at
        )

    async def update(self, file_id: UUID, file_update: FileHomeworkUpdateSchema, file: Optional[UploadFile]) -> FileHomeworkReadSchema:
        db_update = FileHomeworkUpdateDBSchema(
            id=file_id,
            name=file_update.name,
        )
        updated_file = await self.file_repository.update(db_update)
        if file:
            is_file_uploaded = await self.file_service.upload(updated_file.path, file)
            if not is_file_uploaded:
                raise ImageUploadError()

        file_url = await self.get_file_url(updated_file.path)
        return FileHomeworkReadSchema(
            id=updated_file.id,
            name=updated_file.name,
            url=file_url,
            created_at=updated_file.created_at
        )

    async def delete(self, file_id: UUID) -> bool:
        db_file = await self.file_repository.get(file_id)
        is_deleted = await self.file_repository.delete(file_id)
        await self.delete_file(db_file.path)
        return is_deleted

    async def delete_file(self, path: str) -> bool:
        return await self.file_service.delete(path)

    async def get_file_url(self, path: str) -> HttpUrl:
        return await self.file_service.get_url(path)

    def _generate_file_path(self, filename: str) -> str:
        STANDARD_PATH = "homeworks/files"
        return f"{STANDARD_PATH}/{uuid4()}{self._get_extension(filename)}"

    def _get_extension(self, filename: Optional[str]) -> str:
        if not filename:
            return ".txt"
        
        parts = filename.split('.')
        if len(parts) > 1:
            return f".{parts[-1].lower()}"
        return ".txt"