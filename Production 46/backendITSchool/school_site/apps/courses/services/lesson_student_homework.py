from typing import Protocol, Self
from uuid import UUID
import logging
from ..repositories.lesson_student_homework import LessonStudentHomeworkRepositoryProtocol
from ..schemas import LessonStudentHomeworkCreateSchema, LessonStudentHomeworkReadSchema, LessonStudentHomeworkUpdateSchema, \
    LessonStudentHomeworkUpdateDBSchema

class LessonStudentHomeworkServiceProtocol(Protocol):
    async def create(self: Self, homework_link: LessonStudentHomeworkCreateSchema) -> LessonStudentHomeworkReadSchema:
        ...
    
    async def get(self: Self, homework_id: UUID) -> LessonStudentHomeworkReadSchema:
        ...
    
    async def update(self: Self, lesson_student_id: UUID, homework_link: LessonStudentHomeworkUpdateSchema) -> LessonStudentHomeworkReadSchema:
        ...

    async def delete(self: Self, homework_id: UUID) -> None:
        ...

logger = logging.getLogger(__name__)

class LessonStudentHomeworkService(LessonStudentHomeworkServiceProtocol):
    def __init__(self, homework_link_repository: LessonStudentHomeworkRepositoryProtocol):
        self.homework_link_repository = homework_link_repository
    
    async def create(self, homework_link: LessonStudentHomeworkCreateSchema) -> LessonStudentHomeworkReadSchema:
        logger.info("Creating LessonStudentHomework link")
        return await self.homework_link_repository.create(homework_link)
    
    async def get(self, homework_id: UUID) -> LessonStudentHomeworkReadSchema:
        logger.info(f"Fetching LessonStudentHomework link: homework_id={homework_id}")
        return await self.homework_link_repository.get(homework_id)
    
    async def update(self: Self, homework_id: UUID, homework_link: LessonStudentHomeworkUpdateSchema) -> LessonStudentHomeworkReadSchema:
        logger.info(f"Updating LessonStudentHomework link: homework_id={homework_id}")
        homework = LessonStudentHomeworkUpdateDBSchema(
            id=homework_id,
            lesson_student_id=homework_link.lesson_student_id,
            homework_id=homework_link.homework_id
        )
        return await self.homework_link_repository.update(homework) 

    async def delete(self: Self, homework_id: UUID) -> None:
        logger.info(f"Deleting LessonStudentHomework link: homework_id={homework_id}")
        await self.homework_link_repository.delete(homework_id)