import sqlalchemy as sa
from sqlalchemy.sql.expression import func
from sqlalchemy.orm import joinedload
from collections.abc import Iterable
from typing import Self
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.core.schemas import PaginationSchema
from school_site.apps.students.models import Student
from school_site.apps.teachers.models import Teacher
from school_site.apps.courses.models import LessonGroup, Lesson
from ..models import Group
from ..schemas import (
    GroupCreateDBSchema,
    GroupReadDBSchema,
    GroupUpdateDBSchema,
    GroupDBPaginationResultSchema,
    GroupReadDBHeadSchema,
    GroupWithStudentsAndTeacherAndCoursesSchema
)


class GroupRepositoryProtocol(BaseRepositoryImpl[
    Group,
    GroupReadDBSchema,
    GroupCreateDBSchema,
    GroupUpdateDBSchema
]):
    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema
    ) -> GroupDBPaginationResultSchema:
        ...
    async def get_with_students_and_teacher(
    self: Self, group_id: UUID
) -> GroupWithStudentsAndTeacherAndCoursesSchema:
        ...


class GroupRepository(GroupRepositoryProtocol):
    async def paginate(
        self: Self,
        search: str,
        search_by: Iterable[str],
        sorting: Iterable[str],
        pagination: PaginationSchema
    ) -> GroupDBPaginationResultSchema:
        async with self.session as s:
            statement = sa.select(self.model_type.id, self.model_type.name)

            if search:
                search_conditions = [
                    getattr(self.model_type, field).ilike(f"%{search}%")
                    for field in search_by
                ]
                statement = statement.where(sa.or_(*search_conditions))

            order_by_expr = self.get_order_by_expr(sorting)
            statement = statement.order_by(*order_by_expr)
            statement = statement.limit(pagination.limit).offset(pagination.offset)

            results = (await s.execute(statement)).all()
            
            count_statement = sa.select(func.count(self.model_type.id))
            if search:
                count_statement = count_statement.where(sa.or_(*search_conditions))
            count = (await s.execute(count_statement)).scalar_one()
            
            return GroupDBPaginationResultSchema(
                count=count,
                objects=[
                    GroupReadDBHeadSchema(id=id, name=name)
                    for id, name in results
                ]
            ) 
        

    async def get_with_students_and_teacher(
    self: Self, group_id: UUID
) -> GroupWithStudentsAndTeacherAndCoursesSchema:
        async with self.session as s:
            statement = (
                sa.select(self.model_type)
                .where(self.model_type.id == group_id)
                .options(
                    joinedload(self.model_type.students)
                    .joinedload(Student.user), 
                    joinedload(self.model_type.teacher)
                    .joinedload(Teacher.user),
                    joinedload(self.model_type.lessons)  # Group.lessons -> LessonGroup
                    .joinedload(LessonGroup.lesson)      # LessonGroup.lesson -> Lesson
                    .joinedload(Lesson.course)           # Lesson.course -> Course
                )
            )

            result = (await s.execute(statement)).unique().scalar_one_or_none()
            if not result:
                raise ModelNotFoundException(
                    model=self.model_type, model_id=group_id
                )

            unique_courses = {}
            for lesson_group in result.lessons:
                if lesson_group.lesson and lesson_group.lesson.course:
                    course = lesson_group.lesson.course
                    unique_courses[course.id] = {
                        "id": course.id,
                        "name": course.name
                    }

            group_data = {
                "id": result.id,
                "name": result.name,
                "description": result.description,
                "teacher_id": result.teacher_id,
                "created_at": result.created_at,
                "updated_at": result.updated_at,
                "students": result.students,
                "teacher": result.teacher,
                "start_date": result.start_date,
                "end_date": result.end_date,
                "courses": list(unique_courses.values())
            }

            return GroupWithStudentsAndTeacherAndCoursesSchema.model_validate(group_data, from_attributes=True)