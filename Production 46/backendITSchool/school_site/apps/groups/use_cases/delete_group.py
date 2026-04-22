from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..services.groups import GroupServiceProtocol

class DeleteGroupUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, access_token: str, group_id: UUID):
        ...

class DeleteGroupUseCase(DeleteGroupUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminServiceProtocol, group_service: GroupServiceProtocol):
        self.auth_service = auth_service
        self.group_service = group_service
    
    async def __call__(self, access_token: str, group_id: UUID) -> None:
        await self.auth_service.get_admin_user(access_token)
        await self.group_service.delete(group_id) 