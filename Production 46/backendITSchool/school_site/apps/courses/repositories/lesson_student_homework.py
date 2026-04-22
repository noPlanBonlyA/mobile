from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import LessonStudentHomework
from ..schemas import LessonStudentHomeworkCreateSchema, LessonStudentHomeworkUpdateDBSchema, LessonStudentHomeworkReadSchema


class LessonStudentHomeworkRepositoryProtocol(BaseRepositoryImpl[
    LessonStudentHomework,
    LessonStudentHomeworkReadSchema,
    LessonStudentHomeworkCreateSchema,
    LessonStudentHomeworkUpdateDBSchema
]):
    pass

class LessonStudentHomeworkRepository(LessonStudentHomeworkRepositoryProtocol):
    pass