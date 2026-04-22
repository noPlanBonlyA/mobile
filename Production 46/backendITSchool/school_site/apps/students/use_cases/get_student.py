from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.auth import AuthAdminAndStudentServiceProtocol
from ..services.students import StudentServiceProtocol
from ..schemas import StudentReadWithUserSchema

class GetStudentUseCaseProtocol(UseCaseProtocol[StudentReadWithUserSchema]):
    async def __call__(self, access_token: str, student_id: UUID) -> StudentReadWithUserSchema:
        ...


class GetStudentUseCase(GetStudentUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndStudentServiceProtocol, student_service: StudentServiceProtocol):
        self.auth_service = auth_service
        self.student_service = student_service

    async def __call__(self, access_token: str, student_id: UUID) -> StudentReadWithUserSchema:
        await self.auth_service.get_admin_user(access_token)
        return await self.student_service.get(student_id)
