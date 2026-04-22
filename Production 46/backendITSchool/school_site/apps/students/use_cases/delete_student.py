from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.auth import AuthAdminAndStudentServiceProtocol
from ..services.students import StudentServiceProtocol

class DeleteStudentUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, access_token: str, student_id: UUID):
        ...


class DeleteStudentUseCase(DeleteStudentUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndStudentServiceProtocol, student_service: StudentServiceProtocol):
        self.auth_service = auth_service
        self.student_service = student_service

    async def __call__(self, access_token: str, student_id: UUID) -> None:
        await self.auth_service.get_admin_user(access_token)
        await self.student_service.delete(student_id)
