from typing import Self
from uuid import UUID
from school_site.apps.news.schemas import NewsWithPhotoReadSchema
from school_site.apps.news.services.news import NewsServiceProtocol
from school_site.core.use_cases import UseCaseProtocol


class GetNewsUseCaseProtocol(UseCaseProtocol[NewsWithPhotoReadSchema]):
    async def __call__(self, news_id: UUID) -> NewsWithPhotoReadSchema:
        ...

class GetNewsUseCase(GetNewsUseCaseProtocol):
    def __init__(self: Self, news_service: NewsServiceProtocol):
        self.news_service = news_service

    async def __call__(self: Self, news_id: UUID) -> NewsWithPhotoReadSchema:
        return await self.news_service.get_news_by_id(news_id)