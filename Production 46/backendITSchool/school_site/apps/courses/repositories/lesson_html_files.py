from typing import Self
import uuid
import sqlalchemy as sa
from sqlalchemy import func, or_
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..exceptions import FileInUseException
from ..models import LessonHtmlFile, Lesson
from ..schemas import LessonHTMLCreateDBSchema, LessonHTMLUpdateDBSchema, LessonHTMLReadDBSchema


class LessonHTMLRepositoryProtocol(BaseRepositoryImpl[
    LessonHtmlFile,
    LessonHTMLReadDBSchema,
    LessonHTMLCreateDBSchema,
    LessonHTMLUpdateDBSchema
]):
    async def delete(self: Self, file_id: uuid.UUID) -> bool:
        ...


class LessonHTMLRepository(LessonHTMLRepositoryProtocol):
    async def delete(self: Self, file_id: uuid.UUID) -> bool:
        async with self.session as s, s.begin():
            result = await s.execute(
            sa.select(func.count()).select_from(Lesson).where(
                or_(
                    Lesson.teacher_material_id == file_id,
                    Lesson.student_material_id == file_id,
                    Lesson.homework_id == file_id
                )
            )
        )
        ref_count = result.scalar()

        if ref_count > 0:
            raise FileInUseException()
        
        statement = sa.delete(self.model_type).where(self.model_type.id == file_id)
        await s.execute(statement)
        return True