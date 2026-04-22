from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.products import PhotoServiceProtocol 
from ..schemas import PhotoReadSchema 

class GetPhotoUseCaseProtocol(UseCaseProtocol[PhotoReadSchema]):
    async def __call__(self, photo_id: UUID) -> PhotoReadSchema:
        ...


class GetPhotoUseCase(GetPhotoUseCaseProtocol):
    def __init__(self, photo_service: PhotoServiceProtocol):
        self.photo_service = photo_service
    
    async def __call__(self, photo_id: UUID) -> PhotoReadSchema:
        return await self.photo_service.get(photo_id)
