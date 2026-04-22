from typing import Self
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_html_files import LessonHTMLServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonHTMLCreateSchema, LessonHTMLReadSchema

class CreateLessonHTMLFileUseCaseProtocol(UseCaseProtocol[LessonHTMLReadSchema]):
    async def __call__(self: Self, lesson: LessonHTMLCreateSchema, access_token: str) -> LessonHTMLReadSchema:
        ...

class CreateLessonHTMLFileUseCase(CreateLessonHTMLFileUseCaseProtocol):
    def __init__(self, lesson_service: LessonHTMLServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.lesson_service = lesson_service
        self.auth_service = auth_service
    
    async def __call__(self: Self, lesson: LessonHTMLCreateSchema, access_token: str) -> LessonHTMLReadSchema:
        await self.auth_service.get_admin_user(access_token)

        return await self.lesson_service.create(lesson)