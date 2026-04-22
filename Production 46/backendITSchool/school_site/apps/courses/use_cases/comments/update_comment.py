from uuid import UUID
from school_site.apps.teachers.services.teachers import TeacherServiceProtocol
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.comments import CommentServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import CommentReadSchema, CommentUpdateSchema

class UpdateCommentUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, comment_id: UUID, comment: CommentUpdateSchema, access_token: str
    ) -> CommentReadSchema:
        ...


class UpdateCommentUseCase(UpdateCommentUseCaseProtocol):
    def __init__(
        self,
        comment_service: CommentServiceProtocol,
        teacher_service: TeacherServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.comment_service = comment_service
        self.teacher_service = teacher_service
        self.auth_service = auth_service

    async def __call__(
        self, comment_id: UUID, comment: CommentUpdateSchema, access_token: str
    ) -> CommentReadSchema:
        await self.auth_service.get_teacher_user(access_token)
        teacher_user = await self.auth_service.get_teacher_user(access_token)
        teacher = await self.teacher_service.get_by_user_id(teacher_user.user_id)
        return await self.comment_service.update(comment_id, teacher.id, comment)