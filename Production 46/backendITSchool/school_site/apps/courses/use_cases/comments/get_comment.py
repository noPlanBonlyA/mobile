from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.comments import CommentServiceProtocol
from school_site.apps.courses.schemas import CommentReadSchema

class GetCommentUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, comment_id: UUID
    ) -> CommentReadSchema:
        ...


class GetCommentUseCase(GetCommentUseCaseProtocol):
    def __init__(
        self,
        comment_service: CommentServiceProtocol
    ):
        self.comment_service = comment_service

    async def __call__(
        self, comment_id: UUID
    ) -> CommentReadSchema:
        return await self.comment_service.get(comment_id)