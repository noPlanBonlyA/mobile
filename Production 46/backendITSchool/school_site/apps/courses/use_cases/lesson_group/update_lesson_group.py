from uuid import UUID
from school_site.core.enums import UserRole
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_group import LessonGroupServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonGroupUpdateSchema, LessonGroupReadSchema
from school_site.core.utils.exceptions import PermissionDeniedError


class UpdateLessonGroupUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, lesson_group_id: UUID, lesson_group: LessonGroupUpdateSchema, access_token: str) -> LessonGroupReadSchema:
        ...


class UpdateLessonGroupUseCase(UpdateLessonGroupUseCaseProtocol):
    def __init__(
        self,
        lesson_group_service: LessonGroupServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.lesson_group_service = lesson_group_service
        self.auth_service = auth_service

    async def __call__(self, lesson_group_id: UUID, lesson_group: LessonGroupUpdateSchema, access_token: str) -> LessonGroupReadSchema:
        user_data = await self.auth_service.decode_access_token(access_token)
        if user_data.role not in [UserRole.TEACHER, UserRole.ADMIN, UserRole.SUPERADMIN]:
            raise PermissionDeniedError()
        return await self.lesson_group_service.update(lesson_group_id, lesson_group)
