from school_site.apps.teachers.services.teachers import TeacherServiceProtocol
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.comments import CommentServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import CommentCreateSchema, CommentReadSchema

class CreateCommentUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, comment: CommentCreateSchema, access_token: str
    ) -> CommentReadSchema:
        ...


class CreateCommentUseCase(CreateCommentUseCaseProtocol):
    def __init__(
        self,
        comment_service: CommentServiceProtocol,
        teacher_service: TeacherServiceProtocol,
        auth_service: AuthAdminServiceProtocol,
    ):
        self.comment_service = comment_service
        self.teacher_service = teacher_service
        self.auth_service = auth_service

    async def __call__(
        self, comment: CommentCreateSchema, access_token: str
    ) -> CommentReadSchema:
        teacher_user = await self.auth_service.get_teacher_user(access_token)
        teacher = await self.teacher_service.get_by_user_id(teacher_user.user_id)
        return await self.comment_service.create(teacher.id, comment)