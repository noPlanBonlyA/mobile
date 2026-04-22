from uuid import UUID
from typing import Self
from school_site.core.use_cases import UseCaseProtocol
from school_site.core.enums import UserRole
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.apps.courses.services.lessons import LessonServiceProtocol
from school_site.apps.courses.services.lesson_html_files import LessonHTMLServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonHTMLTextCreateSchema, LessonWithHomeworkReadSchema


class AddHomeworkToLessonByTextUseCaseProtocol(UseCaseProtocol[LessonWithHomeworkReadSchema]):
    async def __call__(self: Self, lesson_id: UUID, homework_material: LessonHTMLTextCreateSchema, access_token: str) -> LessonWithHomeworkReadSchema:
        ...

class AddHomeworkToLessonByTextUseCase(AddHomeworkToLessonByTextUseCaseProtocol):
    def __init__(self: Self, lesson_service: LessonServiceProtocol, material_service: LessonHTMLServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.lesson_service = lesson_service
        self.material_service = material_service
        self.auth_service = auth_service

    async def __call__(self: Self, lesson_id: UUID, homework_material: LessonHTMLTextCreateSchema, access_token: str) -> LessonWithHomeworkReadSchema: 
        user_data = await self.auth_service.decode_access_token(access_token)
        if user_data.role not in [UserRole.TEACHER, UserRole.ADMIN, UserRole.SUPERADMIN]:
            raise PermissionDeniedError()

        
        created_material = await self.material_service.create_by_text(homework_material)

        created_lesson = await self.lesson_service.add_homework_to_lesson(lesson_id, created_material.id)

        return LessonWithHomeworkReadSchema(
            **created_lesson.model_dump(),
            homework=created_material
        )