from uuid import UUID
from typing import Self
from fastapi import UploadFile
from school_site.core.use_cases import UseCaseProtocol
from school_site.core.enums import UserRole
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.apps.courses.services.lessons import LessonServiceProtocol
from school_site.apps.courses.services.lesson_html_files import LessonHTMLServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonHTMLCreateSchema, LessonWithHomeworkReadSchema


class AddHomeworkToLessonUseCaseProtocol(UseCaseProtocol[LessonWithHomeworkReadSchema]):
    async def __call__(self: Self, lesson_id: UUID, homework_material_name: str, homework_material: UploadFile, access_token: str) -> LessonWithHomeworkReadSchema:
        ...

class AddHomeworkToLessonUseCase(AddHomeworkToLessonUseCaseProtocol):
    def __init__(self: Self, lesson_service: LessonServiceProtocol, material_service: LessonHTMLServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.lesson_service = lesson_service
        self.material_service = material_service
        self.auth_service = auth_service

    async def __call__(self: Self, lesson_id: UUID, homework_material_name: str, homework_material: UploadFile, access_token: str) -> LessonWithHomeworkReadSchema: 
        user_data = await self.auth_service.decode_access_token(access_token)
        if user_data.role not in [UserRole.TEACHER, UserRole.ADMIN, UserRole.SUPERADMIN]:
            raise PermissionDeniedError()

        homework_material = LessonHTMLCreateSchema(
            name=homework_material_name,
            file=homework_material
        )
        created_material = await self.material_service.create(homework_material)

        created_lesson = await self.lesson_service.add_additional_homework_to_lesson(lesson_id, created_material.id)

        return LessonWithHomeworkReadSchema(
            **created_lesson.model_dump(),
            homework=created_material
        )