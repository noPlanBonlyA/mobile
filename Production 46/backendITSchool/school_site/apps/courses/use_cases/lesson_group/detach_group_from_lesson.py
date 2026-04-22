from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_group import DeleteLessonGroupServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol


class DeleteLessonGroupByLessonAndGroupUseCaseProtocol(UseCaseProtocol[bool]):
    async def __call__(self, lesson_id: UUID, group_id: UUID, access_token: str) -> bool:

        ...


class DeleteLessonGroupByLessonAndGroupUseCase(DeleteLessonGroupByLessonAndGroupUseCaseProtocol):
    def __init__(
        self,
        lesson_group_service: DeleteLessonGroupServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.lesson_group_service = lesson_group_service
        self.auth_service = auth_service

    async def __call__(self, lesson_id: UUID, group_id: UUID, access_token: str) -> bool:
        await self.auth_service.get_admin_user(access_token)
        return await self.lesson_group_service.detach_group_from_lesson(lesson_id, group_id)
