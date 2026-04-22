from uuid import UUID
from typing import Union
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lessons import GetLessonWithMaterialsServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.students.services.students import StudentServiceProtocol

from school_site.apps.courses.schemas import LessonStudentMaterialDetailReadSchema, LessonSimpleReadSchema

class GetStudentMaterialUseCaseProtocol(UseCaseProtocol[Union[LessonStudentMaterialDetailReadSchema, LessonSimpleReadSchema]]):
    async def __call__(self, lesson_id: UUID,  access_token: str) -> Union[LessonStudentMaterialDetailReadSchema, LessonSimpleReadSchema]:
        ...

class GetStudentMaterialUseCase(GetStudentMaterialUseCaseProtocol):
    def __init__(self, lesson_service: GetLessonWithMaterialsServiceProtocol,
                 auth_service: AuthAdminServiceProtocol,
                 student_service: StudentServiceProtocol):
        self.student_service = student_service
        self.lesson_service = lesson_service
        self.auth_service = auth_service
    
    async def __call__(self, lesson_id: UUID, access_token: str) -> Union[LessonStudentMaterialDetailReadSchema, LessonSimpleReadSchema]:
        student = await self.auth_service.get_student_user(access_token)
        db_student = await self.student_service.get_by_user_id(student.user_id)
        return await self.lesson_service.get_lesson_for_student(lesson_id, db_student.id) 