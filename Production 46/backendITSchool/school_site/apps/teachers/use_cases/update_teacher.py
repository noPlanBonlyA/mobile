from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol 
from ..schemas import TeacherReadSchema, TeacherUpdateSchema
from ..services.auth import AuthAdminAndTeacherServiceProtocol
from ..services.teachers import TeacherServiceProtocol


class UpdateTeacherUseCaseProtocol(UseCaseProtocol[TeacherReadSchema]):
    async def __call__(self, access_token: str, teacher_id: UUID, teacher: TeacherUpdateSchema):
        ...


class UpdateTeacherUseCase(UpdateTeacherUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndTeacherServiceProtocol, teacher_service: TeacherServiceProtocol):
        self.auth_service = auth_service
        self.teacher_service = teacher_service

    async def __call__(self, access_token: str, teacher_id: UUID, teacher: TeacherUpdateSchema):
        await self.auth_service.get_admin_user(access_token)
        return await self.teacher_service.update(teacher_id, teacher) 