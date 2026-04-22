from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_student import GetDetailedLessonStudentByIdServiceProtocol
from school_site.apps.courses.schemas import LessonStudentDetailReadSchema


class GetDetailedLessonStudentUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, lesson_student_id: UUID) -> LessonStudentDetailReadSchema:
        ...


class GetDetailedLessonStudentUseCase(GetDetailedLessonStudentUseCaseProtocol):
    def __init__(
        self,
        lesson_student_service: GetDetailedLessonStudentByIdServiceProtocol,
    ):
        self.lesson_student_service = lesson_student_service

    async def __call__(self, lesson_student_id: UUID) -> LessonStudentDetailReadSchema:
        return await self.lesson_student_service.get_detailed_by_id(lesson_student_id)
