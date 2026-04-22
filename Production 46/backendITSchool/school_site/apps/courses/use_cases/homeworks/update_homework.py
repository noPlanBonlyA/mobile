from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.homeworks import HomeworkServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import HomeworkUpdateSchema, HomeworkReadSchema


class UpdateHomeworkUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, lesson_id: UUID, homework: HomeworkUpdateSchema, access_token: str
    ) -> HomeworkReadSchema:
        ...


class UpdateHomeworkUseCase(UpdateHomeworkUseCaseProtocol):
    def __init__(
        self,
        homework_service: HomeworkServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.homework_service = homework_service
        self.auth_service = auth_service

    async def __call__(
        self, lesson_id: UUID, homework: HomeworkUpdateSchema, access_token: str
    ) -> HomeworkReadSchema:
        await self.auth_service.get_student_user(access_token)
        return await self.homework_service.update(lesson_id, homework)