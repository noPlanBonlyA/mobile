from fastapi import UploadFile
from typing import Optional
from uuid import UUID
import json
from school_site.core.use_cases import UseCaseProtocol 
from ..services.products import PhotoServiceProtocol 
from school_site.apps.users.services.tokens import TokenServiceProtocol 
from ..schemas import PhotoReadSchema, PhotoUpdateSchema

class UpdatePhotoUseCaseProtocol(UseCaseProtocol[PhotoReadSchema]):
    async def __call__(self, token: str, product_id: UUID, photo_id: UUID, photo_data: str, image: Optional[UploadFile]) -> PhotoReadSchema:
        ...


class UpdatePhotoUseCase(UpdatePhotoUseCaseProtocol):
    def __init__(self, auth_service: TokenServiceProtocol, photo_service: PhotoServiceProtocol):
        self.auth_service = auth_service
        self.photo_service = photo_service
    
    async def __call__(self, token: str, product_id: UUID, photo_id: UUID, photo_data: str, image: Optional[UploadFile]) -> PhotoReadSchema:
        await self.auth_service.get_admin_user(token)
        photo_json = json.loads(photo_data)
        photo = PhotoUpdateSchema(
            name=photo_json["name"],
            product_id=product_id,
            id=photo_id
        )
        return await self.photo_service.update(photo_id, photo, image)
