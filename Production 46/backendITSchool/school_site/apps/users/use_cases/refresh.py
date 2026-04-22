from school_site.core.use_cases import UseCaseProtocol 
from school_site.apps.users.schemas import AuthReadSchema
from school_site.apps.users.services.auth import AuthServiceProtocol 


class RefreshUseCaseProtocol(UseCaseProtocol[AuthReadSchema]):
    async def __call__(self, refresh_token: str) -> AuthReadSchema:
        ...


class RefreshUseCase(RefreshUseCaseProtocol):
    def __init__(self, auth_service: AuthServiceProtocol):
        self.auth_service = auth_service
    
    async def __call__(self, refresh_token: str) -> AuthReadSchema:
        return await self.auth_service.refresh(refresh_token)
