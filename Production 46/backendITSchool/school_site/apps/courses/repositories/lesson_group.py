import sqlalchemy as sa
from sqlalchemy.orm import joinedload
from typing import List, Self
from uuid import UUID
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import LessonGroup, Lesson
from ..schemas import LessonGroupCreateSchema, LessonGroupUpdateDBSchema, LessonGroupReadSchema, \
    LessonGroupReadWithLessonSchema

class LessonGroupRepositoryProtocol(BaseRepositoryImpl[
    LessonGroup,
    LessonGroupReadSchema,
    LessonGroupCreateSchema,
    LessonGroupUpdateDBSchema
]):
    async def get_by_group_id(self, group_id: UUID) -> List[LessonGroupReadWithLessonSchema]:
        ...
    
    async def detach_group_from_lesson(self: Self, lesson_id: UUID, group_id: UUID) -> bool:
        ...
    
    async def detach_group_from_course(self: Self, group_id: UUID, course_id: UUID) -> bool:
        ...


class LessonGroupRepository(LessonGroupRepositoryProtocol):
    async def get_by_group_id(self, group_id: UUID) -> List[LessonGroupReadWithLessonSchema]:
        async with self.session as s:
            statement = sa.select(self.model_type).where(self.model_type.group_id == group_id).options(
                joinedload(self.model_type.lesson)
            )
            result = await s.execute(statement)
            lesson_groups = result.scalars().all()
            return [
                LessonGroupReadWithLessonSchema.model_validate(lesson_group, from_attributes=True) 
                for lesson_group in lesson_groups
            ]
    
    async def detach_group_from_lesson(self: Self, lesson_id: UUID, group_id: UUID) -> bool:
        """
        Открепить группу от занятия - удалить LessonGroup по lesson_id и group_id
        
        Args:
            lesson_id: UUID занятия
            group_id: UUID группы
            
        Returns:
            bool: True если запись была удалена, False если не найдена
        """
        async with self.session as s, s.begin():
            stmt = sa.delete(self.model_type).where(
                sa.and_(
                    self.model_type.lesson_id == lesson_id,
                    self.model_type.group_id == group_id
                )
            )
            await s.execute(stmt)
            return True
    
    async def detach_group_from_course(self: Self, group_id: UUID, course_id: UUID) -> bool:
        """
        Открепить группу от курса - удалить все LessonGroup для группы с group_id 
        и всеми lesson_id у которых lesson.course_id == course_id
        
        Args:
            group_id: UUID группы
            course_id: UUID курса
            
        Returns:
            int: Количество удаленных записей
        """
        async with self.session as s, s.begin():
            # Используем EXISTS подзапрос
            stmt = sa.delete(self.model_type).where(
                sa.and_(
                    self.model_type.group_id == group_id,
                    sa.exists().where(
                        sa.and_(
                            Lesson.id == self.model_type.lesson_id,
                            Lesson.course_id == course_id
                        )
                    )
                )
            )
            await s.execute(stmt)
            return True
