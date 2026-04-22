import sqlalchemy as sa
from uuid import UUID
from typing import Self
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.users.models import RefreshToken
from school_site.apps.users.schemas import RefreshTokenReadDBSchema, RefreshTokenUpdateDBSchema, RefreshTokenCreateDBSchema


class RefreshTokenRepositoryProtocol(BaseRepositoryImpl[
    RefreshToken,
    RefreshTokenReadDBSchema,
    RefreshTokenCreateDBSchema,
    RefreshTokenUpdateDBSchema
]):
    async def count_by_user_id(self: Self, user_id: UUID) -> int:
        ...

    async def get_oldest_by_user_id(self: Self, user_id: UUID) -> RefreshTokenReadDBSchema:
        ...
    
    async def get_by_hashed_token(self: Self, hashed_token: str) -> RefreshTokenReadDBSchema:
        ...

    async def delete_all_by_user_id(self: Self, user_id: UUID) -> bool:
        ...

class RefreshTokenRepository(RefreshTokenRepositoryProtocol):
    async def count_by_user_id(self: Self, user_id: UUID) -> int:
        async with self.session as session:
            stmt = sa.select(sa.func.count(self.model_type.id)).where(
                self.model_type.user_id == user_id
            )
            result = await session.execute(stmt)
            count = result.scalar()
            return count

    async def get_oldest_by_user_id(self: Self, user_id: UUID) -> RefreshTokenReadDBSchema:
        async with self.session as session:
            stmt = (
                sa.select(self.model_type)
                .where(self.model_type.user_id == user_id)
                .order_by(self.model_type.created_at.asc())
                .limit(1)
            )
            token = (await session.execute(stmt)).scalar_one_or_none()
            if token is None:
                return None
            return self.read_schema_type.model_validate(token, from_attributes=True)

    async def get_by_hashed_token(self: Self, hashed_token: str) -> RefreshTokenReadDBSchema:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(
                self.model_type.hashed_refresh_token == hashed_token
            )
            token = (await session.execute(stmt)).scalar_one_or_none()
            if token is None:
               return None
            return self.read_schema_type.model_validate(token, from_attributes=True)
    
    async def delete_all_by_user_id(self: Self, user_id: UUID) -> bool:
        async with self.session as session, session.begin():
            stmt = sa.delete(self.model_type).where(
                self.model_type.user_id == user_id
            )
            await session.execute(stmt)
            
            return True