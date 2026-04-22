from uuid import UUID
from typing import Self, Optional, List
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_student import LessonStudentServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonStudentReadWithStudentSchema

class GetAllLessonStudentsByLessonGroupUseCaseProtocol(UseCaseProtocol[List[LessonStudentReadWithStudentSchema]]):
    async def __call__(self: Self, lesson_group_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonStudentReadWithStudentSchema]:
        ...

class GetAllLessonStudentsByLessonGroupUseCase(GetAllLessonStudentsByLessonGroupUseCaseProtocol):
    def __init__(
        self,
        lesson_student_service: LessonStudentServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.lesson_student_service = lesson_student_service
        self.auth_service = auth_service

    async def __call__(self: Self, lesson_group_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonStudentReadWithStudentSchema]:
        return await self.lesson_student_service.get_all_by_lesson_group_id(lesson_group_id, is_graded_homework)