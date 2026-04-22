from uuid import UUID
from typing import List
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_group import LessonGroupServiceProtocol
from school_site.apps.courses.schemas import LessonGroupReadWithLessonSchema


class GetByGroupIdLessonGroupUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, group_id: UUID) -> List[LessonGroupReadWithLessonSchema]:
        ...


class GetByGroupIdLessonGroupUseCase(GetByGroupIdLessonGroupUseCaseProtocol):
    def __init__(
        self,
        lesson_group_service: LessonGroupServiceProtocol,
    ):
        self.lesson_group_service = lesson_group_service

    async def __call__(self, group_id: UUID) -> List[LessonGroupReadWithLessonSchema]:
        return await self.lesson_group_service.get_by_group_id(group_id)
