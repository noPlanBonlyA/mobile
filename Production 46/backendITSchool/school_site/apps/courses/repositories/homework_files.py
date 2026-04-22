from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import FileHomework
from ..schemas import FileHomeworkCreateDBSchema, FileHomeworkUpdateDBSchema, FileHomeworkReadDBSchema


class FileHomeworkRepositoryProtocol(BaseRepositoryImpl[
    FileHomework,
    FileHomeworkReadDBSchema,
    FileHomeworkCreateDBSchema,
    FileHomeworkUpdateDBSchema
]):
    pass

class FileHomeworkRepository(FileHomeworkRepositoryProtocol):
    pass