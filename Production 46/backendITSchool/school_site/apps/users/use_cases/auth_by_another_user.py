from typing import Self
from school_site.core.use_cases import UseCaseProtocol 
from school_site.apps.users.schemas import AuthReadSchema, UserIdSchema
from school_site.apps.users.services.auth import AuthByAnotherUserServiceProtocol, AuthServiceProtocol


class AuthByAnotherUserUseCaseProtocol(UseCaseProtocol[AuthReadSchema]):
    async def __call__(self: Self, access_token: str, user: UserIdSchema) -> AuthReadSchema:
        ...


class AuthByAnotherUserUseCase(AuthByAnotherUserUseCaseProtocol):
    def __init__(self: Self, auth_service: AuthServiceProtocol, auth_by_another_user_service: AuthByAnotherUserServiceProtocol):
        self.auth_service = auth_service
        self.auth_by_another_user_service = auth_by_another_user_service
    
    async def __call__(self: Self, access_token: str, user: UserIdSchema) -> AuthReadSchema:
        await self.auth_service.get_super_admin_user(access_token)
        return await self.auth_by_another_user_service.auth_by_another_user(user.user_id)
