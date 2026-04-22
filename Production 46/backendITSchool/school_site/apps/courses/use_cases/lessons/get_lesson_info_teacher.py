from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lessons import GetLessonWithMaterialsServiceProtocol
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonInfoTeacherReadSchema

class GetTeacherLessonInfoUseCaseProtocol(UseCaseProtocol[LessonInfoTeacherReadSchema]):
    async def __call__(self, lesson_id: UUID, access_token: str) -> LessonInfoTeacherReadSchema:
        ...

class GetTeacherLessonInfoUseCase(GetTeacherLessonInfoUseCaseProtocol):
    def __init__(self, lesson_service: GetLessonWithMaterialsServiceProtocol,
                 auth_service: AuthAdminServiceProtocol,
                 teacher_service: TeacherServiceProtocol):
        self.lesson_service = lesson_service
        self.auth_service = auth_service
        self.teacher_service = teacher_service
    
    async def __call__(self, lesson_id: UUID, access_token: str) -> LessonInfoTeacherReadSchema:
        teacher_user = await self.auth_service.get_teacher_user(access_token)
        db_teacher = await self.teacher_service.get_by_user_id(teacher_user.user_id)
        return await self.lesson_service.get_lesson_info_for_teacher(lesson_id, db_teacher.id) 