from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_group import DeleteLessonGroupServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol


class DeleteLessonGroupByLessonAndCourseUseCaseProtocol(UseCaseProtocol[bool]):
    async def __call__(self, group_id: UUID, course_id: UUID, access_token: str) -> bool:

        ...


class DeleteLessonGroupByLessonAndCourseUseCase(DeleteLessonGroupByLessonAndCourseUseCaseProtocol):
    def __init__(
        self,
        lesson_group_service: DeleteLessonGroupServiceProtocol,
        auth_service: AuthAdminServiceProtocol

    ):
        self.auth_service =auth_service
        self.lesson_group_service = lesson_group_service

    async def __call__(self, group_id: UUID, course_id: UUID, access_token: str) -> bool:
        await self.auth_service.get_admin_user(access_token)
        return await self.lesson_group_service.detach_group_from_course(group_id, course_id)
