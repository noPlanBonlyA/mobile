import logging
from typing import Protocol
from uuid import UUID
from ..repositories.comments import CommentRepositoryProtocol
from ..schemas import (
    CommentCreateSchema,
    CommentCreateDBSchema,
    CommentUpdateSchema,
    CommentUpdateDBSchema,
    CommentReadSchema
)

logger = logging.getLogger(__name__)

class CommentServiceProtocol(Protocol):
    async def create(self, teacher_id: UUID, comment: CommentCreateSchema) -> CommentReadSchema:
        ...
    
    async def get(self, comment_id: UUID) -> CommentReadSchema:
        ...
    
    async def update(self, comment_id: UUID, teacher_id: UUID, comment: CommentUpdateSchema) -> CommentReadSchema:
        ...
    
    async def delete(self, comment_id: UUID) -> None:
        ...

class CommentService(CommentServiceProtocol):
    def __init__(self, comment_repository: CommentRepositoryProtocol):
        self.comment_repository = comment_repository
    
    async def create(self, teacher_id: UUID, comment: CommentCreateSchema) -> CommentReadSchema:
        logger.info("Creating Comment")
        db_comment = CommentCreateDBSchema(
            teacher_id=teacher_id,
            lesson_student_id=comment.lesson_student_id,
            text=comment.text
        )
        return await self.comment_repository.create(db_comment)
    
    async def get(self, comment_id: UUID) -> CommentReadSchema:
        logger.info(f"Fetching Comment with ID: {comment_id}")
        return await self.comment_repository.get(comment_id)
    
    async def update(self, comment_id: UUID, teacher_id: UUID, comment: CommentUpdateSchema) -> CommentReadSchema:
        logger.info(f"Updating Comment with ID: {comment_id}")
        db_comment = CommentUpdateDBSchema(
            id=comment_id,
            text=comment.text,
            lesson_student_id=comment.lesson_student_id,
            teacher_id=teacher_id
        )
        return await self.comment_repository.update(db_comment)
    
    async def delete(self, comment_id: UUID) -> None:
        logger.info(f"Deleting Comment with ID: {comment_id}")
        await self.comment_repository.delete(comment_id)