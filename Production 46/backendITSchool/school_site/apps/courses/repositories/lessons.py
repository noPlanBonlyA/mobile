import sqlalchemy as sa
from sqlalchemy.orm import joinedload, contains_eager
from typing import Self, Union, List, Optional
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.schemas import PaginationSchema
from school_site.core.utils.exceptions import ModelNotFoundException
from ..models import Lesson, LessonGroup, LessonStudent, Homework
from school_site.apps.groups.models import Group
from ..schemas import (
    LessonCreateDBSchema,
    LessonReadDBSchema,
    LessonUpdateDBSchema,
    LessonPaginationResultDBSchema,
    LessonReadDBHeadSchema,
    LessonStudentMaterialDetailReadDBSchema,
    LessonTeacherMaterialDetailReadDBSchema,
    LessonSimpleReadSchema,
    LessonInfoTeacherReadDBSchema
)


class LessonRepositoryProtocol(BaseRepositoryImpl[
    Lesson,
    LessonReadDBSchema,
    LessonCreateDBSchema,
    LessonUpdateDBSchema
]):
    async def get_by_course_id(self: Self, course_id: UUID) -> list[LessonReadDBSchema]:
        ...

    async def paginate_by_course(
        self: Self,
        course_id: UUID,
        pagination: PaginationSchema
    ) -> LessonPaginationResultDBSchema:
        ...

    async def check_teacher_material_exists(self: Self, teacher_material_id: UUID) -> bool:
        ...

    async def get_lesson_for_student(self: Self, lesson_id: UUID, student_id: UUID) -> Union[LessonStudentMaterialDetailReadDBSchema, LessonSimpleReadSchema]:
        ...

    async def get_lesson_for_teacher(
    self, lesson_id: UUID, student_id: UUID, teacher_id: UUID
) -> Union[LessonTeacherMaterialDetailReadDBSchema, LessonSimpleReadSchema]:
        ...

    async def get_lesson_info_for_teacher(self: Self, lesson_id: UUID, teacher_id: UUID) -> LessonInfoTeacherReadDBSchema:
        ...

    async def add_homework_to_lesson(self: Self, lessson_id: UUID, homework_material_id: UUID) -> LessonReadDBSchema:
        ...

    async def add_additional_homework_to_lesson(self: Self, lesson_id: UUID, homework_material_id: UUID) -> LessonReadDBSchema:
        ...

    async def get_all_teacher_lessons(self: Self, teacher_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonInfoTeacherReadDBSchema]:
        ...

