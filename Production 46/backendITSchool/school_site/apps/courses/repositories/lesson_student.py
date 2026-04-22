import sqlalchemy as sa
from sqlalchemy.orm import joinedload, selectinload
from typing import Self, List, Optional
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.apps.students.models import Student
from school_site.core.utils.exceptions import ModelNotFoundException
from ..models import LessonStudent, LessonGroup, Homework, Lesson
from ..schemas import (LessonStudentCreateSchema, LessonStudentUpdateDBSchema, LessonStudentReadSchema,
    LessonStudentReadWithStudentSchema, 
    LessonStudentReadWithStudentDBSchema,
    LessonStudentDetailReadDBSchema,
    LessonStudentWithLessonGroupReadSchema
)


class LessonStudentRepositoryProtocol(BaseRepositoryImpl[
    LessonStudent,
    LessonStudentReadSchema,
    LessonStudentCreateSchema,
    LessonStudentUpdateDBSchema
    
]):
    async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
        ...
    
    async def get_all_by_lesson_group_id(self: Self, lesson_group_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonStudentReadWithStudentDBSchema]:
        ...

    async def get_all_lesson_students_by_lesson_group(
        self: Self, lesson_group_id: UUID
    ) -> List[LessonStudentReadWithStudentSchema]:
        ...

    async def get_detailed_by_id(self, lesson_student_id: UUID) -> LessonStudentDetailReadDBSchema:
        ...
    
    async def get_all_lesson_students_by_student_id(self: Self, student_id: UUID) -> List[LessonStudentReadSchema]:
        ...
    
   

class LessonStudentRepository(LessonStudentRepositoryProtocol):
    async def get_lesson_student(self: Self, student_id: UUID, lesson_id: UUID) -> LessonStudentReadSchema:
        async with self.session as s:
            stmt = (
                sa.select(self.model_type)
                .join(LessonGroup)
                .where(
                    self.model_type.student_id == student_id,
                    LessonGroup.lesson_id == lesson_id
                )
            )
            
            model = (await s.execute(stmt)).scalar_one()
            return LessonStudentReadSchema.model_validate(model, from_attributes=True)

    async def get_all_by_lesson_group_id(self, lesson_group_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonStudentReadWithStudentSchema]:
        async with self.session as s:
            statement = (
                sa.select(LessonStudent)
                .join(LessonStudent.student)
                .where(LessonStudent.lesson_group_id == lesson_group_id).options(
                    joinedload(self.model_type.student)
                    .joinedload(Student.user)
                )
            )
            
            if is_graded_homework is not None:
                statement = statement.where(LessonStudent.is_graded_homework == is_graded_homework)
            
            result = await s.execute(statement)
            return [LessonStudentReadWithStudentSchema.model_validate(model, from_attributes=True) for model in result.scalars().all()]
    
    async def get_all_lesson_students_by_student_id(self: Self, student_id: UUID) -> List[LessonStudentWithLessonGroupReadSchema]:
        async with self.session as s:
            stmt = (
                sa.select(self.model_type)
                .options(joinedload(self.model_type.lesson_group))  # Подгружаем связь с LessonGroup
                .where(self.model_type.student_id == student_id)
            )
            models = (await s.execute(stmt)).scalars().all()
            return [
                LessonStudentWithLessonGroupReadSchema.model_validate(model, from_attributes=True)
                for model in models
            ]

    async def get_all_lesson_students_by_lesson_group(
        self: Self, lesson_group_id: UUID
    ) -> List[LessonStudentReadWithStudentSchema]:
        async with self.session as s:
            stmt = (
                sa.select(self.model_type)
                .where(self.model_type.lesson_group_id == lesson_group_id)
                .options(
                    joinedload(self.model_type.student)
                    .joinedload(Student.user)
                )
            )
            
            models = (await s.execute(stmt)).scalars().all()
            return [
                LessonStudentReadWithStudentSchema.model_validate(model, from_attributes=True)
                for model in models
            ]
        
    async def get_detailed_by_id(self, lesson_student_id: UUID) -> LessonStudentDetailReadDBSchema:
        async with self.session as s:
            stmt = (
                sa.select(self.model_type)
                .where(self.model_type.id == lesson_student_id)
                .options(
                    joinedload(self.model_type.student)
                    .joinedload(Student.user),
                    
                    selectinload(self.model_type.passed_homeworks)
                    .joinedload(Homework.file),
                    
                    selectinload(self.model_type.comments),
                    selectinload(self.model_type.comments_students)
                )
            )
            
            result = await s.execute(stmt)
            lesson_student = result.unique().scalar_one_or_none()
            
            if lesson_student is None:
                raise ModelNotFoundException(
                    model=self.model_type,
                    model_id=lesson_student_id
                )
                
            return LessonStudentDetailReadDBSchema.model_validate(lesson_student, from_attributes=True)
