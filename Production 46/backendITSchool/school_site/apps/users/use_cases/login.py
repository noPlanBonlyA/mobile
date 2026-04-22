from school_site.core.use_cases import UseCaseProtocol 
from school_site.apps.users.schemas import AuthReadSchema
from school_site.apps.users.services.auth import AuthServiceProtocol 


class LoginUseCaseProtocol(UseCaseProtocol[AuthReadSchema]):
    async def __call__(self, username: str, password: str) -> AuthReadSchema:
        ...


class LoginUseCase(LoginUseCaseProtocol):
    def __init__(self, auth_service: AuthServiceProtocol):
        self.auth_service = auth_service
    
    async def __call__(self, username: str, password: str) -> AuthReadSchema:
        return await self.auth_service.login(username, password)
