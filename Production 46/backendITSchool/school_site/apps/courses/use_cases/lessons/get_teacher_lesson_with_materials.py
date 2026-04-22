from uuid import UUID
from typing import Union
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lessons import GetLessonWithMaterialsServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol
from school_site.apps.courses.schemas import LessonTeacherMaterialDetailReadSchema, LessonSimpleReadSchema

class GetTeacherMaterialUseCaseProtocol(UseCaseProtocol[Union[LessonTeacherMaterialDetailReadSchema, LessonSimpleReadSchema]]):
    async def __call__(self, lesson_id: UUID, student_id: UUID, access_token: str) -> Union[LessonTeacherMaterialDetailReadSchema, LessonSimpleReadSchema]:
        ...

class GetTeacherMaterialUseCase(GetTeacherMaterialUseCaseProtocol):
    def __init__(self, lesson_service: GetLessonWithMaterialsServiceProtocol,
                 auth_service: AuthAdminServiceProtocol,
                 teacher_service: TeacherServiceProtocol):
        self.teacher_service = teacher_service
        self.lesson_service = lesson_service
        self.auth_service = auth_service
    
    async def __call__(self, lesson_id: UUID, student_id: UUID, access_token: str) -> Union[LessonTeacherMaterialDetailReadSchema, LessonSimpleReadSchema]:
        teacher_data = await self.auth_service.get_teacher_user(access_token)
        db_teacher = await self.teacher_service.get_by_user_id(teacher_data.user_id)
        return await self.lesson_service.get_lesson_for_teacher(lesson_id, student_id, db_teacher.id) 