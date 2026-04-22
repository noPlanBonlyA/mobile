from typing import Self, Optional, List
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lessons import GetLessonWithMaterialsServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol 
from school_site.apps.courses.schemas import LessonInfoTeacherReadSchema

class GetTeacherLessonsUseCaseProtocol(UseCaseProtocol[List[LessonInfoTeacherReadSchema]]):
    async def __call__(self: Self, access_token: str, is_graded_homework: Optional[bool] = None) -> List[LessonInfoTeacherReadSchema]:
        ...

class GetTeacherLessonsUseCase(GetTeacherLessonsUseCaseProtocol):
    def __init__(
        self,
        lesson_service: GetLessonWithMaterialsServiceProtocol,
        auth_service: AuthAdminServiceProtocol,
        teacher_service: TeacherServiceProtocol
    ):
        self.lesson_service = lesson_service
        self.auth_service = auth_service
        self.teacher_service = teacher_service

    async def __call__(self: Self, access_token: str, is_graded_homework: Optional[bool] = None) -> List[LessonInfoTeacherReadSchema]:
        user_data = await self.auth_service.get_teacher_user(access_token)
        teacher = await self.teacher_service.get_by_user_id(user_data.user_id)
        return await self.lesson_service.get_all_teacher_lessons(teacher.id, is_graded_homework)