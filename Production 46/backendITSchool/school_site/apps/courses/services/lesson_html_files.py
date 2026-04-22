import logging
from typing import Protocol, Optional
from uuid import UUID, uuid4
from ..schemas import (
    LessonHTMLCreateSchema,
    LessonHTMLTextCreateSchema,
    LessonHTMLTextUpdateSchema,
    LessonHTMLReadSchema,
    LessonHTMLUpdateSchema,
    LessonHTMLCreateDBSchema,
    LessonHTMLUpdateDBSchema
)
from ..repositories.lesson_html_files import LessonHTMLRepositoryProtocol
from ....core.services.files import FileServiceProtocol
from school_site.core.utils.exceptions import ImageUploadError

logger = logging.getLogger(__name__)



class LessonHTMLServiceProtocol(Protocol):
    async def create(self, file: LessonHTMLCreateSchema) -> LessonHTMLReadSchema:
        ...

    async def create_by_text(self, file: LessonHTMLTextCreateSchema) -> LessonHTMLReadSchema:
        ...

    async def get(self, file_id: UUID) -> LessonHTMLReadSchema:
        ...

    async def update(self, file_id: UUID, file: LessonHTMLUpdateSchema) -> LessonHTMLReadSchema:
        ...

    async def update_by_text(self, file_id: UUID, file: LessonHTMLTextUpdateSchema) -> LessonHTMLReadSchema:
        ...

    async def get_file_url(self, path: str) -> str:
        ...

    async def delete(self, file_id: UUID) -> bool:
        ...


class LessonHTMLService(LessonHTMLServiceProtocol):
    def __init__(self, 
                 files_repository: LessonHTMLRepositoryProtocol,
                 file_service: FileServiceProtocol
                 ):
        self.files_repository = files_repository
        self.file_service = file_service


    async def create(self, file: LessonHTMLCreateSchema) -> LessonHTMLReadSchema:
        path = self._generate_file_path(file.file.filename)
        is_file_uploaded = await self.file_service.upload(path, file.file)
        if not is_file_uploaded:
            raise ImageUploadError()
        
        file_for_create = LessonHTMLCreateDBSchema(
            name=file.name,
            path=path
        )
        created_file = await self.files_repository.create(file_for_create)
        uploaded_file_url = await self.get_file_url(created_file.path)
        return LessonHTMLReadSchema(
            id=created_file.id,
            name=created_file.name,
            url=uploaded_file_url
        ) 

    async def create_by_text(self, file: LessonHTMLTextCreateSchema) -> LessonHTMLReadSchema:
        path = self._generate_file_path(f"{file.name}.html")
        is_file_uploaded = await self.file_service.upload_html(path, file.html_text)
        if not is_file_uploaded:
            raise ImageUploadError()
        
        file_for_create = LessonHTMLCreateDBSchema(
            name=file.name,
            path=path
        )
        created_file = await self.files_repository.create(file_for_create)
        uploaded_file_url = await self.get_file_url(created_file.path)
        return LessonHTMLReadSchema(
            id=created_file.id,
            name=created_file.name,
            url=uploaded_file_url
        ) 
    
    async def update_by_text(self, file_id: UUID, file: LessonHTMLTextUpdateSchema) -> LessonHTMLReadSchema:
        db_update_file = LessonHTMLUpdateDBSchema(
            id=file_id,
            name=file.name
        )
        updated_file = await self.files_repository.update(db_update_file)
        is_file_uploaded = await self.file_service.upload_html(updated_file.path, file.html_text)
        if not is_file_uploaded:
            raise ImageUploadError()
        updated_file_url = await self.get_file_url(updated_file.path)
        return LessonHTMLReadSchema(
            id=updated_file.id,
            name=updated_file.name,
            url=updated_file_url,
            created_at=updated_file.created_at
        )

    async def get_file_url(self, path: str) -> str:
        uploaded_file_url = await self.file_service.get_url(path)
        return uploaded_file_url
    

    async def get(self, file_id: UUID) -> LessonHTMLReadSchema:
        file = await self.files_repository.get(file_id)
        file_url = await self.get_file_url(file.path)
        return LessonHTMLReadSchema(
            id=file.id,
            name=file.name,
            url=file_url,
            created_at=file.created_at,
            updated_at=file.updated_at
        )


    async def update(self, file_id: UUID, file: LessonHTMLUpdateSchema) -> LessonHTMLReadSchema:
        db_update_file = LessonHTMLUpdateDBSchema(
            id=file_id,
            name=file.name
        )
        updated_file = await self.files_repository.update(db_update_file)
        is_file_uploaded = await self.file_service.upload(updated_file.path, file.file)
        if not is_file_uploaded:
            raise ImageUploadError()
        updated_file_url = await self.get_file_url(updated_file.path)
        return LessonHTMLReadSchema(
            id=updated_file.id,
            name=updated_file.name,
            url=updated_file_url,
            created_at=updated_file.created_at
        ) 


    async def delete(self, file_id: UUID) -> bool:
        file = await self.files_repository.get(file_id)
        is_deleted = await self.files_repository.delete(file_id)
        await self.delete_file(file.path)
        return is_deleted 
    

    async def delete_file(self, path: str) -> bool:
        return await self.file_service.delete(path)


    def _generate_file_path(self, filename: Optional[str]) -> str:
        STANDARD_PATH = "lessons/files"
        return f"{STANDARD_PATH}/{uuid4()}{self._get_extension(filename)}"

    def _get_extension(self, filename: Optional[str]) -> str:
        if not filename:
            return ".html"
        
        parts = filename.split('.')
        if len(parts) > 1:
            return f".{parts[-1].lower()}"
        return ".html"