from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_group_student import CombinedLessonGroupStudentServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonGroupCreateSchema, LessonGroupReadSchema


class CreateLessonGroupStudentUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, lesson_group: LessonGroupCreateSchema, access_token: str
    ) -> LessonGroupReadSchema:
        ...


class CreateLessonGroupStudentUseCase(CreateLessonGroupStudentUseCaseProtocol):
    def __init__(
        self,
        group_student_service: CombinedLessonGroupStudentServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.group_student_service = group_student_service
        self.auth_service = auth_service

    async def __call__(
        self, lesson_group: LessonGroupCreateSchema, access_token: str
    ) -> LessonGroupReadSchema:
        await self.auth_service.get_admin_user(access_token)
        return await self.group_student_service.create_lesson_group_with_students(lesson_group)