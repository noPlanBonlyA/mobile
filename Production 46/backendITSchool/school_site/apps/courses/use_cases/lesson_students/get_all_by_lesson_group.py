from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_student import GetAllLessonStudentsByLessonGroupServiceProtocol
from school_site.apps.courses.schemas import LessonStudentDetailReadSchema


class GetAllLessonStudentsByLessonGroupUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, lesson_group_id: UUID) -> LessonStudentDetailReadSchema:
        ...


class GetAllLessonStudentsByLessonGroupUseCase(GetAllLessonStudentsByLessonGroupUseCaseProtocol):
    def __init__(
        self,
        lesson_group_service: GetAllLessonStudentsByLessonGroupServiceProtocol,
    ):
        self.lesson_group_service = lesson_group_service

    async def __call__(self, lesson_group_id: UUID) -> LessonStudentDetailReadSchema:
        return await self.lesson_group_service.get_all_lesson_students_by_lesson_group(lesson_group_id)
