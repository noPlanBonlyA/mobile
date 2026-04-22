from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import CommentStudent
from ..schemas import CommentStudentCreateDBSchema, CommentStudentUpdateDBSchema, CommentStudentReadSchema


class CommentStudentRepositoryProtocol(BaseRepositoryImpl[
    CommentStudent,
    CommentStudentReadSchema,
    CommentStudentCreateDBSchema,
    CommentStudentUpdateDBSchema
]):
    pass

class CommentStudentRepository(CommentStudentRepositoryProtocol):
    pass