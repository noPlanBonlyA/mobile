from typing import Self, Optional
from uuid import UUID
from fastapi import UploadFile
import json
from school_site.apps.news.schemas import NewsWithPhotoReadSchema, NewsUpdateSchema
from school_site.apps.news.services.news import NewsServiceProtocol
from school_site.core.use_cases import UseCaseProtocol

class UpdateNewsUseCaseProtocol(UseCaseProtocol[NewsWithPhotoReadSchema]):
    async def __call__(self: Self, news_id: UUID, news_data: str, image: Optional[UploadFile]) -> NewsWithPhotoReadSchema:
        ...

class UpdateNewsUseCase(UpdateNewsUseCaseProtocol):
    def __init__(self: Self, news_service: NewsServiceProtocol):
        self.news_service = news_service

    async def __call__(self: Self, news_id: UUID, news_data: str, image: Optional[UploadFile]) -> NewsWithPhotoReadSchema:
        news_update = NewsUpdateSchema(**json.loads(news_data))
        return await self.news_service.update_news(news_id, news_update, image)