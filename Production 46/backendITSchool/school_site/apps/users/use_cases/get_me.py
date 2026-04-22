from typing import Self
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserWithPhotoReadSchema
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.services.tokens import TokenServiceProtocol

class GetMeByUserIdUseCaseProtocol(UseCaseProtocol[UserWithPhotoReadSchema]):
    async def __call__(self: Self, user_id: UUID) -> UserWithPhotoReadSchema:
        ...

class GetMeByUserIdUseCase(GetMeByUserIdUseCaseProtocol):
    def __init__(self: Self, token_service: TokenServiceProtocol, user_service: UserServiceProtocol):
        self.user_service = user_service
        self.token_service = token_service


    async def __call__(self: Self, access_token: str) -> UserWithPhotoReadSchema:
        user_data = await self.token_service.decode_access_token(access_token)
        return await self.user_service.get_me(user_data.user_id)
        
