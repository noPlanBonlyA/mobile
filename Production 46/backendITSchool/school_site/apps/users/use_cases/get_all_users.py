from typing import Self, List, Optional
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.users.schemas import UserWithPhotoReadSchema, PaginationResultSchema
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.services.auth import AuthServiceProtocol
from school_site.core.enums import UserRole
from school_site.apps.users.services.permissions import permission_service

class GetAllUsersUseCaseProtocol(UseCaseProtocol[PaginationResultSchema[UserWithPhotoReadSchema]]):
    async def __call__(self: Self) -> List[UserWithPhotoReadSchema]:
        ...

class GetAllUsersUseCase(UseCaseProtocol[PaginationResultSchema[UserWithPhotoReadSchema]]):
    def __init__(self, auth_service: AuthServiceProtocol, user_service: UserServiceProtocol):
        self.auth_service = auth_service
        self.user_service = user_service

    async def __call__(self: Self, access_token: str, role: Optional[UserRole] = None, limit: int = 10, offset: int = 0) -> PaginationResultSchema[UserWithPhotoReadSchema]:
        current_user = await self.auth_service.get_admin_user(access_token)
        
        if permission_service.check("get_all_users", current_user=current_user):
            role = UserRole.STUDENT
            
        return await self.user_service.get_all_users(role, limit, offset)