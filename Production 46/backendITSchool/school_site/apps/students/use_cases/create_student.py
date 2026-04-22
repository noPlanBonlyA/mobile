from school_site.core.use_cases import UseCaseProtocol 
from ..schemas import StudentReadSchema, StudentCreateSchema
from ..services.auth import AuthAdminAndStudentServiceProtocol
from ..services.students import StudentServiceProtocol

class CreateStudentUseCaseProtocol(UseCaseProtocol[StudentReadSchema]):
    async def __call__(self, student: StudentCreateSchema):
        ...


class CreateStudentUseCase(CreateStudentUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndStudentServiceProtocol, student_service: StudentServiceProtocol):
        self.auth_service = auth_service
        self.student_service = student_service

    async def __call__(self, access_token: str, student: StudentCreateSchema):
        await self.auth_service.get_admin_user(access_token)
        return await self.student_service.create(student)