class LessonRepository(LessonRepositoryProtocol):
    async def get_by_course_id(self: Self, course_id: UUID) -> list[LessonReadDBSchema]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.course_id == course_id)
            models = (await s.execute(statement)).scalars().all()
            return [LessonReadDBSchema.model_validate(model, from_attributes=True) for model in models]

    async def paginate_by_course(
    self: Self,
    course_id: UUID,
    pagination: PaginationSchema
) -> LessonPaginationResultDBSchema:
        async with self.session as s:
            statement = sa.select(
                self.model_type.id,
                self.model_type.name,
                self.model_type.course_id
            ).where(self.model_type.course_id == course_id)

            result = await s.execute(statement.limit(pagination.limit).offset(pagination.offset))
            rows = result.all()  
            objects = [
                LessonReadDBHeadSchema.model_validate(
                    {"id": row[0], "name": row[1], "course_id": row[2]}, 
                    from_attributes=True
                )
                for row in rows
            ]

            count_statement = sa.select(sa.func.count(self.model_type.id)).where(
                self.model_type.course_id == course_id
            )
            count = (await s.execute(count_statement)).scalar_one()

            return LessonPaginationResultDBSchema(count=count, objects=objects)

    async def check_teacher_material_exists(self: Self, teacher_material_id: UUID) -> bool:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.teacher_material_id == teacher_material_id)
            result = await s.execute(statement)
            return result.scalar_one_or_none() is not None 
    
    async def get_lesson_for_student(
    self, lesson_id: UUID, student_id: UUID
) -> Union[LessonStudentMaterialDetailReadDBSchema, LessonSimpleReadSchema]:
        async with self.session as s:
            lesson_group_stmt = (
                sa.select(LessonGroup)
                .join(LessonGroup.students)
                .where(
                    LessonGroup.lesson_id == lesson_id,
                    LessonStudent.student_id == student_id
                )
            )
            lesson_groups = (await s.execute(lesson_group_stmt)).scalars().all()

            if not lesson_groups:
                raise ModelNotFoundException(model=LessonGroup, model_id=lesson_id)

            opened_groups = [group for group in lesson_groups if group.is_opened]
            
            if not opened_groups:
                lesson = await self.get(lesson_id)
                return LessonSimpleReadSchema.model_validate(lesson, from_attributes=True)

            lesson_stmt = (
                sa.select(Lesson)
                .where(Lesson.id == lesson_id)
                .options(
                    joinedload(Lesson.homework),
                    joinedload(Lesson.homework_additional_material),
                    joinedload(Lesson.student_material),
                    joinedload(Lesson.student_additional_material),
                    joinedload(Lesson.groups)
                    .selectinload(LessonGroup.students)
                    .selectinload(LessonStudent.passed_homeworks)
                    .selectinload(Homework.file),
                    joinedload(Lesson.groups)
                    .selectinload(LessonGroup.students)
                    .selectinload(LessonStudent.comments),
                    joinedload(Lesson.groups)
                    .selectinload(LessonGroup.students)
                    .selectinload(LessonStudent.comments_students)
                )
            )

            lesson = (await s.execute(lesson_stmt)).unique().scalar_one()

            lesson.groups = [group for group in lesson.groups if group.id in [g.id for g in opened_groups]]

            return LessonStudentMaterialDetailReadDBSchema.model_validate(lesson, from_attributes=True)           
    
    async def get_lesson_for_teacher(
    self, lesson_id: UUID, student_id: UUID, teacher_id: UUID
) -> Union[LessonTeacherMaterialDetailReadDBSchema, LessonSimpleReadSchema]:
        async with self.session as s:
            lesson_group_stmt = (
                sa.select(LessonGroup)
                .join(LessonGroup.students)
                .join(LessonGroup.group)
                .where(
                    LessonGroup.lesson_id == lesson_id,
                    LessonStudent.student_id == student_id,
                    Group.teacher_id == teacher_id
                )
            )
            lesson_group = (await s.execute(lesson_group_stmt)).scalar()

            if not lesson_group:
                raise ModelNotFoundException(model=LessonGroup, model_id=lesson_id)

            lesson_stmt = (
                sa.select(Lesson)
                .where(Lesson.id == lesson_id)
                .join(Lesson.groups)
                .join(LessonGroup.students)
                .join(LessonGroup.group)
                .where(
                    LessonGroup.id == lesson_group.id,
                    LessonStudent.student_id == student_id,
                    Group.teacher_id == teacher_id
                )
                .options(
                    joinedload(Lesson.teacher_material),
                    joinedload(Lesson.teacher_additional_material),
                    joinedload(Lesson.homework),
                    joinedload(Lesson.homework_additional_material),
                    contains_eager(Lesson.groups)
                    .contains_eager(LessonGroup.students)
                    .selectinload(LessonStudent.passed_homeworks)
                    .selectinload(Homework.file),
                    contains_eager(Lesson.groups)
                    .contains_eager(LessonGroup.students)
                    .selectinload(LessonStudent.comments),
                    contains_eager(Lesson.groups)  # <<< НОВОЕ
                    .contains_eager(LessonGroup.students)
                    .selectinload(LessonStudent.comments_students)
                )
            )

            lesson = (await s.execute(lesson_stmt)).unique().scalar_one()

            return LessonTeacherMaterialDetailReadDBSchema.model_validate(lesson, from_attributes=True)        
    
    async def get_lesson_info_for_teacher(
    self: Self, lesson_id: UUID, teacher_id: UUID
) -> LessonInfoTeacherReadDBSchema:
        async with self.session as s:
            lesson_stmt = (
                sa.select(self.model_type)
                .join(self.model_type.groups)        # ← LessonGroup
                .join(LessonGroup.group)           # ← Group
                .where(
                    Lesson.id == lesson_id,
                    Group.teacher_id == teacher_id  # ← Проверка принадлежности преподавателю
                )
                .options(
                    joinedload(self.model_type.homework),
                    joinedload(self.model_type.homework_additional_material),
                    joinedload(self.model_type.teacher_material),
                    joinedload(self.model_type.teacher_additional_material),
                    joinedload(self.model_type.groups)
                    .selectinload(LessonGroup.students),
                    
                )
            )

            result = await s.execute(lesson_stmt)
            lesson = result.unique().scalar_one_or_none()  # ← Обязательно используйте .unique()

            if not lesson:
                raise ModelNotFoundException(model=Lesson, model_id=lesson_id)

            return LessonInfoTeacherReadDBSchema.model_validate(lesson, from_attributes=True)
        
    
    async def add_homework_to_lesson(self: Self, lesson_id: UUID, homework_material_id: UUID) -> LessonReadDBSchema:
        async with self.session as s, s.begin():
            statement = (
                sa.update(self.model_type)
                .where(self.model_type.id == lesson_id)
                .values(homework_id=homework_material_id)
                .returning(self.model_type)
                )
            model = (await s.execute(statement)).scalar_one_or_none()

            if model is None:
                raise ModelNotFoundException(model=self.model_type, model_id=lesson_id)

            
            return self.read_schema_type.model_validate(model, from_attributes=True)
        
    async def add_additional_homework_to_lesson(self: Self, lesson_id: UUID, homework_material_id: UUID) -> LessonReadDBSchema:
        async with self.session as s, s.begin():
            statement = (
                sa.update(self.model_type)
                .where(self.model_type.id == lesson_id)
                .values(homework_additional_id=homework_material_id)
                .returning(self.model_type)
                )
            model = (await s.execute(statement)).scalar_one_or_none()
            
            if model is None:
                raise ModelNotFoundException(model=self.model_type, model_id=lesson_id)

            return self.read_schema_type.model_validate(model, from_attributes=True)
            
    async def get_all_teacher_lessons(self: Self, teacher_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonInfoTeacherReadDBSchema]:
        async with self.session as s:
            statement = (
                sa.select(Lesson)
                .join(Lesson.groups)
                .join(LessonGroup.group)
                .join(LessonGroup.students)
                .where(Group.teacher_id == teacher_id)
                .options(
                    joinedload(Lesson.homework),
                    joinedload(Lesson.homework_additional_material),
                    joinedload(Lesson.teacher_material),
                    joinedload(Lesson.teacher_additional_material)

                )
            )
            
            if is_graded_homework is not None:
                statement = statement.where(LessonStudent.is_graded_homework == is_graded_homework)
            
            result = await s.execute(statement)
            return [LessonInfoTeacherReadDBSchema.model_validate(model, from_attributes=True) for model in result.unique().scalars().all()]