import logging
from typing import Protocol
from uuid import UUID
from ..repositories.homeworks import HomeworkRepositoryProtocol
from ..schemas import (
    HomeworkCreateSchema,
    HomeworkUpdateSchema,
    HomeworkReadDBSchema,
    HomeworkUpdateDBSchema
)

logger = logging.getLogger(__name__)


class HomeworkServiceProtocol(Protocol):
    async def create(self, homework: HomeworkCreateSchema) -> HomeworkReadDBSchema:
        ...

    async def get(self, homework_id: UUID) -> HomeworkReadDBSchema:
        ...

    async def update(self, homework_id: UUID, homework: HomeworkUpdateSchema) -> HomeworkReadDBSchema:
        ...

    async def delete(self, homework_id: UUID) -> None:
        ...


class HomeworkService(HomeworkServiceProtocol):
    def __init__(self, homework_repository: HomeworkRepositoryProtocol):
        self.homework_repository = homework_repository

    async def create(self, homework: HomeworkCreateSchema) -> HomeworkReadDBSchema:
        logger.info("Creating homework")
        return await self.homework_repository.create(homework)

    async def get(self, homework_id: UUID) -> HomeworkReadDBSchema:
        logger.info(f"Fetching homework with ID: {homework_id}")
        return await self.homework_repository.get(homework_id)

    async def update(self, homework_id: UUID, homework: HomeworkUpdateSchema) -> HomeworkReadDBSchema:
        logger.info(f"Updating homework with ID: {homework_id}")
        db_homework = HomeworkUpdateDBSchema(
            id=homework_id,
            file_id=homework.file_id
        )
        return await self.homework_repository.update(db_homework)

    async def delete(self, homework_id: UUID) -> None:
        logger.info(f"Deleting homework with ID: {homework_id}")
        await self.homework_repository.delete(homework_id)
