from typing import Self, Optional
from fastapi import UploadFile
import json
from school_site.apps.news.schemas import NewsCreateSchema, NewsWithPhotoReadSchema
from school_site.apps.news.services.news import NewsServiceProtocol
from school_site.core.use_cases import UseCaseProtocol


class CreateNewsUseCaseProtocol(UseCaseProtocol[NewsWithPhotoReadSchema]):
    async def __call__(self, news: NewsCreateSchema, image: Optional[UploadFile]) -> NewsWithPhotoReadSchema:
        ...

class CreateNewsUseCase(CreateNewsUseCaseProtocol):
    def __init__(self: Self, news_service: NewsServiceProtocol):
        self.news_service = news_service

    async def __call__(self: Self, news_data: str, image: Optional[UploadFile]) -> NewsWithPhotoReadSchema:
        news = NewsCreateSchema(**json.loads(news_data))
        return await self.news_service.create_news(news, image)