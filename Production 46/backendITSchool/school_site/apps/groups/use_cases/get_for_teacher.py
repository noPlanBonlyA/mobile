from school_site.core.use_cases import UseCaseProtocol
from ..services.group_teachers import GroupTeacherServiceProtocol
from ..services.auth import AuthAdminServiceProtocol
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol
from ..schemas import GroupReadTeacherSchema

class GetGroupForTeacherUseCaseProtocol(UseCaseProtocol[list[GroupReadTeacherSchema]]):
    async def __call__(self, access_token: str) -> list[GroupReadTeacherSchema]:
        ...

class GetGroupForTeacherUseCase(GetGroupForTeacherUseCaseProtocol):
    def __init__(self, group_service: GroupTeacherServiceProtocol,
                 teacher_service: TeacherServiceProtocol,
                 auth_service: AuthAdminServiceProtocol):
        self.auth_service = auth_service
        self.group_service = group_service
        self.teacher_service = teacher_service
    
    async def __call__(self, access_token: str) -> list[GroupReadTeacherSchema]:
        user_data = await self.auth_service.get_teacher_user(access_token)
        teacher = await self.teacher_service.get_by_user_id(user_data.user_id)
        return await self.group_service.get_by_teacher_id(teacher.id) 