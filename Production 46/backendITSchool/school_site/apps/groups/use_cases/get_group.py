from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.groups import GroupServiceProtocol
from ..schemas import GroupWithStudentsAndTeacherAndCoursesSchema

class GetGroupUseCaseProtocol(UseCaseProtocol[GroupWithStudentsAndTeacherAndCoursesSchema]):
    async def __call__(self, group_id: UUID) -> GroupWithStudentsAndTeacherAndCoursesSchema:
        ...

class GetGroupUseCase(GetGroupUseCaseProtocol):
    def __init__(self, group_service: GroupServiceProtocol):
        self.group_service = group_service
    
    async def __call__(self, group_id: UUID) -> GroupWithStudentsAndTeacherAndCoursesSchema:
        return await self.group_service.get(group_id) 