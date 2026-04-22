from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lessons import LessonServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol


class DeleteLessonUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, course_id: UUID, lesson_id: UUID, access_token: str) -> None:
        ...


class DeleteLessonUseCase(DeleteLessonUseCaseProtocol):
    def __init__(
        self,
        lesson_service: LessonServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.lesson_service = lesson_service
        self.auth_service = auth_service

    async def __call__(self, course_id: UUID, lesson_id: UUID, access_token: str) -> None:
        await self.auth_service.get_admin_user(access_token)
        await self.lesson_service.delete(course_id, lesson_id) 