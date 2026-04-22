import logging
from typing import Protocol, List, Self
from uuid import UUID
from ..repositories.lesson_group import LessonGroupRepositoryProtocol
from ..schemas import (
    LessonGroupCreateSchema,
    LessonGroupUpdateSchema,
    LessonGroupReadSchema,
    LessonGroupUpdateDBSchema,
    LessonGroupReadWithLessonSchema
)

logger = logging.getLogger(__name__)


class LessonGroupServiceProtocol(Protocol):
    async def create(self, lesson_group: LessonGroupCreateSchema) -> LessonGroupReadSchema:
        ...

    async def get(self, lesson_group_id: UUID) -> LessonGroupReadSchema:
        ...

    async def update(self, lesson_group_id: UUID, LessonGroup: LessonGroupUpdateSchema) -> LessonGroupReadSchema:
        ...

    async def delete(self, lesson_group_id: UUID) -> None:
        ...

    async def bulk_create(self, lesson_groups: list[LessonGroupCreateSchema]) -> list[LessonGroupReadSchema]:
        ...

    async def get_by_group_id(self, group_id: UUID) -> List[LessonGroupReadWithLessonSchema]:
        ...


class LessonGroupService(LessonGroupServiceProtocol):
    def __init__(self, lesson_group_repository: LessonGroupRepositoryProtocol):
        self.lesson_group_repository = lesson_group_repository

    async def create(self, lesson_group: LessonGroupCreateSchema) -> LessonGroupReadSchema:
        logger.info("Creating LessonGroup")
        return await self.lesson_group_repository.create(lesson_group)

    async def bulk_create(self, lesson_groups: list[LessonGroupCreateSchema]) -> list[LessonGroupReadSchema]:
        logger.info("Bulk creating LessonGroup")
        return await self.lesson_group_repository.bulk_create(lesson_groups)

    async def get(self, lesson_group_id: UUID) -> LessonGroupReadSchema:
        logger.info(f"Fetching LessonGroup with ID: {lesson_group_id}")
        return await self.lesson_group_repository.get(lesson_group_id)

    async def update(self, lesson_group_id: UUID, lesson_group: LessonGroupUpdateSchema) -> LessonGroupReadSchema:
        logger.info(f"Updating LessonGroup with ID: {lesson_group_id}")
        db_lesson_group = LessonGroupUpdateDBSchema(
            id=lesson_group_id,
            lesson_id=lesson_group.lesson_id,
            group_id=lesson_group.group_id,
            start_datetime=lesson_group.start_datetime,
            end_datetime=lesson_group.end_datetime,
            auditorium=lesson_group.auditorium,
            is_opened=lesson_group.is_opened
        )
        return await self.lesson_group_repository.update(db_lesson_group)

    async def delete(self, lesson_group_id: UUID) -> None:
        logger.info(f"Deleting LessonGroup with ID: {lesson_group_id}")
        await self.lesson_group_repository.delete(lesson_group_id)

    async def get_by_group_id(self, group_id: UUID) -> List[LessonGroupReadWithLessonSchema]:
        logger.info(f"Fetching LessonGroups for Group ID: {group_id}")
        return await self.lesson_group_repository.get_by_group_id(group_id)


class DeleteLessonGroupServiceProtocol(Protocol):
    async def detach_group_from_lesson(self: Self, lesson_id: UUID, group_id: UUID) -> bool:
        ...
    
    async def detach_group_from_course(self: Self, group_id: UUID, course_id: UUID) -> bool:
        ...

class DeleteLessonGroupService(DeleteLessonGroupServiceProtocol):
    def __init__(self: Self, repository: LessonGroupRepositoryProtocol):
        self.repository = repository

    async def detach_group_from_lesson(self: Self, lesson_id: UUID, group_id: UUID) -> bool:
        return await self.repository.detach_group_from_lesson(lesson_id, group_id)
    
    async def detach_group_from_course(self: Self, group_id: UUID, course_id: UUID) -> bool:
        return await self.repository.detach_group_from_course(group_id, course_id)