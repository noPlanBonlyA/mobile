from school_site.core.use_cases import UseCaseProtocol 
from school_site.apps.users.services.auth import ResetPasswordServiceProtocol 
from ..schemas import UserResetSchema

class ResetPasswordUseCaseProtocol(UseCaseProtocol[bool]):
    async def __call__(self, user: UserResetSchema) -> bool:
        ...


class ResetPasswordUseCase(ResetPasswordUseCaseProtocol):
    def __init__(self, reset_password_service: ResetPasswordServiceProtocol):
        self.reset_password_service = reset_password_service
    
    async def __call__(self, user: UserResetSchema) -> bool:
        return await self.reset_password_service.reset_password(user)
