import asyncio
import logging 
from typing import Protocol, List
from fastapi import UploadFile
from typing import Optional
from ..repositories.news import NewsRepositoryProtocol
from ..schemas import (
    NewsCreateSchema,   
    NewsReadSchema, 
    NewsUpdateSchema,
    PaginationResultSchema,
    NewsCreateDBSchema,
    NewsUpdateDBSchema,
    NewsWithPhotoReadSchema,
    NewsWithPhotoReadDBSchema,
    NewsWithPhotoPaginationResultSchema,
    NewsWithPhotoPaginationResultDBSchema,
    PhotoReadDBSchema,
    PhotoCreateSchema,
    PhotoReadSchema,
    PhotoUpdateSchema
)

from uuid import UUID
from school_site.core.schemas import PaginationSchema
from typing_extensions import Self
from .photo_news import PhotoServiceProtocol

logger = logging.getLogger(__name__)


class NewsServiceProtocol(Protocol): 

    async def create_news(self: Self, news: NewsCreateSchema, image: Optional[UploadFile]) -> NewsWithPhotoReadSchema:
        ...

    async def get_news_by_id(self, news_id: UUID) -> NewsWithPhotoReadSchema: 
        ... 

    async def get_all_news(self, limit: int = 10, offset: int = 0) -> PaginationResultSchema[NewsReadSchema]: 
        ... 

    async def _get_news_by_name(self, name: str) -> NewsReadSchema | None:
        ...

    async def update_news(self, news_id: UUID, news_data: NewsUpdateSchema, image: Optional[UploadFile]) -> NewsWithPhotoReadSchema:
        ...

    async def delete_news(self, news_id: UUID) -> bool:
        ...

    async def list(self, pagination: PaginationSchema) -> NewsWithPhotoPaginationResultSchema:
        ...

        
