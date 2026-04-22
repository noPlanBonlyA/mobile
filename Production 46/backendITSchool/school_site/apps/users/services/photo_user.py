from fastapi import UploadFile
import logging
from typing import Protocol, Optional
from uuid import UUID, uuid4
from ..schemas import (
    PhotoUserCreateSchema,
    PhotoUserCreateDBSchema,
    PhotoUserUpdateSchema,
    PhotoUserUpdateDBSchema,
    PhotoUserReadSchema
)
from ..repositories.photo_user import PhotoUserRepositoryProtocol
from ....core.services.files import FileServiceProtocol
from school_site.core.utils.exceptions import ImageUploadError

logger = logging.getLogger(__name__)


class PhotoUserServiceProtocol(Protocol):
    async def create(self, photo: PhotoUserCreateSchema, image: UploadFile) -> PhotoUserReadSchema:
        ...

    async def get(self, photo_id: UUID) -> PhotoUserReadSchema:
        ...

    async def update(self, photo_id: UUID, photo: PhotoUserUpdateSchema, image: UploadFile) -> PhotoUserReadSchema:
        ...

    async def get_photo_url(self, path: str) -> str:
        ...

    async def delete(self, photo_id: UUID) -> bool:
        ...


class PhotoUserService(PhotoUserServiceProtocol):
    def __init__(self, 
                 photo_repository: PhotoUserRepositoryProtocol,
                 image_service: FileServiceProtocol
                 ):
        self.photo_repository = photo_repository
        self.image_service = image_service

    async def create(self, photo: PhotoUserCreateSchema, image: UploadFile) -> PhotoUserReadSchema:
        path = self._generate_photo_path(image.filename)
        is_image_uploaded = await self.image_service.upload(path, image)
        if not is_image_uploaded:
            raise ImageUploadError()
        
        photo_for_create = PhotoUserCreateDBSchema(
            name=photo.name,
            user_id=photo.user_id,
            path=path
        )
        created_photo = await self.photo_repository.create(photo_for_create)
        uploaded_photo_url = await self.get_photo_url(created_photo.path)
        return PhotoUserReadSchema(
            id=created_photo.id,
            name=created_photo.name,
            user_id=created_photo.user_id,
            url=uploaded_photo_url
        ) 

    async def get_photo_url(self, path: str):
        uploaded_photo_url = await self.image_service.get_url(path)
        return uploaded_photo_url
    
    async def get(self, photo_id: UUID) -> PhotoUserReadSchema:
        photo = await self.photo_repository.get(photo_id)
        photo_url = await self.get_photo_url(photo.path)
        return PhotoUserReadSchema(
            id=photo.id,
            name=photo.name,
            user_id=photo.user_id,
            url=photo_url,
            created_at=photo.created_at,
            updated_at=photo.updated_at
        )

    async def update(self, photo_id: UUID, photo: PhotoUserUpdateSchema, image: UploadFile) -> PhotoUserReadSchema:
        db_update_photo = PhotoUserUpdateDBSchema(
            id=photo_id,
            user_id=photo.user_id,
            name=photo.name
        )
        updated_photo = await self.photo_repository.update(db_update_photo)
        is_image_uploaded = await self.image_service.upload(updated_photo.path, image)
        if not is_image_uploaded:
            raise ImageUploadError()
        updated_photo_url = await self.get_photo_url(updated_photo.path)
        return PhotoUserReadSchema(
            id=updated_photo.id,
            name=updated_photo.name,
            user_id=updated_photo.user_id,
            url=updated_photo_url,
            created_at=updated_photo.created_at
        ) 

    async def delete(self, photo_id: UUID) -> bool:
        photo = await self.photo_repository.get(photo_id)
        await self.delete_image(photo.path)
        return await self.photo_repository.delete(photo_id)
    
    async def delete_image(self, path: str) -> bool:
        return await self.image_service.delete(path)

    def _generate_photo_path(self, filename: Optional[str]):
        STANDART_PATH = "users/images"
        name = str(uuid4())
        return f"{STANDART_PATH}/{name}{self._get_extension(filename)}"

    def _get_extension(self, filename: Optional[str]) -> str:
        if not filename:
            return ".jpg"
        parts = filename.split('.')
        if len(parts) > 1:
            return f".{parts[-1].lower()}"
        return ".jpg" 