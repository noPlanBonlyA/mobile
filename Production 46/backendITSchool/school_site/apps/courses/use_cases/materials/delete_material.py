from typing import Self
from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_html_files import LessonHTMLServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol

class DeleteLessonHTMLFileUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self: Self, file_id: UUID, access_token: str) -> None:
        ...

class DeleteLessonHTMLFileUseCase(DeleteLessonHTMLFileUseCaseProtocol):
    def __init__(self, lesson_service: LessonHTMLServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.lesson_service = lesson_service
        self.auth_service = auth_service
    
    async def __call__(self: Self, file_id: UUID, access_token: str) -> None:
        await self.auth_service.get_admin_user(access_token)
        return await self.lesson_service.delete(file_id)