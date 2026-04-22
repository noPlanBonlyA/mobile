from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.homeworks import HomeworkServiceProtocol
from school_site.apps.courses.schemas import HomeworkReadSchema


class GetHomeworkUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, lesson_id: UUID
    ) -> HomeworkReadSchema:
        ...


class GetHomeworkUseCase(GetHomeworkUseCaseProtocol):
    def __init__(
        self,
        homework_service: HomeworkServiceProtocol,
    ):
        self.homework_service = homework_service

    async def __call__(
        self, lesson_id: UUID
    ) -> HomeworkReadSchema:
        return await self.homework_service.get(lesson_id)