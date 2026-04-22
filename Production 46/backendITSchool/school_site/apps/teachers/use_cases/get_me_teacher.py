from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.auth import AuthAdminAndTeacherServiceProtocol
from ..services.teachers import TeacherServiceProtocol
from ..schemas import TeacherReadWithUserSchema


class GetMeTeacherUseCaseProtocol(UseCaseProtocol[TeacherReadWithUserSchema]):
    async def __call__(self, access_token: str) -> TeacherReadWithUserSchema:
        ...


class GetMeTeacherUseCase(GetMeTeacherUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndTeacherServiceProtocol, teacher_service: TeacherServiceProtocol):
        self.auth_service = auth_service
        self.teacher_service = teacher_service

    async def __call__(self, access_token: str) -> TeacherReadWithUserSchema:
        user = await self.auth_service.get_teacher_user(access_token)
        return await self.teacher_service.get_by_user_id(user.user_id) 