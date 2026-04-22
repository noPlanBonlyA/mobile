import sqlalchemy as sa
from sqlalchemy.orm import joinedload
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import GroupStudent
from ..schemas import (
    GroupAddStudentsDBSchema,
    GroupReadStudentsDBSchema,
    GroupUpdateStudentsDBSchema,
    GroupsForStudentReadSchema
)
from school_site.apps.courses.models import LessonGroup


class GroupStudentsRepositoryProtocol(BaseRepositoryImpl[
    GroupStudent,
    GroupAddStudentsDBSchema,
    GroupReadStudentsDBSchema,
    GroupUpdateStudentsDBSchema
]):
    async def add_students(self, group_id: UUID, students: GroupAddStudentsDBSchema) -> None:
        ...

    async def delete_student(self, group_id: UUID, student_id: UUID) -> bool:
        ...

    async def get_lesson_groups_by_group_id(self, group_id: UUID) -> list[LessonGroup]:
        ...

    async def get_groups_by_student_id(self, student_id: UUID) -> list[GroupsForStudentReadSchema]:
        ...

class GroupStudentsRepository(GroupStudentsRepositoryProtocol):
    async def add_students(self, group_id: UUID, students: GroupAddStudentsDBSchema) -> None:
        async with self.session as s, s.begin():
            for student_id in students.students_id:
                statement = sa.dialects.postgresql.insert(GroupStudent).values(
                    group_id=group_id,
                    student_id=student_id
                ).on_conflict_do_nothing(
                    index_elements=['group_id', 'student_id']
                )
                await s.execute(statement)

    async def delete_student(self, group_id: UUID, student_id: UUID) -> bool:
        async with self.session as s, s.begin():
            await s.execute(
                sa.delete(GroupStudent).where(
                    GroupStudent.group_id == group_id,
                    GroupStudent.student_id == student_id
                )
            )
            return True

    async def get_lesson_groups_by_group_id(self, group_id: UUID) -> list[LessonGroup]:
        async with self.session as s:
            query = sa.select(LessonGroup).where(LessonGroup.group_id == group_id)
            result = await s.execute(query)
            return list(result.scalars().all())

    async def get_groups_by_student_id(self, student_id: UUID) -> list[GroupsForStudentReadSchema]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.student_id == student_id).options(
                joinedload(self.model_type.group)
            )
            groups = (await s.execute(statement)).scalars().all()

            return [GroupsForStudentReadSchema.model_validate(gs, from_attributes=True) for gs in groups]
