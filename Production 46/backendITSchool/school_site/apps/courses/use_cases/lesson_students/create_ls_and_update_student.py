from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_student import LessonStudentWithStudentService
from school_site.apps.courses.schemas import LessonStudentReadSchema, LessonStudentCreateSchema


class CreateLessonStudentsAndUpdateStudentsUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, lesson_student: LessonStudentCreateSchema) -> LessonStudentReadSchema:
        ...


class CreateLessonStudentsAndUpdateStudentsUseCase(CreateLessonStudentsAndUpdateStudentsUseCaseProtocol):
    def __init__(
        self,
        lesson_student_service: LessonStudentWithStudentService,
    ):
        self.lesson_student_service = lesson_student_service

    async def __call__(self, lesson_student: LessonStudentCreateSchema) -> LessonStudentReadSchema:
        return await self.lesson_student_service.create_ls_and_update_student(lesson_student)
