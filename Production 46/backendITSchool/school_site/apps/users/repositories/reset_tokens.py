from typing import Self
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import PasswordResetTokens
from ..schemas import ResetTokenCreateSchema, ResetTokenUpdateSchema, ResetTokenReadSchema
import sqlalchemy as sa


class ResetTokenRepositoryProtocol(BaseRepositoryImpl[
    PasswordResetTokens,
    ResetTokenReadSchema,
    ResetTokenCreateSchema,
    ResetTokenUpdateSchema
]):
    async def delete_all_expired_tokens(self: Self) -> bool:
        ...

class ResetTokenRepository(ResetTokenRepositoryProtocol):
    async def delete_all_expired_tokens(self: Self) -> bool:
        async with self.session as session, session.begin():
            stmt = sa.delete(self.model_type).where(
                self.model_type.expires_at < sa.func.now()
                )
            await session.execute(stmt)

            return True
        