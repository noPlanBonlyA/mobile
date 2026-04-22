from ..models import PhotoNews
from ..schemas import PhotoReadDBSchema, PhotoCreateDBSchema, PhotoUpdateDBSchema
from school_site.core.repositories.base_repository import BaseRepositoryImpl


class PhotoRepositoryProtocol(BaseRepositoryImpl[
    PhotoNews,
    PhotoReadDBSchema,
    PhotoCreateDBSchema,
    PhotoUpdateDBSchema
]):
    pass

class PhotoRepository(PhotoRepositoryProtocol):
    pass