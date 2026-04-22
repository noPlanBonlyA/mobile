from typing import Any, Iterable
from typing_extensions import Self
import sqlalchemy as sa
from sqlalchemy import func
from school_site.core.schemas import PaginationSchema
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.points_history.models import PointsHistory
from school_site.apps.points_history.schemas import (
    PointsHistoryCreateSchema,
    PointsHistoryUpdateSchema,
    PointsHistoryReadSchema,
    PointsHistoryPaginationSchema
)


class PointsHistoryRepositoryProtocol(BaseRepositoryImpl[PointsHistory, PointsHistoryReadSchema, PointsHistoryCreateSchema, PointsHistoryUpdateSchema]):
    pass

class PointsHistoryRepository(PointsHistoryRepositoryProtocol):
     async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema,
        user: Any,
        policies: list[str],
    ) -> PointsHistoryPaginationSchema:
        if len(policies) == 0:
            return PointsHistoryPaginationSchema(objects=[], count=0)
        async with self.session as s:
            statement = sa.select(self.model_type)
            if search:
                search_where: sa.ColumnElement[Any] = sa.false()
                for sb in search_by:
                    column = getattr(self.model_type, sb)
                    if hasattr(column.type, 'python_type') and column.type.python_type is str:
                        search_where = sa.or_(search_where, column.ilike(f'%{search}%'))
                    else:
                        search_where = sa.or_(search_where, column == search)
                statement = statement.where(search_where)
            order_by_expr = self.get_order_by_expr(sorting)
            models = (
                (await s.execute(statement.limit(pagination.limit).offset(pagination.offset).order_by(*order_by_expr)))
                .scalars()
                .all()
            )
            objects = [self.read_schema_type.model_validate(model, from_attributes=True) for model in models]
            count_statement = statement.with_only_columns(func.count(self.model_type.id))
            count = (await s.execute(count_statement)).scalar_one()
            return PointsHistoryPaginationSchema(count=count, objects=objects)
