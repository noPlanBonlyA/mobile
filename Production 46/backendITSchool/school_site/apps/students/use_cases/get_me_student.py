from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.auth import AuthAdminAndStudentServiceProtocol
from ..services.students import StudentServiceProtocol
from ..schemas import StudentReadWithUserSchema

class GetMeStudentUseCaseProtocol(UseCaseProtocol[StudentReadWithUserSchema]):
    async def __call__(self, access_token: str) -> StudentReadWithUserSchema:
        ...


class GetMeStudentUseCase(GetMeStudentUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndStudentServiceProtocol, student_service: StudentServiceProtocol):
        self.auth_service = auth_service
        self.student_service = student_service

    async def __call__(self, access_token: str) -> StudentReadWithUserSchema:
        user = await self.auth_service.get_student_user(access_token)
        return await self.student_service.get_by_user_id(user.user_id)
