from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.core.services.files import FileServiceProtocol
from school_site.core.depends import get_image_service
from school_site.apps.users.services.tokens import TokenServiceProtocol
from school_site.apps.users.depends import  get_token_service
from .repositories.products import ProductRepositoryProtocol, ProductRepository
from .services.products import ProductServiceProtocol, ProductService
from .repositories.photos import PhotoRepositoryProtocol, PhotoRepository
from .services.photos import PhotoServiceProtocol, PhotoService
from .use_cases.create_product import CreateProductUseCaseProtocol, CreateProductUseCase
from .use_cases.update_product import UpdateProductUseCaseProtocol, UpdateProductUseCase
from .use_cases.get_product import GetProductUseCaseProtocol, GetProductUseCase
from .use_cases.delete_product import DeleteProductUseCaseProtocol, DeleteProductUseCase
from .use_cases.list_product import GetListProductUseCaseProtocol, GetListProductUseCase
from .use_cases.create_photo import CreatePhotoUseCaseProtocol, CreatePhotoUseCase
from .use_cases.update_photo import UpdatePhotoUseCaseProtocol, UpdatePhotoUseCase
from .use_cases.delete_photo import DeletePhotoUseCaseProtocol, DeletePhotoUseCase
from .use_cases.get_photo import GetPhotoUseCaseProtocol, GetPhotoUseCase
from .use_cases.list_available_products import GetAvailableListProductUseCaseProtocol, GetAvailableProductUseCase
from .use_cases.list_not_available_products import GetNotAvailableListProductUseCaseProtocol, GetNotAvailableProductUseCase

def get_product_image_service() -> FileServiceProtocol:
    """Зависимость для работы с изображениями продуктов."""
    return get_image_service("product-images")


def __get_photo_repository(
        session: AsyncSession = Depends(get_async_session)
) -> PhotoRepositoryProtocol:
    return PhotoRepository(session)


def __get_product_repository(
        session: AsyncSession = Depends(get_async_session)
) -> ProductRepositoryProtocol:
    return ProductRepository(session)


def get_photo_service(
        photo_repository: PhotoRepositoryProtocol = Depends(__get_photo_repository),
        image_service: FileServiceProtocol = Depends(get_product_image_service)
) -> PhotoServiceProtocol:
    return PhotoService(photo_repository, image_service)


def get_product_service(
        product_repository: ProductRepositoryProtocol = Depends(__get_product_repository),
        photo_service: PhotoServiceProtocol = Depends(get_photo_service) 
) -> ProductServiceProtocol:
    return ProductService(product_repository, photo_service)
    


def get_product_create_use_case(auth_service: TokenServiceProtocol = Depends(get_token_service), 
                                product_service: ProductServiceProtocol = Depends(get_product_service)) -> \
        CreateProductUseCaseProtocol:
    return CreateProductUseCase(auth_service, product_service)


def get_product_update_use_case(auth_service: TokenServiceProtocol = Depends(get_token_service), 
                                product_service: ProductServiceProtocol = Depends(get_product_service)) -> \
        UpdateProductUseCaseProtocol:
    return UpdateProductUseCase(auth_service, product_service)


def get_product_get_use_case(product_service: ProductServiceProtocol = Depends(get_product_service)) -> \
    GetProductUseCaseProtocol:
    return GetProductUseCase(product_service)
    

def get_product_delete_use_case(auth_service: TokenServiceProtocol = Depends(get_token_service),
                                product_service: ProductServiceProtocol = Depends(get_product_service)) -> \
    DeleteProductUseCaseProtocol:
    return DeleteProductUseCase(auth_service, product_service)


def get_product_get_list_use_case(product_service: ProductServiceProtocol = Depends(get_product_service)) -> \
    GetListProductUseCaseProtocol:
    return GetListProductUseCase(product_service)


def get_available_products_use_case(product_service: ProductServiceProtocol = Depends(get_product_service)) -> \
    GetAvailableListProductUseCaseProtocol:
    return GetAvailableProductUseCase(product_service)


def get_not_available_products_use_case(product_service: ProductServiceProtocol = Depends(get_product_service)) -> \
    GetNotAvailableListProductUseCaseProtocol:
    return GetNotAvailableProductUseCase(product_service)


def get_photo_create_use_case(auth_service: TokenServiceProtocol = Depends(get_token_service),
                              photo_service: PhotoServiceProtocol = Depends(get_photo_service)) -> \
                            CreatePhotoUseCaseProtocol:
    return CreatePhotoUseCase(auth_service, photo_service)


def get_photo_update_use_case(auth_service: TokenServiceProtocol = Depends(get_token_service),
                              photo_service: PhotoServiceProtocol = Depends(get_photo_service)) -> \
                            UpdatePhotoUseCaseProtocol:
    return UpdatePhotoUseCase(auth_service, photo_service)


def get_photo_delete_use_case(auth_service: TokenServiceProtocol = Depends(get_token_service),
                              photo_service: PhotoServiceProtocol = Depends(get_photo_service)) -> \
                            DeletePhotoUseCaseProtocol:
    return DeletePhotoUseCase(auth_service, photo_service)


def get_photo_get_use_case(photo_service: PhotoServiceProtocol = Depends(get_photo_service)) -> \
                            GetPhotoUseCaseProtocol:
    return GetPhotoUseCase(photo_service)


