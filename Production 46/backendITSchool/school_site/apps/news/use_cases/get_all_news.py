from typing import Self
from school_site.core.schemas import PaginationSchema

from school_site.apps.news.schemas import NewsReadSchema
from school_site.apps.news.services.news import NewsServiceProtocol
from school_site.core.use_cases import UseCaseProtocol
from school_site.core.schemas import PaginationResultSchema


class GetAllNewsUseCaseProtocol(UseCaseProtocol[PaginationResultSchema[NewsReadSchema]]):
    async def __call__(self: Self, limit: int = 10, offset: int = 0) -> PaginationResultSchema[NewsReadSchema]:
        ...

class GetAllNewsUseCase(GetAllNewsUseCaseProtocol):
    def __init__(self: Self, news_service: NewsServiceProtocol):
        self.news_service = news_service

    async def __call__(self: Self, limit: int = 10, offset: int = 0) -> PaginationResultSchema[NewsReadSchema]:
        pagination_parameters = PaginationSchema(
            limit=limit,
            offset=offset
        )
        return await self.news_service.list(pagination_parameters)