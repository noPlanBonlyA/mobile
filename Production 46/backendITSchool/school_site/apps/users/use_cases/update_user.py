from typing import Self, Optional
from uuid import UUID
from fastapi import UploadFile
import json
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserWithPhotoReadSchema, UserUpdateRequestSchema
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol
from school_site.apps.users.services.permissions import permission_service


class UpdateUserUseCaseProtocol(UseCaseProtocol[UserWithPhotoReadSchema]):
    async def __call__(self: Self, url_user_id: UUID, user_data: str, image: Optional[UploadFile]) -> UserWithPhotoReadSchema:
        ...

class UpdateUserUseCase(UpdateUserUseCaseProtocol):
    def __init__(self: Self, auth_service: AuthServiceProtocol, user_service: UserServiceProtocol):
        self.auth_service = auth_service
        self.user_service = user_service

    async def __call__(self: Self, access_token: str, url_user_id: UUID, user_data: str, image: Optional[UploadFile] = None) -> UserWithPhotoReadSchema:
        current_user = await self.auth_service.decode_acess_token(access_token)
        user_schema = UserUpdateRequestSchema(**json.loads(user_data))

        permission_service.check(
            "update_user",
            current_user=current_user,
            target_user=user_schema,
            target_user_id=url_user_id
        )
        
        return await self.user_service.update_user_by_router(url_user_id, user_schema, image)