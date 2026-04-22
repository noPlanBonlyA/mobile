from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lessons import GetLessonWithMaterialsServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonInfoTeacherReadSchema

class GetTeacherLessonInfoByTeacherIdUseCaseProtocol(UseCaseProtocol[LessonInfoTeacherReadSchema]):
    async def __call__(self, lesson_id: UUID, teacher_id: UUID, access_token: str) -> LessonInfoTeacherReadSchema:
        ...

class GetTeacherLessonInfoByTeacherIdUseCase(GetTeacherLessonInfoByTeacherIdUseCaseProtocol):
    def __init__(self, lesson_service: GetLessonWithMaterialsServiceProtocol,
                 auth_service: AuthAdminServiceProtocol):
        self.lesson_service = lesson_service
        self.auth_service = auth_service
    
    async def __call__(self, lesson_id: UUID, teacher_id: UUID, access_token: str) -> LessonInfoTeacherReadSchema:
        await self.auth_service.get_admin_user(access_token)
        return await self.lesson_service.get_lesson_info_for_teacher(lesson_id, teacher_id) 