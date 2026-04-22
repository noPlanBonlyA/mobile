from ..models import PhotoUser
from ..schemas import PhotoUserReadDBSchema, PhotoUserCreateDBSchema, PhotoUserUpdateDBSchema
from school_site.core.repositories.base_repository import BaseRepositoryImpl


class PhotoUserRepositoryProtocol(BaseRepositoryImpl[
    PhotoUser,
    PhotoUserReadDBSchema,
    PhotoUserCreateDBSchema,
    PhotoUserUpdateDBSchema
]):
    pass

class PhotoUserRepository(PhotoUserRepositoryProtocol):
    pass 