class NewsService(NewsServiceProtocol):
    def __init__(self: Self, news_repository: NewsRepositoryProtocol,
                 photo_service: PhotoServiceProtocol):
        self.news_repository = news_repository
        self.photo_service = photo_service

    async def create_news(self: Self, news: NewsCreateSchema, image: Optional[UploadFile]) -> NewsWithPhotoReadSchema:
        logger.info(f"Creating news with name {news.name} and with a pinned state {news.is_pinned}")
        news_db = NewsCreateDBSchema(
            name=news.name,
            description=news.description,
            is_pinned=news.is_pinned,
        )
        new_news = await self.news_repository.create(news_db)
        photo = None
        if news.photo and image:
            photo = await self.photo_service.create(
                PhotoCreateSchema(name=news.photo.name, news_id=new_news.id),
                image
            )
        return NewsWithPhotoReadSchema(
            id=new_news.id,
            name=new_news.name,
            description=new_news.description,
            is_pinned=new_news.is_pinned,
            photo=photo,
            created_at=new_news.created_at,
            updated_at=new_news.updated_at
        )
    
    async def get_all_news(self: Self, limit: int = 10, offset: int = 0) -> PaginationResultSchema[NewsReadSchema]:
        logger.info(f"Getting all news with limit={limit}, offset={offset}")
        paginated_news = await self.news_repository.get_all(limit=limit, offset=offset)
        
        # Преобразуем SQLAlchemy модели в Pydantic модели
        news_schemas = [NewsReadSchema.model_validate(news, from_attributes=True) for news in paginated_news.objects]
    
        
        # Создаем PaginationResultSchema с помощью model_validate
        return PaginationResultSchema[NewsReadSchema].model_validate({
            "count": paginated_news.count,
            "objects": news_schemas
            })
    
    async def get_news_by_id(self: Self, news_id: UUID) -> NewsWithPhotoReadSchema:   
        logger.info(f"Fetching news with id {news_id}")
        news = await self.get_with_photo(news_id)
        photo_read = None
        if news.photo:
            image_url = await self.photo_service.get_photo_url(news.photo.path)
            photo_read = PhotoReadSchema(
                id=news.photo.id,
                name=news.photo.name,
                news_id=news.id,
                url=image_url,
                created_at=news.photo.created_at,
                updated_at=news.photo.updated_at
            )
        return NewsWithPhotoReadSchema(
            id=news.id,
            name=news.name,
            description=news.description,
            is_pinned=news.is_pinned,
            created_at=news.created_at,
            updated_at=news.updated_at,
            photo=photo_read
        )
    
    async def get_with_photo(self, news_id: UUID) -> NewsWithPhotoReadSchema:
        news = await self.news_repository.get_with_photo(news_id)
        return news
    
    async def _get_news_by_name(self, name: str) -> NewsReadSchema | None:
        news = await self.news_repository.get_by_name(name)
        return news
    
    async def update_news(self, news_id: UUID, news_data: NewsUpdateSchema, image: Optional[UploadFile]) -> NewsWithPhotoReadSchema:
        logger.info(f"Fetching news with id {news_id}")
        upd_news_db = NewsUpdateDBSchema(
            id=news_id,
            name=news_data.name,
            description=news_data.description,
            is_pinned=news_data.is_pinned,
        )
        
        updated_news = await self.news_repository.update(upd_news_db)
        photo = None

        if news_data.photo and image:
            photo_id = news_data.photo.id or ((await self.get_with_photo(news_id)).photo.id)
            photo = await self.photo_service.update(
                photo_id,
                PhotoUpdateSchema(
                    news_id=news_id,
                    name=news_data.photo.name
                ),
                image
            )
        else:
            return await self.get_news_by_id(news_id)

        return NewsWithPhotoReadSchema(
            id=updated_news.id,
            name=updated_news.name,
            description=updated_news.description,
            is_pinned=updated_news.is_pinned,
            created_at=updated_news.created_at,
            updated_at=updated_news.updated_at,
            photo=photo
        )

    
    async def delete_news(self, news_id: UUID) -> bool:
        logger.info(f"Fetching news with id {news_id}")
        news = await self.get_with_photo(news_id)
        if news.photo:
            await self.photo_service.delete(news.photo.id)
        return await self.news_repository.delete(news_id)    

    async def list(self, pagination: PaginationSchema) -> NewsWithPhotoPaginationResultSchema:
        news_paginate = await self.news_repository.paginate(
            search=None,
            search_by=None,
            user=None,
            pagination=pagination,
            sorting=["created_at", "id"],
            policies=["can_view"]
        )
        converted_news = await self._convert_courses_path_to_url(news_paginate.objects)

        converted_news_paginate = NewsWithPhotoPaginationResultSchema(objects=converted_news,
                                                           count=news_paginate.count)
        
        return converted_news_paginate
    
    async def _convert_courses_path_to_url(
    self, 
    courses: List[NewsWithPhotoPaginationResultDBSchema]
) -> List[NewsWithPhotoPaginationResultSchema]:
    
        async def process_photo(photo: PhotoReadDBSchema) -> PhotoReadSchema:
            if not photo:
                return None
            url = await self.photo_service.get_photo_url(photo.path)
            return PhotoReadSchema(
                id=photo.id,
                name=photo.name,
                news_id=photo.news_id,
                url=url,
                created_at=photo.created_at,
                updated_at=photo.updated_at
        )
    
        async def process_course(news: NewsWithPhotoReadDBSchema) -> NewsWithPhotoReadSchema:
            photo = news.photo
            conv_photo = await process_photo(photo) if photo else None
            
            return NewsWithPhotoReadSchema(
                id=news.id,
                name=news.name,
                description=news.description,
                is_pinned=news.is_pinned,
                photo=conv_photo,
                created_at=news.created_at,
                updated_at=news.updated_at
            )
    
        return await asyncio.gather(*[process_course(p) for p in courses])
  
   