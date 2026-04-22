import sqlalchemy as sa
from uuid import UUID
from typing import Self, Optional
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.apps.users.models import User
from school_site.apps.users.schemas import (
    UserReadDBSchema, UserCreateSchema, UserUpdateDBSchema, PasswordSchema, 
    UserReadSchema, PaginationResultSchema, UserWithPhotoReadDBSchema, 
    UserWithPhotoPaginationResultDBSchema
)
from school_site.core.enums import UserRole
from school_site.core.schemas import PaginationSchema


class UserRepositoryProtocol(BaseRepositoryImpl[
    User,
    UserReadDBSchema,
    UserCreateSchema,
    UserUpdateDBSchema
]):
    async def get_by_username(self: Self, username: int) -> Optional[UserReadDBSchema]:
        ...

    async def change_password(self: Self, record_id: UUID, password: PasswordSchema) -> UserReadDBSchema:
        ...

    async def get_by_email(self: Self, email: str) -> Optional[UserReadDBSchema]:
       ...

    async def update_password_by_id(self: Self, record_id: UUID, password: PasswordSchema) -> UserReadDBSchema:
        ...

    async def get_with_photo(self, user_id: UUID) -> UserWithPhotoReadDBSchema:
        ...

    async def get_all(self: Self, role: Optional[UserRole] = None, limit: int = 10, offset: int = 0 ) -> PaginationResultSchema[UserReadSchema]:
        ...

    async def paginate(
        self: Self,
        search: str,
        search_by: list[str],
        sorting: list[str],
        pagination: PaginationSchema,
        user: any,
        policies: list[str],
    ) -> UserWithPhotoPaginationResultDBSchema:
        ...

    async def generate_username(self: Self) -> int:
        ...

class UserRepository(UserRepositoryProtocol):
    async def get_by_username(self: Self, username: int) -> Optional[UserReadDBSchema]:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.username == username)
            user = (await session.execute(stmt)).scalar_one_or_none()
            if user is None:
               return None
            return self.read_schema_type.model_validate(user, from_attributes=True)
        
    async def change_password(self: Self, record_id: UUID, password: PasswordSchema) -> UserReadDBSchema:
        async with self.session as session, session.begin():
            stmt = (
                sa.update(self.model_type)
                .where(self.model_type.id == record_id)
                .values(password.model_dump())
                .returning(self.model_type)
            )
            user = (await session.execute(stmt)).scalar_one_or_none()
            if user is None:
                raise ModelNotFoundException(self.model_type, record_id)

            return self.read_schema_type.model_validate(user, from_attributes=True)
        
    async def get_by_email(self: Self, email: str) -> Optional[UserReadDBSchema]:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.email == email)
            user = (await session.execute(stmt)).scalar_one_or_none()
            if user is None:
                return None
            return self.read_schema_type.model_validate(user, from_attributes=True)

    async def get_with_photo(self, user_id: UUID) -> UserWithPhotoReadDBSchema:
        async with self.session as session, session.begin():
            statement = (
                sa.select(self.model_type)
                .options(sa.orm.selectinload(self.model_type.photo)) 
                .where(self.model_type.id == user_id)
            )
            model = (await session.execute(statement)).scalar_one_or_none()
            if model is None:
                raise ModelNotFoundException(self.model_type, user_id)

            return UserWithPhotoReadDBSchema.model_validate(model, from_attributes=True)
        
    async def get_all(self: Self, role: Optional[UserRole] = None, limit: int = 10, offset: int = 0 ) -> PaginationResultSchema[UserReadSchema]:
        async with self.session as session:
            count_query = sa.select(sa.func.count(self.model_type.id))
            data_query = sa.select(self.model_type)
        
            if role:
                count_query = count_query.where(self.model_type.role == role)
                data_query = data_query.where(self.model_type.role == role)
        
            total_count = (await session.execute(count_query)).scalar_one()
        
            data_query = data_query.limit(limit).offset(offset)
            models = (await session.execute(data_query)).scalars().all()
            
            pydantic_models = [UserReadSchema.model_validate(model, from_attributes=True) for model in models]
        
            return PaginationResultSchema[UserReadSchema].model_validate({
            "count": total_count,
            "objects": pydantic_models
            })

    async def paginate(
        self: Self,
        search: str,
        search_by: list[str],
        sorting: list[str],
        pagination: PaginationSchema,
        user: any,
        policies: list[str],
    ) -> UserWithPhotoPaginationResultDBSchema:
        if len(policies) == 0:
            return UserWithPhotoPaginationResultDBSchema(objects=[], count=0)
        async with self.session as s:
            statement = sa.select(self.model_type).options(sa.orm.selectinload(self.model_type.photo)) 
            if search:
                search_where: sa.ColumnElement[any] = sa.false()
                for sb in search_by:
                    search_where = sa.or_(search_where, getattr(self.model_type, sb).ilike(f'%{search}%'))
                statement = statement.where(search_where)
            order_by_expr = self.get_order_by_expr(sorting)
            models = (
                (await s.execute(statement.limit(pagination.limit).offset(pagination.offset).order_by(*order_by_expr)))
                .scalars()
                .all()
            )
            objects = [UserWithPhotoReadDBSchema.model_validate(model, from_attributes=True) for model in models]
            count_statement = statement.with_only_columns(sa.func.count(self.model_type.id))
            count = (await s.execute(count_statement)).scalar_one()
            return UserWithPhotoPaginationResultDBSchema(count=count, objects=objects)

    async def generate_username(self: Self) -> str:
        async with self.session as session:
            subquery = (
                sa.select(
                    self.model_type.username,
                    sa.func.cast(self.model_type.username, sa.Integer).label("username_num"),
                    sa.func.row_number().over(order_by=sa.cast(self.model_type.username, sa.Integer)).label("rn")
                )
                .where(sa.func.regexp_match(self.model_type.username, r'^\d+$').is_not(None))  
                .subquery()
            )

            gap_query = (
                sa.select(subquery.c.rn)
                .where(sa.cast(subquery.c.username, sa.Integer) > subquery.c.rn)
                .order_by(subquery.c.rn)
                .limit(1)
            )

            gap_result = (await session.execute(gap_query)).scalar()

            if gap_result is not None:
                return f"{gap_result:03d}" 
            
            max_username = (
                await session.execute(
                    sa.select(sa.func.max(sa.cast(self.model_type.username, sa.Integer)))
                    .where(sa.func.regexp_match(self.model_type.username, r'^\d+$').is_not(None)) 
                )
            ).scalar() or 0

            next_id = max_username + 1

            if next_id < 100:
                return f"{next_id:03d}"
            else:
                return str(next_id)
