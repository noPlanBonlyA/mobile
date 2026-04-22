from typing import Self
from school_site.core.use_cases import UseCaseProtocol 
from school_site.apps.users.schemas import AuthReadSchema, PasswordChangeSchema
from school_site.apps.users.services.auth import AuthServiceProtocol 


class ChangePasswordUseCaseProtocol(UseCaseProtocol[AuthReadSchema]):
    async def __call__(self: Self, username: str, password: str) -> AuthReadSchema:
        ...


class ChangePasswordUseCase(ChangePasswordUseCaseProtocol):
    def __init__(self: Self, auth_service: AuthServiceProtocol):
        self.auth_service = auth_service
    
    async def __call__(self: Self, access_token: str, password: PasswordChangeSchema) -> AuthReadSchema:
        return await self.auth_service.change_password_authenticated(access_token, password)
