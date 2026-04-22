import sqlalchemy as sa
from sqlalchemy.orm import joinedload
from typing import List
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.utils.exceptions import ModelNotFoundException
from ..models import CourseStudent, Course
from ..schemas import CourseStudentCreateSchema, CourseStudentUpdateDBSchema, CourseStudentReadSchema,\
    CourseStudentWithCoursesDBSchema


class CourseStudentRepositoryProtocol(BaseRepositoryImpl[
    CourseStudent,
    CourseStudentReadSchema,
    CourseStudentCreateSchema,
    CourseStudentUpdateDBSchema
]):
    async def get_courses_by_student_id(self, student_id: UUID) -> List[CourseStudentWithCoursesDBSchema]:
        ...

    async def get_by_student_id_and_course_id(self, student_id: UUID, course_id: UUID) -> CourseStudentReadSchema:
        ...

            
class CourseStudentRepository(CourseStudentRepositoryProtocol):
    async def get_courses_by_student_id(self, student_id: UUID) -> List[CourseStudentWithCoursesDBSchema]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.student_id == student_id).options(
                joinedload(self.model_type.course)
                .joinedload(Course.photo)
            )
            models = (await s.execute(statement)).scalars().all()
            return [CourseStudentWithCoursesDBSchema.model_validate(model, from_attributes=True) for model in models]
    
    async def get_by_student_id_and_course_id(self, student_id: UUID, course_id: UUID) -> CourseStudentReadSchema:
        async with self.session as s:
            statement = sa.select(self.model_type).where(
                self.model_type.student_id == student_id,
                self.model_type.course_id == course_id
            )
            model = (await s.execute(statement)).scalar_one_or_none()
            if not model:
                return None
            return CourseStudentReadSchema.model_validate(model, from_attributes=True)
