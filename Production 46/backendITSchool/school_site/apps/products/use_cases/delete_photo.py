from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.products import PhotoServiceProtocol 
from school_site.apps.users.services.tokens import TokenServiceProtocol 

class DeletePhotoUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, token: str, photo_id: UUID) -> None:
        ...


class DeletePhotoUseCase(DeletePhotoUseCaseProtocol):
    def __init__(self, auth_service: TokenServiceProtocol, photo_service: PhotoServiceProtocol):
        self.auth_service = auth_service
        self.photo_service = photo_service
    
    async def __call__(self, token: str, photo_id: UUID) -> None:
        await self.auth_service.get_admin_user(token)
        return await self.photo_service.delete(photo_id)
