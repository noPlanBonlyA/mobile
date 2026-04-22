from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.homeworks_files import FileHomeworkServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import FileHomeworkReadSchema


class GetHomeworkUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, homework_id: UUID, access_token: str
    ) -> FileHomeworkReadSchema:
        ...


class GetHomeworkUseCase(GetHomeworkUseCaseProtocol):
    def __init__(
        self,
        homework_service: FileHomeworkServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.homework_service = homework_service
        self.auth_service = auth_service

    async def __call__(
        self, homework_id: UUID, access_token: str
        ) -> FileHomeworkReadSchema:
        await self.auth_service.get_student_user(access_token)
        return await self.homework_service.delete(homework_id)