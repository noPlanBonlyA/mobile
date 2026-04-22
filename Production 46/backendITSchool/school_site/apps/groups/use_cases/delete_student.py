from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..services.group_students import GroupStudentServiceProtocol


class DeleteStudentUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, access_token: str, group_id: UUID, student_id: UUID):
        ...


class DeleteStudentUseCase(DeleteStudentUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminServiceProtocol, student_service: GroupStudentServiceProtocol):
        self.auth_service = auth_service
        self.student_service = student_service

    async def __call__(self, access_token: str, group_id: UUID, student_id: UUID) -> None:
        await self.auth_service.get_admin_user(access_token)
        await self.student_service.delete_student(group_id, student_id) 