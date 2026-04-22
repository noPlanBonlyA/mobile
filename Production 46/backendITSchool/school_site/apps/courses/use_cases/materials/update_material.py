from typing import Self
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_html_files import LessonHTMLServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonHTMLTextUpdateSchema, LessonHTMLReadSchema

class UpdateLessonHTMLFileUseCaseProtocol(UseCaseProtocol[LessonHTMLReadSchema]):
    async def __call__(self: Self, file_id: UUID, lesson: LessonHTMLTextUpdateSchema, access_token: str) -> LessonHTMLReadSchema:
        ...

class UpdateLessonHTMLFileUseCase(UpdateLessonHTMLFileUseCaseProtocol):
    def __init__(self, lesson_service: LessonHTMLServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.lesson_service = lesson_service
        self.auth_service = auth_service
    
    async def __call__(self: Self, file_id: UUID, lesson: LessonHTMLTextUpdateSchema, access_token: str) -> LessonHTMLReadSchema:
        await self.auth_service.get_admin_user(access_token)
        
        return await self.lesson_service.update(file_id, lesson)