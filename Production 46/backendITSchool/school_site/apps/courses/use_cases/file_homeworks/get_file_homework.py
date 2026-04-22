from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.homeworks_files import FileHomeworkServiceProtocol
from school_site.apps.courses.schemas import FileHomeworkReadSchema


class GetHomeworkUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, homework_id: UUID
    ) -> FileHomeworkReadSchema:
        ...


class GetHomeworkUseCase(GetHomeworkUseCaseProtocol):
    def __init__(
        self,
        homework_service: FileHomeworkServiceProtocol,
    ):
        self.homework_service = homework_service

    async def __call__(
        self, homework_id: UUID
        ) -> FileHomeworkReadSchema:
        return await self.homework_service.get(homework_id)