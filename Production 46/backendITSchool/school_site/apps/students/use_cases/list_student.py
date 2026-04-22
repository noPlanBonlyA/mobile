from typing import Optional
from school_site.core.schemas import PaginationSchema
from school_site.core.use_cases import UseCaseProtocol 
from ..services.auth import AuthAdminAndStudentServiceProtocol
from ..services.students import StudentServiceProtocol
from ..schemas import StudentPaginationResultSchema

class GetListStudentUseCaseProtocol(UseCaseProtocol[StudentPaginationResultSchema]):
    async def __call__(self, access_token: str, limit: int = 10,
                       offset: int = 0, sorting_by: Optional[str] = None) -> StudentPaginationResultSchema:
        ...


class GetListStudentUseCase(GetListStudentUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndStudentServiceProtocol, student_service: StudentServiceProtocol):
        self.auth_service = auth_service
        self.student_service = student_service

    async def __call__(self, access_token: str, limit: int = 10,
                       offset: int = 0, sorting_by: Optional[str] = None) -> StudentPaginationResultSchema:
        pagination = PaginationSchema(
            limit=limit,
            offset=offset
        )
        return await self.student_service.list(pagination, sorting_by)
