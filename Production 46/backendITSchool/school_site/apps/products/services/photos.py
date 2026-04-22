from fastapi import UploadFile
import logging
from typing import Protocol, Optional
from uuid import UUID, uuid4
from ..schemas import (
    PhotoCreateSchema,
    PhotoCreateDBSchema,
    PhotoUpdateSchema,
    PhotoUpdateDBSchema,
    PhotoReadSchema
)
from ..repositories.photos import PhotoRepositoryProtocol
from ....core.services.files import FileServiceProtocol
from ..exceptions import ImageUploadError

logger = logging.getLogger(__name__)



class PhotoServiceProtocol(Protocol):
    async def create(self, photo: PhotoCreateSchema, image: UploadFile) -> PhotoReadSchema:
        ...

    async def get(self, photo_id: UUID) -> PhotoReadSchema:
        ...

    async def update(self, photo_id: UUID, photo: PhotoUpdateSchema, image: UploadFile) -> PhotoReadSchema:
        ...

    async def get_photo_url(self, path: str) -> str:
        ...

    async def delete(self, photo_id: UUID) -> bool:
        ...


class PhotoService(PhotoServiceProtocol):
    def __init__(self, 
                 photo_repository: PhotoRepositoryProtocol,
                 image_service: FileServiceProtocol
                 ):
        self.photo_repository = photo_repository
        self.image_service = image_service


    async def create(self, photo: PhotoCreateSchema, image: UploadFile) -> PhotoReadSchema:
        path = self._generate_photo_path(image.filename)
        is_image_uploaded = await self.image_service.upload(path, image)
        if not is_image_uploaded:
            raise ImageUploadError()
        
        photo_for_create = PhotoCreateDBSchema(
            name=photo.name,
            product_id=photo.product_id,
            path=path
        )
        created_photo = await self.photo_repository.create(photo_for_create)
        uploaded_photo_url = await self.get_photo_url(created_photo.path)
        return PhotoReadSchema(
            id=created_photo.id,
            name=created_photo.name,
            product_id=created_photo.product_id,
            url=uploaded_photo_url
        ) 


    async def get_photo_url(self, path: str):
        uploaded_photo_url = await self.image_service.get_url(path)
        return uploaded_photo_url
    

    async def get(self, photo_id: UUID) -> PhotoReadSchema:
        photo = await self.photo_repository.get(photo_id)
        photo_url = await self.get_photo_url(photo.path)
        return PhotoReadSchema(
            id=photo.id,
            name=photo.name,
            product_id=photo.product_id,
            url=photo_url,
            created_at=photo.created_at,
            updated_at=photo.updated_at
        )


    async def update(self, photo_id: UUID, photo: PhotoUpdateSchema, image: UploadFile) -> PhotoReadSchema:
        db_update_photo = PhotoUpdateDBSchema(
            id=photo_id,
            product_id=photo.product_id,
            name=photo.name
        )
        updated_photo = await self.photo_repository.update(db_update_photo)
        is_image_uploaded = await self.image_service.upload(updated_photo.path, image)
        if not is_image_uploaded:
            raise ImageUploadError()
        updated_photo_url = await self.get_photo_url(updated_photo.path)
        return PhotoReadSchema(
            id=updated_photo.id,
            name=updated_photo.name,
            product_id=updated_photo.product_id,
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
        STANDART_PATH = "products/images"

        name = str(uuid4())
        return f"{STANDART_PATH}/{name}{self._get_extension(filename)}"


    def _get_extension(self, filename: Optional[str]) -> str:
        if not filename:
            return ".jpg"
        
        parts = filename.split('.')
        if len(parts) > 1:
            return f".{parts[-1].lower()}"
        return ".jpg"