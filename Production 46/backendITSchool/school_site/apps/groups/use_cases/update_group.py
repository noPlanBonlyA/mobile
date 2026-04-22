from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..schemas import GroupReadSchema, GroupUpdateSchema
from ..services.auth import AuthAdminServiceProtocol
from ..services.groups import GroupServiceProtocol

class UpdateGroupUseCaseProtocol(UseCaseProtocol[GroupReadSchema]):
    async def __call__(self, access_token: str, group_id: UUID, group: GroupUpdateSchema):
        ...

class UpdateGroupUseCase(UpdateGroupUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminServiceProtocol, group_service: GroupServiceProtocol):
        self.auth_service = auth_service
        self.group_service = group_service
    
    async def __call__(self, access_token: str, group_id: UUID, group: GroupUpdateSchema):
        await self.auth_service.get_admin_user(access_token)
        return await self.group_service.update(group_id, group) 