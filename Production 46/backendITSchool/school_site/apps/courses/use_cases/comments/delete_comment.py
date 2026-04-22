from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.comments import CommentServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol

class DeleteCommentUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, comment_id: UUID, access_token: str
    ) -> None:
        ...


class DeleteCommentUseCase(DeleteCommentUseCaseProtocol):
    def __init__(
        self,
        comment_service: CommentServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.comment_service = comment_service
        self.auth_service = auth_service

    async def __call__(
        self, comment_id: UUID, access_token: str
    ) -> None:
        await self.auth_service.get_teacher_user(access_token)
        
        return await self.comment_service.delete(comment_id)