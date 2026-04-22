from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.homeworks import HomeworkServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol


class DeleteHomeworkUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, homework_id: UUID, access_token: str
    ) -> None:
        ...


class DeleteHomeworkUseCase(DeleteHomeworkUseCaseProtocol):
    def __init__(
        self,
        homework_service: HomeworkServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.homework_service = homework_service
        self.auth_service = auth_service

    async def __call__(
        self, homework_id: UUID, access_token: str
    ) -> None:
        await self.auth_service.get_student_user(access_token)
        return await self.homework_service.delete(homework_id)