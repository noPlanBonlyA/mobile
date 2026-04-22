from school_site.core.use_cases import UseCaseProtocol
from ..schemas import GroupReadSchema, GroupCreateSchema
from ..services.auth import AuthAdminServiceProtocol
from ..services.groups import GroupServiceProtocol

class CreateGroupUseCaseProtocol(UseCaseProtocol[GroupReadSchema]):
    async def __call__(self, access_token: str, group: GroupCreateSchema):
        ...

class CreateGroupUseCase(CreateGroupUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminServiceProtocol, group_service: GroupServiceProtocol):
        self.auth_service = auth_service
        self.group_service = group_service
    
    async def __call__(self, access_token: str, group: GroupCreateSchema):
        await self.auth_service.get_admin_user(access_token)
        return await self.group_service.create(group) 