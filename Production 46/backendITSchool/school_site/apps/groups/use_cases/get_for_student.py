from school_site.core.use_cases import UseCaseProtocol
from ..services.group_students import GroupStudentServiceProtocol
from ..services.auth import AuthAdminServiceProtocol
from school_site.apps.students.services.students import StudentServiceProtocol
from ..schemas import GroupsForStudentReadSchema

class GetGroupForStudentUseCaseProtocol(UseCaseProtocol[list[GroupsForStudentReadSchema]]):
    async def __call__(self, access_token: str) -> list[GroupsForStudentReadSchema]:
        ...

class GetGroupForStudentUseCase(GetGroupForStudentUseCaseProtocol):
    def __init__(self, group_service: GroupStudentServiceProtocol,
                 student_service: StudentServiceProtocol,
                 auth_service: AuthAdminServiceProtocol):
        self.auth_service = auth_service
        self.group_service = group_service
        self.student_service = student_service
    
    async def __call__(self, access_token: str) -> list[GroupsForStudentReadSchema]:
        user_data = await self.auth_service.get_student_user(access_token)
        student = await self.student_service.get_by_user_id(user_data.user_id)
        return await self.group_service.get_groups_by_student_id(student.id) 