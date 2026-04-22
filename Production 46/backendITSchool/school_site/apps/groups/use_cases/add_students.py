from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..services.group_students import GroupStudentServiceProtocol
from ..schemas import GroupAddStudentsSchema, GroupReadStudentsSchema


class AddStudentsUseCaseProtocol(UseCaseProtocol[GroupReadStudentsSchema]):
    async def __call__(self, access_token: str, group_id: UUID, students: GroupAddStudentsSchema):
        ...


class AddStudentsUseCase(AddStudentsUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminServiceProtocol, student_service: GroupStudentServiceProtocol):
        self.auth_service = auth_service
        self.student_service = student_service

    async def __call__(self, access_token: str, group_id: UUID, students: GroupAddStudentsSchema):
        await self.auth_service.get_admin_user(access_token)
        return await self.student_service.add_students(group_id, students) 