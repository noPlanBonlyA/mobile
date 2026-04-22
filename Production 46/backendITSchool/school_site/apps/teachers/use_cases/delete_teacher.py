from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..services.auth import AuthAdminAndTeacherServiceProtocol
from ..services.teachers import TeacherServiceProtocol


class DeleteTeacherUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, access_token: str, teacher_id: UUID):
        ...


class DeleteTeacherUseCase(DeleteTeacherUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndTeacherServiceProtocol, teacher_service: TeacherServiceProtocol):
        self.auth_service = auth_service
        self.teacher_service = teacher_service

    async def __call__(self, access_token: str, teacher_id: UUID) -> None:
        await self.auth_service.get_admin_user(access_token)
        await self.teacher_service.delete(teacher_id) 