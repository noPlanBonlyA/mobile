from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..schemas import StudentReadSchema, StudentUpdateSchema
from ..services.auth import AuthAdminAndStudentServiceProtocol
from ..services.students import StudentServiceProtocol

class UpdateStudentUseCaseProtocol(UseCaseProtocol[StudentReadSchema]):
    async def __call__(self, access_token: str, student_id: UUID, student: StudentUpdateSchema):
        ...


class UpdateStudentUseCase(UpdateStudentUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndStudentServiceProtocol, student_service: StudentServiceProtocol):
        self.auth_service = auth_service
        self.student_service = student_service

    async def __call__(self, access_token: str, student_id: UUID, student: StudentUpdateSchema):
        await self.auth_service.get_admin_user(access_token)
        return await self.student_service.update(student_id, student)
