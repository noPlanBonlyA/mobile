from school_site.core.use_cases import UseCaseProtocol 
from school_site.apps.users.services.auth import AuthServiceProtocol 


class LogoutUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, refresh_token: str) -> None:
        ...


class LogoutUseCase(LogoutUseCaseProtocol):
    def __init__(self, auth_service: AuthServiceProtocol):
        self.auth_service = auth_service
    
    async def __call__(self, refresh_token: str) -> None:
        return await self.auth_service.logout(refresh_token)
