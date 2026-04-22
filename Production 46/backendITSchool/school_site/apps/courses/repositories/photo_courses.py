from ..models import PhotoCourse
from ..schemas import PhotoReadDBSchema, PhotoCreateDBSchema, PhotoUpdateDBSchema
from school_site.core.repositories.base_repository import BaseRepositoryImpl


class PhotoRepositoryProtocol(BaseRepositoryImpl[
    PhotoCourse,
    PhotoReadDBSchema,
    PhotoCreateDBSchema,
    PhotoUpdateDBSchema
]):
    pass

class PhotoRepository(PhotoRepositoryProtocol):
    pass