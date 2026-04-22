from fastapi import UploadFile
import asyncio 
import logging
from typing import Protocol, Optional, List
from uuid import UUID
from school_site.core.schemas import PaginationSchema
from ..schemas import (
    ProductCreateSchema,
    ProductUpdateSchema,
    ProductUpdateDBSchema,
    ProductReadSchema,
    PhotoReadDBSchema,
    ProductWithPhotoDBReadSchema,
    ProductPaginationResultSchema,
    ProductCreateDBSchema,
    PhotoCreateSchema,
    PhotoUpdateSchema,
    PhotoReadSchema
)
from ..repositories.products import ProductRepositoryProtocol
from .photos import PhotoServiceProtocol

logger = logging.getLogger(__name__)


class ProductServiceProtocol(Protocol):
    async def create(self, product: ProductCreateSchema, image: Optional[UploadFile]) -> ProductReadSchema:
        ...

    async def get(self, product_id: UUID) -> ProductReadSchema:
        ...

    async def update(self, product_id: UUID, product: ProductUpdateSchema, image: Optional[UploadFile]) -> ProductReadSchema:
        ...

    async def delete(self, product_id: UUID) -> bool:
        ...

    async def list(self, pagination: PaginationSchema) -> ProductPaginationResultSchema:
        ...

    async def paginate_available(self, pagination: PaginationSchema, max_price: int) -> ProductPaginationResultSchema:
        ...

    async def paginate_not_available(self, pagination: PaginationSchema, min_price: int) -> ProductPaginationResultSchema:
        ...


class ProductService(ProductServiceProtocol):
    def __init__(self, product_repository: ProductRepositoryProtocol,
                 photo_service: PhotoServiceProtocol):
        self.product_repository = product_repository
        self.photo_service = photo_service

    async def create(self, product: ProductCreateSchema, image: Optional[UploadFile]) -> ProductReadSchema:
        product_db = ProductCreateDBSchema(
            name=product.name,
            description=product.description,
            is_pinned=product.is_pinned,
            price=product.price
        )

        new_product = await self.product_repository.create(product_db)
        
        photo = None
        if product.photo and image:
            photo = await self.photo_service.create(
                PhotoCreateSchema(name=product.photo.name, product_id=new_product.id),
                image
            )

        return ProductReadSchema(
            id=new_product.id,
            name=new_product.name,
            description=new_product.description,
            price=new_product.price,
            is_pinned=new_product.is_pinned,
            photo=photo
        )
    

    async def get(self, product_id: UUID) -> ProductReadSchema:
        product = await self.product_repository.get_with_photo(product_id)
        photo_read = None
        if product.photo:
            image_url = await self.photo_service.get_photo_url(product.photo.path)
            photo_read = PhotoReadSchema(
                id=product.photo.id,
                name=product.photo.name,
                product_id=product.id,
                url=image_url,
                created_at=product.photo.created_at,
                updated_at=product.photo.updated_at
            )
        return ProductReadSchema(
            id=product.id,
            name=product.name,
            description=product.description,
            is_pinned=product.is_pinned,
            price=product.price,
            created_at=product.created_at,
            updated_at=product.updated_at,
            photo=photo_read
        )


    async def get_with_photo(self, product_id: UUID) -> ProductWithPhotoDBReadSchema:
        product = await self.product_repository.get_with_photo(product_id)
        return product


    async def update(self, product_id: UUID, product: ProductUpdateSchema, image: Optional[UploadFile]) -> ProductReadSchema:
        upd_product_db = ProductUpdateDBSchema(
            id=product_id,
            name=product.name,
            description=product.description,
            is_pinned=product.is_pinned,
            price=product.price
        )
        updated_product = await self.product_repository.update(upd_product_db)
        photo = None
        
        if product.photo and image:
            photo_id = product.photo.id or ((await self.get_with_photo(product_id)).photo.id)
            photo = await self.photo_service.update(
                photo_id,
                PhotoUpdateSchema(
                    product_id=product_id,
                    name=product.photo.name
                ),
                image
            )

        else:
            return await self.get(product_id)
        
        return ProductReadSchema(
            id=updated_product.id,
            name=updated_product.name,
            description=updated_product.description,
            is_pinned=updated_product.is_pinned,
            price=updated_product.price,
            created_at=updated_product.created_at,
            photo=photo,
        )

    async def delete(self, product_id: UUID) -> bool:
        product = await self.get_with_photo(product_id)
        if product.photo:
            await self.photo_service.delete(product.photo.id)
        return await self.product_repository.delete(product_id)
    
    async def list(self, pagination: PaginationSchema) -> ProductPaginationResultSchema:
        products_paginate = await self.product_repository.paginate(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            sorting=["-is_pinned", "created_at", "id"],
            policies=["can_view"]
        )
        converted_products = await self._convert_products_path_to_url(products_paginate.objects)

        converted_products_paginate = ProductPaginationResultSchema(objects=converted_products,
                                                           count=products_paginate.count)
        
        return converted_products_paginate
    
    async def paginate_available(self, pagination: PaginationSchema, max_price: int) -> ProductPaginationResultSchema:
        products_available = await self.product_repository.paginate_available(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            max_price=max_price,
            sorting=["-is_pinned", "created_at", "id"],
            policies=["can_view"]
        )
        
        converted_products_available = await self._convert_products_path_to_url(products_available.objects)

        converted_products_available_paginate = ProductPaginationResultSchema(objects=converted_products_available,
                                                                              count=products_available.count)
        
        return converted_products_available_paginate
    

    async def paginate_not_available(self, pagination: PaginationSchema, min_price: int) -> ProductPaginationResultSchema:
        products_not_available = await self.product_repository.paginate_not_available(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            min_price=min_price,
            sorting=["-is_pinned", "created_at", "id"],
            policies=["can_view"]
        )
        
        converted_products_not_available = await self._convert_products_path_to_url(products_not_available.objects)

        converted_products_not_available_paginate = ProductPaginationResultSchema(objects=converted_products_not_available,
                                                                              count=products_not_available.count)
        
        return converted_products_not_available_paginate

    async def _convert_products_path_to_url(
    self, 
    products: List[ProductWithPhotoDBReadSchema]
) -> List[ProductReadSchema]:
    
        async def process_photo(photo: PhotoReadDBSchema) -> PhotoReadSchema:
            if not photo:
                return None
            url = await self.photo_service.get_photo_url(photo.path)
            return PhotoReadSchema(
                id=photo.id,
                name=photo.name,
                product_id=photo.product_id,
                url=url,
                created_at=photo.created_at,
                updated_at=photo.updated_at
        )
    
        async def process_product(product: ProductWithPhotoDBReadSchema) -> ProductReadSchema:
            photo = product.photo
            conv_photo = await process_photo(photo) if photo else None
            
            return ProductReadSchema(
                id=product.id,
                name=product.name,
                description=product.description,
                is_pinned=product.is_pinned,
                price=product.price,
                photo=conv_photo,
                created_at=product.created_at,
                updated_at=product.updated_at
            )
    
        return await asyncio.gather(*[process_product(p) for p in products])