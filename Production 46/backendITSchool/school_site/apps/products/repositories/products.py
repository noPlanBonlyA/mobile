import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from collections.abc import Iterable
from uuid import UUID
from typing import Self, Any
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.schemas import PaginationSchema
from school_site.apps.products.models import Product
from school_site.apps.products.schemas import (
    ProductCreateDBSchema, ProductReadDBSchema, ProductUpdateDBSchema, ProductWithPhotoDBReadSchema,
    ProductDBPaginationResultSchema
)
from sqlalchemy.ext.asyncio import AsyncSession

from school_site.core.utils.exceptions import ModelNotFoundException


class ProductRepositoryProtocol(BaseRepositoryImpl[
    Product,
    ProductReadDBSchema,
    ProductCreateDBSchema,
    ProductUpdateDBSchema
]):
    async def get_with_photo(self: Self, id: UUID) -> ProductWithPhotoDBReadSchema:
        ...

    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        user: Any,
        policies: list[str],
    ) -> ProductDBPaginationResultSchema:
        ...

    async def paginate_available(
        self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        max_price: float,
        user: Any,
        policies: list[str],
    ) -> ProductDBPaginationResultSchema:
        ...

    async def paginate_not_available(
        self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        min_price: float,
        user: Any,
        policies: list[str],
    ) -> ProductDBPaginationResultSchema:
        ...

class ProductRepository(ProductRepositoryProtocol):
    async def get_with_photo(self: Self, id: UUID) -> ProductWithPhotoDBReadSchema:
        async with self.session as s, s.begin():
            statement = (
                sa.select(self.model_type)
                .options(sa.orm.selectinload(self.model_type.photo)) 
                .where(self.model_type.id == id)
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, id)
            return ProductWithPhotoDBReadSchema.model_validate(model, from_attributes=True)


    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        user: Any,
        policies: list[str],
    ) -> ProductDBPaginationResultSchema:
        if len(policies) == 0:
            return ProductDBPaginationResultSchema(objects=[], count=0)
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
            objects = [ProductWithPhotoDBReadSchema.model_validate(model, from_attributes=True) for model in models]
            count_statement = statement.with_only_columns(func.count(self.model_type.id))
            count = (await s.execute(count_statement)).scalar_one()
            return ProductDBPaginationResultSchema(count=count, objects=objects)
        
    async def paginate_available(
        self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        max_price: float,
        user: Any,
        policies: list[str],
    ) -> ProductDBPaginationResultSchema:
        return await self._paginate_with_price_filter(
            search=search,
            search_by=search_by,
            sorting=sorting,
            pagination=pagination,
            price_condition=self.model_type.price <= max_price,
            user=user,
            policies=policies
        )

    async def paginate_not_available(
        self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        min_price: float,
        user: Any,
        policies: list[str],
    ) -> ProductDBPaginationResultSchema:
        return await self._paginate_with_price_filter(
            search=search,
            search_by=search_by,
            sorting=sorting,
            pagination=pagination,
            price_condition=self.model_type.price > min_price,
            user=user,
            policies=policies
        )

    async def _paginate_with_price_filter(
        self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        price_condition: sa.ColumnElement[bool],
        user: Any,
        policies: list[str],
    ) -> ProductDBPaginationResultSchema:
        if not policies:
            return ProductDBPaginationResultSchema(objects=[], count=0)
        
        async with self.session as s:
            statement = sa.select(self.model_type).options(
                sa.orm.selectinload(self.model_type.photo)
            )
            
            if search:
                search_conditions = [
                    getattr(self.model_type, field).ilike(f"%{search}%")
                    for field in search_by
                ]
                statement = statement.where(sa.or_(*search_conditions))
            
            statement = statement.where(price_condition)
            
            order_by_expr = self.get_order_by_expr(sorting)
            statement = statement.order_by(*order_by_expr)
            
            statement = statement.limit(pagination.limit).offset(pagination.offset)
            
            models = (await s.execute(statement)).scalars().all()
            count = await self._get_filtered_count(s, statement)
            return ProductDBPaginationResultSchema(
                count=count,
                objects=[ProductWithPhotoDBReadSchema.model_validate(m, from_attributes=True) for m in models]
            )
    
    async def _get_filtered_count(
    self, 
    session: AsyncSession, 
    statement: sa.Select
) -> int:
        count_stmt = sa.select(sa.func.count()).select_from(
            statement.order_by(None).limit(None).offset(None).subquery()
        )
        result = await session.execute(count_stmt)
        return result.scalar() or 0