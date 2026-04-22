import sqlalchemy as sa
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import Teacher
from ..schemas import TeacherCreateSchema, TeacherReadSchema, TeacherUpdateSchema


class TeacherRepositoryProtocol(BaseRepositoryImpl[
    Teacher,
    TeacherReadSchema,
    TeacherCreateSchema,
    TeacherUpdateSchema
]):
    async def get_by_user_id(self, user_id: UUID) -> TeacherReadSchema:
        ...


class TeacherRepository(TeacherRepositoryProtocol):
    async def get_by_user_id(self, user_id: UUID) -> TeacherReadSchema:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.user_id == user_id)
            teacher = (await session.execute(stmt)).scalar_one_or_none()
            if teacher is None:
               return None
            return self.read_schema_type.model_validate(teacher, from_attributes=True) 