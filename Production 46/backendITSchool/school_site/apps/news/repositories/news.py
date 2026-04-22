import sqlalchemy as sa
from sqlalchemy.sql.expression import func

from typing import Iterable, Any, Self
from ..models import News
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.core.schemas import PaginationSchema
from ..schemas import(
    NewsReadSchema, NewsCreateDBSchema, NewsUpdateDBSchema, PaginationResultSchema, NewsWithPhotoReadDBSchema,
    NewsWithPhotoPaginationResultDBSchema
)

class NewsRepositoryProtocol(BaseRepositoryImpl[News, NewsReadSchema, NewsCreateDBSchema, NewsUpdateDBSchema]):

    async def get_by_name(name: str) -> NewsReadSchema | None:
        ...

    async def get_all(limit: int, offset: int) -> PaginationResultSchema[NewsReadSchema]:
        ...

    async def get_with_photo(self, id: str) -> NewsWithPhotoReadDBSchema:
        ...

    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        user: Any,
        policies: list[str],
    ) -> NewsWithPhotoPaginationResultDBSchema:
        ...

class NewsRepository(NewsRepositoryProtocol):
    async def get_by_name(self, name: str) -> NewsReadSchema | None:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.name == name)
            news = (await session.execute(stmt)).scalar_one_or_none()
            if news is None:
                return None
            return self.read_schema_type.model_validate(news, from_attributes=True)
       
    async def get_all(self, limit: int = 10, offset: int = 0) -> PaginationResultSchema[NewsReadSchema]:
        async with self.session as session:
            count_query = sa.select(sa.func.count(self.model_type.id))
            total_count = (await session.execute(count_query)).scalar_one()
            
            data_query = (
                sa.select(self.model_type)
                .order_by(self.model_type.created_at.desc())  
                .limit(limit)
                .offset(offset)
            )
            models = (await session.execute(data_query)).scalars().all()
            
            pydantic_models = [self.read_schema_type.model_validate(model, from_attributes=True) for model in models]

            return PaginationResultSchema[NewsReadSchema](
                count=total_count,
                objects=pydantic_models
            )
    
    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        user: Any,
        policies: list[str],
    ) -> NewsWithPhotoPaginationResultDBSchema:
        if len(policies) == 0:
            return NewsWithPhotoPaginationResultDBSchema(objects=[], count=0)
        async with self.session as s:
            statement = sa.select(self.model_type).options(sa.orm.selectinload(self.model_type.photo)) 
            if search:
                search_where: sa.ColumnElement[Any] = sa.false()
                for sb in search_by:
                    search_where = sa.or_(search_where, getattr(self.model_type, sb).ilike(f'%{search}%'))
                statement = statement.where(search_where)
            order_by_expr = self.get_order_by_expr(sorting)
            models = (
                (await s.execute(statement.limit(pagination.limit).offset(pagination.offset).order_by(*order_by_expr)))
                .scalars()
                .all()
            )
            objects = [NewsWithPhotoReadDBSchema.model_validate(model, from_attributes=True) for model in models]
            count_statement = statement.with_only_columns(func.count(self.model_type.id))
            count = (await s.execute(count_statement)).scalar_one()
            return NewsWithPhotoPaginationResultDBSchema(count=count, objects=objects)
 

    async def get_with_photo(self, id: str) -> NewsWithPhotoReadDBSchema:
        async with self.session as session, session.begin():
            statement = (
                sa.select(self.model_type)
                .options(sa.orm.selectinload(self.model_type.photo)) 
                .where(self.model_type.id == id)
            )
            model = (await session.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, id)

            return NewsWithPhotoReadDBSchema.model_validate(model, from_attributes=True)