from typing import Self, Optional
from fastapi import UploadFile
import json
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import RegisterRequestSchema, UserWithPhotoReadSchema
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol
from school_site.apps.users.services.permissions import permission_service


class CreateUserUseCaseProtocol(UseCaseProtocol[UserWithPhotoReadSchema]):
    async def __call__(self: Self, user_data: str, image: Optional[UploadFile]) -> UserWithPhotoReadSchema:
        ...

class CreateUserUseCase(CreateUserUseCaseProtocol):
    def __init__(self: Self, auth_service: AuthServiceProtocol, user_service: UserServiceProtocol):
        self.auth_service = auth_service
        self.user_service = user_service

    async def __call__(self: Self, access_token: str, user_data: str, image: Optional[UploadFile] = None) -> UserWithPhotoReadSchema:
        current_user = await self.auth_service.get_admin_user(access_token)
        user_schema = RegisterRequestSchema(**json.loads(user_data))
        permission_service.check(
            "create_user",
            current_user=current_user,
            user_data=user_schema
        )
        
        return await self.user_service.create_user(user_schema, image)