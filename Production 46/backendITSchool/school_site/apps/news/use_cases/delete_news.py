from typing import Self
from uuid import UUID
from school_site.apps.news.services.news import NewsServiceProtocol
from school_site.core.use_cases import UseCaseProtocol


class DeleteNewsUseCaseProtocol(UseCaseProtocol[bool]):
    async def __call__(self, news_id: UUID) -> bool:
        ...

class DeleteNewsUseCase(DeleteNewsUseCaseProtocol):
    def __init__(self: Self, news_service: NewsServiceProtocol):
        self.news_service = news_service

    async def __call__(self: Self, news_id: UUID) -> bool:
        return await self.news_service.delete_news(news_id)