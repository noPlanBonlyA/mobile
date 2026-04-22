from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import Comment
from ..schemas import CommentCreateDBSchema, CommentUpdateDBSchema, CommentReadSchema


class CommentRepositoryProtocol(BaseRepositoryImpl[
    Comment,
    CommentReadSchema,
    CommentCreateDBSchema,
    CommentUpdateDBSchema
]):
    pass

class CommentRepository(CommentRepositoryProtocol):
    pass