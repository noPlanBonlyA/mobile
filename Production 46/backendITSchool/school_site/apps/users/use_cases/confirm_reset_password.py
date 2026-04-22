from school_site.core.use_cases import UseCaseProtocol 
from school_site.apps.users.services.auth import ResetPasswordServiceProtocol 
from ..schemas import ResetPasswordRequest, AuthReadSchema

class ConfirmResetPasswordUseCaseProtocol(UseCaseProtocol[AuthReadSchema]):
    async def __call__(self, reset_password: ResetPasswordRequest) -> AuthReadSchema:
        ...


class ConfirmResetPasswordUseCase(ConfirmResetPasswordUseCaseProtocol):
    def __init__(self, reset_password_service: ResetPasswordServiceProtocol):
        self.reset_password_service = reset_password_service
    
    async def __call__(self, reset_password: ResetPasswordRequest) -> AuthReadSchema:
        return await self.reset_password_service.confirm_reset_password(reset_password)
