import logging
from typing import Protocol
from uuid import UUID
from ..repositories.comments_students import CommentStudentRepositoryProtocol
from ..schemas import (
    CommentStudentCreateSchema,
    CommentStudentCreateDBSchema,
    CommentStudentUpdateSchema,
    CommentStudentUpdateDBSchema,
    CommentStudentReadSchema
)

logger = logging.getLogger(__name__)

class CommentStudentServiceProtocol(Protocol):
    async def create(self, comment: CommentStudentCreateSchema) -> CommentStudentReadSchema:
        ...

    async def get(self, comment_id: UUID) -> CommentStudentReadSchema:
        ...

    async def update(self, comment_id: UUID, comment: CommentStudentUpdateSchema) -> CommentStudentReadSchema:
        ...
    
    async def delete(self, comment_id: UUID) -> None:
        ...

class CommentStudentService(CommentStudentServiceProtocol):
    def __init__(self, comment_repository: CommentStudentRepositoryProtocol):
        self.comment_repository = comment_repository

    async def create(self, comment: CommentStudentCreateSchema) -> CommentStudentReadSchema:
        logger.info("Creating Comment")
        db_comment = CommentStudentCreateDBSchema(
            **comment.model_dump()
        )
        return await self.comment_repository.create(db_comment)

    async def get(self, comment_id: UUID) -> CommentStudentReadSchema:
        logger.info(f"Fetching Comment with ID: {comment_id}")
        return await self.comment_repository.get(comment_id)

    async def update(self, comment_id: UUID, comment: CommentStudentUpdateSchema) -> CommentStudentReadSchema:
        logger.info(f"Updating Comment with ID: {comment_id}")
        db_comment = CommentStudentUpdateDBSchema(
            id=comment_id,
            **comment.model_dump()
        )
        return await self.comment_repository.update(db_comment)
    
    async def delete(self, comment_id: UUID) -> None:
        logger.info(f"Deleting Comment with ID: {comment_id}")
        await self.comment_repository.delete(comment_id)