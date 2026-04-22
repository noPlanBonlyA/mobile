from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.products.models import Photo
from school_site.apps.products.schemas import (
    PhotoCreateDBSchema, PhotoUpdateDBSchema, PhotoReadDBSchema
)

class PhotoRepositoryProtocol(BaseRepositoryImpl[
    Photo,
    PhotoReadDBSchema,
    PhotoCreateDBSchema,
    PhotoUpdateDBSchema
]):
    pass

class PhotoRepository(PhotoRepositoryProtocol):
    pass