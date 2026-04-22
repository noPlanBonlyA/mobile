from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.auth import AuthAdminAndTeacherServiceProtocol
from ..services.teachers import TeacherServiceProtocol
from ..schemas import TeacherReadWithUserSchema


class GetTeacherUseCaseProtocol(UseCaseProtocol[TeacherReadWithUserSchema]):
    async def __call__(self, access_token: str, teacher_id: UUID) -> TeacherReadWithUserSchema:
        ...


class GetTeacherUseCase(GetTeacherUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndTeacherServiceProtocol, teacher_service: TeacherServiceProtocol):
        self.auth_service = auth_service
        self.teacher_service = teacher_service

    async def __call__(self, access_token: str, teacher_id: UUID) -> TeacherReadWithUserSchema:
        await self.auth_service.get_admin_user(access_token)
        return await self.teacher_service.get(teacher_id) 