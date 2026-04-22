from school_site.core.use_cases import UseCaseProtocol
from ..services.groups import GroupServiceProtocol
from ..schemas import GroupPaginationResultSchema
from school_site.core.schemas import PaginationSchema

class GetListGroupsUseCaseProtocol(UseCaseProtocol[GroupPaginationResultSchema]):
    async def __call__(self, 
                       limit: int = 10, 
                       offset: int = 0) -> GroupPaginationResultSchema:
        ...

class GetListGroupsUseCase(GetListGroupsUseCaseProtocol):
    def __init__(self, group_service: GroupServiceProtocol):
        self.group_service = group_service
    
    async def __call__(self, 
                       limit: int = 10, 
                       offset: int = 0) -> GroupPaginationResultSchema:
        pagination = PaginationSchema(
            limit=limit, 
            offset=offset
            )
        return await self.group_service.list(pagination) 