from typing import List
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_group_student import CombinedLessonGroupStudentServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonGroupCreateSchema, LessonGroupReadSchema


class BulkCreateLessonGroupStudentUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, lesson_group: List[LessonGroupCreateSchema], access_token: str
    ) ->  List[LessonGroupReadSchema]:
        ...


class BulkCreateLessonGroupStudentUseCase(BulkCreateLessonGroupStudentUseCaseProtocol):
    def __init__(
        self,
        group_student_service: CombinedLessonGroupStudentServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.group_student_service = group_student_service
        self.auth_service = auth_service

    async def __call__(
        self, lesson_group: List[LessonGroupCreateSchema], access_token: str
    ) ->  List[LessonGroupReadSchema]:
        await self.auth_service.get_admin_user(access_token)
        return await self.group_student_service.bulk_create_lesson_groups_with_students(lesson_group)