import sqlalchemy as sa
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import Group
from ..schemas import (
    GroupAddTeacherDBSchema,
    GroupReadTeacherDBSchema,
    GroupUpdateTeacherDBSchema
)


class GroupTeachersRepositoryProtocol(BaseRepositoryImpl[
    Group, 
    GroupAddTeacherDBSchema,
    GroupReadTeacherDBSchema,
    GroupUpdateTeacherDBSchema
]):
    async def add_teacher(self, group_id: UUID, teacher_id: UUID) -> None:
        ...

    async def delete_teacher(self, group_id: UUID, teacher_id: UUID) -> bool:
        ...

    async def has_teacher(self, group_id: UUID) -> bool:
        ...

    async def get_by_teacher_id(self, teacher_id: UUID) -> list[GroupReadTeacherDBSchema]:
        ...


class GroupTeachersRepository(GroupTeachersRepositoryProtocol):
    async def add_teacher(self, group_id: UUID, teacher_id: UUID) -> None:
        async with self.session as s, s.begin():
            statement = sa.update(Group).where(
                Group.id == group_id
            ).values(
                teacher_id=teacher_id
            )
            await s.execute(statement)

    async def delete_teacher(self, group_id: UUID, teacher_id: UUID) -> bool:
        async with self.session as s, s.begin():
            statement = sa.update(Group).where(
                Group.id == group_id,
                Group.teacher_id == teacher_id
            ).values(
                teacher_id=None
            )
            await s.execute(statement)
            return True

    async def has_teacher(self, group_id: UUID) -> bool:
        async with self.session as s:
            statement = sa.select(Group.teacher_id).where(Group.id == group_id)
            result = await s.execute(statement)
            teacher_id = result.scalar_one_or_none()
            return teacher_id is not None 
        
    async def get_by_teacher_id(self, teacher_id: UUID) -> list[GroupReadTeacherDBSchema]:
        async with self.session as s:
            statement = sa.select(Group).where(Group.teacher_id == teacher_id)
            result = await s.execute(statement)
            groups = result.scalars().all()
            return [GroupReadTeacherDBSchema.model_validate(group, from_attributes=True) for group in groups]