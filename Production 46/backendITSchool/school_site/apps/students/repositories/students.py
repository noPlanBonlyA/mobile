import sqlalchemy as sa
from uuid import UUID
from typing import List
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.groups.models import GroupStudent
from ..models import Student
from ..schemas import StudentCreateSchema, StudentReadSchema, StudentUpdateSchema


class StudentRepositoryProtocol(BaseRepositoryImpl[
    Student,
    StudentReadSchema,
    StudentCreateSchema,
    StudentUpdateSchema
]):
    async def get_by_user_id(self, user_id: UUID) -> StudentReadSchema:
        ...

    async def get_students_by_group_id(self, group_id: UUID) -> List[Student]:
        ...
    

class StudentRepository(StudentRepositoryProtocol):
    async def get_by_user_id(self, user_id: UUID) -> StudentReadSchema:
        async with self.session as session:
            stmt = sa.select(self.model_type).where(self.model_type.user_id == user_id)
            student = (await session.execute(stmt)).scalar_one_or_none()
            if student is None:
               return None
            return self.read_schema_type.model_validate(student, from_attributes=True)
        
    async def get_students_by_group_id(self, group_id: UUID) -> List[StudentReadSchema]:
        async with self.session as s:
            query = (
                sa.select(self.model_type)
                .join(self.model_type.group_students)
                .where(GroupStudent.group_id == group_id)
            )
            
            result = await s.execute(query)
            students = result.scalars().all()
            
            return [self.read_schema_type.model_validate(student, from_attributes=True)
                    for student in students]