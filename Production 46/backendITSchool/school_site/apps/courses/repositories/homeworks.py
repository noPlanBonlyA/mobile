from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import Homework
from ..schemas import HomeworkCreateSchema, HomeworkUpdateDBSchema, HomeworkReadDBSchema


class HomeworkRepositoryProtocol(BaseRepositoryImpl[
    Homework,
    HomeworkReadDBSchema,
    HomeworkCreateSchema,
    HomeworkUpdateDBSchema
]):
    pass

class HomeworkRepository(HomeworkRepositoryProtocol):
    pass