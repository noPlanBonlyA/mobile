import logging
from typing import Protocol, Self, Union, List, Optional
from uuid import UUID
from school_site.core.schemas import PaginationSchema
from school_site.core.services.files import FileServiceProtocol
from ..repositories.lessons import LessonRepositoryProtocol
from ..schemas import (
    LessonCreateSchema,
    LessonCreateDBSchema,
    LessonUpdateDBSchema,
    LessonUpdateSchema,
    LessonReadSchema,
    LessonPaginationResultSchema,
    LessonSimpleReadSchema,
    FileHomeworkReadSchema,
    HomeworkReadSchema,
    LessonHTMLReadSchema,
    LessonStudentDetailReadSchema,
    LessonGroupDetailBaseSchema,
    LessonTeacherMaterialDetailReadDBSchema,
    LessonTeacherMaterialDetailReadSchema,
    LessonStudentMaterialDetailReadDBSchema,
    LessonStudentMaterialDetailReadSchema,
    LessonInfoTeacherReadSchema
)

logger = logging.getLogger(__name__)


class LessonServiceProtocol(Protocol):
    async def create(self, course_id: UUID, lesson: LessonCreateSchema) -> LessonReadSchema:
        ...

    async def get(self, lesson_id: UUID) -> LessonReadSchema:
        ...

    async def update(self, course_id: UUID, lesson_id: UUID, lesson: LessonUpdateSchema) -> LessonReadSchema:
        ...

    async def delete(self, course_id: UUID, lesson_id: UUID) -> None:
        ...

    async def list(self, course_id: UUID, pagination: PaginationSchema) -> LessonPaginationResultSchema:
        ...

    async def add_homework_to_lesson(self, lesson_id: UUID, homework_material_id: UUID) -> LessonReadSchema:
        ...

    async def add_additional_homework_to_lesson(self: Self, lesson_id: UUID, homework_material_id: UUID) -> LessonReadSchema:
        ...


class LessonService(LessonServiceProtocol):
    def __init__(self, lesson_repository: LessonRepositoryProtocol):
        self.lesson_repository = lesson_repository

    async def create(self, course_id: UUID, lesson: LessonCreateSchema) -> LessonReadSchema:
        db_lesson_create = LessonCreateDBSchema(
            name=lesson.name,
            teacher_material_id=lesson.teacher_material_id,
            teacher_additional_material_id=lesson.teacher_additional_material_id,
            student_material_id=lesson.student_material_id,
            student_additional_material_id=lesson.student_additional_material_id,
            homework_id=lesson.homework_id,
            homework_additional_id=lesson.homework_additional_id,
            course_id=course_id
        )
        return await self.lesson_repository.create(db_lesson_create)

    async def get(self, lesson_id: UUID) -> LessonReadSchema:
        return await self.lesson_repository.get(lesson_id)

    async def update(self, course_id: UUID, lesson_id: UUID, lesson: LessonUpdateSchema) -> LessonReadSchema:
        db_lesson_update = LessonUpdateDBSchema(
            id=lesson_id,
            name=lesson.name,
            teacher_material_id=lesson.teacher_material_id,
            teacher_additional_material_id=lesson.teacher_additional_material_id,
            student_material_id=lesson.student_material_id,
            student_additional_material_id=lesson.student_additional_material_id,
            homework_id=lesson.homework_id,
            homework_additional_id=lesson.homework_additional_id,
            course_id=course_id
        )
        return await self.lesson_repository.update(db_lesson_update)

    async def delete(self, course_id: UUID, lesson_id: UUID) -> None:
        await self.lesson_repository.delete(lesson_id)

    async def list(self, course_id: UUID, pagination: PaginationSchema) -> LessonPaginationResultSchema:
        return await self.lesson_repository.paginate_by_course(course_id, pagination)

    async def add_homework_to_lesson(self, lesson_id: UUID, homework_material_id: UUID) -> LessonReadSchema:
        return await self.lesson_repository.add_homework_to_lesson(lesson_id, homework_material_id) 

    async def add_additional_homework_to_lesson(self: Self, lesson_id: UUID, homework_material_id: UUID) -> LessonReadSchema:
        return await self.lesson_repository.add_additional_homework_to_lesson(lesson_id, homework_material_id)

class GetLessonWithMaterialsServiceProtocol(Protocol):
    async def get_lesson_for_student(self: Self, lesson_id: UUID, student_id: UUID) -> Union[LessonSimpleReadSchema, LessonStudentMaterialDetailReadSchema]:
        ...
    
    async def get_lesson_for_teacher(
    self, lesson_id: UUID, student_id: UUID, teacher_id: UUID
) -> Union[LessonTeacherMaterialDetailReadSchema, LessonSimpleReadSchema]:
        ...

    async def get_lesson_info_for_teacher(self: Self, lesson_id: UUID, teacher_id: UUID) -> LessonInfoTeacherReadSchema:
        ...

    async def get_all_teacher_lessons(self: Self, teacher_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonInfoTeacherReadSchema]:
        ...

class GetLessonWithMaterialsService(GetLessonWithMaterialsServiceProtocol):
    def __init__(self, lesson_repository: LessonRepositoryProtocol,
                 file_service: FileServiceProtocol):
        self.file_service = file_service
        self.lesson_repository = lesson_repository

    async def get_lesson_for_student(
    self, lesson_id: UUID, student_id: UUID
) -> Union[LessonSimpleReadSchema, LessonStudentMaterialDetailReadSchema]:
        result = await self.lesson_repository.get_lesson_for_student(lesson_id, student_id)
        if isinstance(result, LessonSimpleReadSchema):
            return result

        homework_material, homework_additional, groups = await self._process_lesson_data(result)

        student_material = None
        if result.student_material:
            student_material_url = await self.file_service.get_url(result.student_material.path)
            student_material = LessonHTMLReadSchema(
                id=result.student_material.id,
                name=result.student_material.name,
                url=student_material_url
            )

        student_additional_material = None
        if result.student_additional_material:
            student_additional_url = await self.file_service.get_url(result.student_additional_material.path)
            student_additional_material = LessonHTMLReadSchema(
                id=result.student_additional_material.id,
                name=result.student_additional_material.name,
                url=student_additional_url
            )

        new_result =  LessonStudentMaterialDetailReadSchema(
            id=result.id,
            name=result.name,
            course_id=result.course_id,
            homework=homework_material,
            homework_additional_material=homework_additional,
            student_material=student_material,
            student_additional_material=student_additional_material,
            groups=groups
        )
        return new_result
    
    async def get_lesson_for_teacher(
    self, lesson_id: UUID, student_id: UUID, teacher_id: UUID
) -> Union[LessonTeacherMaterialDetailReadSchema, LessonSimpleReadSchema]:
        result = await self.lesson_repository.get_lesson_for_teacher(lesson_id, student_id, teacher_id)

        if isinstance(result, LessonSimpleReadSchema):
            return result

        homework_material, homework_additional_material, groups = await self._process_lesson_data(result)

        teacher_material = None
        if result.teacher_material:
            teacher_url = await self.file_service.get_url(result.teacher_material.path)
            teacher_material = LessonHTMLReadSchema(
                id=result.teacher_material.id,
                name=result.teacher_material.name,
                url=teacher_url
            )

        teacher_additional_material = None
        if result.teacher_additional_material:
            teacher_additional_url = await self.file_service.get_url(result.teacher_additional_material.path)
            teacher_additional_material = LessonHTMLReadSchema(
                id=result.teacher_additional_material.id,
                name=result.teacher_additional_material.name,
                url=teacher_additional_url
            )

        return LessonTeacherMaterialDetailReadSchema(
            id=result.id,
            name=result.name,
            course_id=result.course_id,
            homework=homework_material,
            homework_additional_material=homework_additional_material,
            teacher_material=teacher_material,
            teacher_additional_material=teacher_additional_material,
            groups=groups
        )
    
    async def get_lesson_info_for_teacher(self: Self, lesson_id: UUID, teacher_id: UUID) -> LessonInfoTeacherReadSchema:
        result = await self.lesson_repository.get_lesson_info_for_teacher(lesson_id, teacher_id)

        homework_url = await self.file_service.get_url(result.homework.path) if result.homework else None
        homework_additional_url = await self.file_service.get_url(result.homework_additional_material.path) if result.homework_additional_material else None
        teacher_material_url = await self.file_service.get_url(result.teacher_material.path) if result.teacher_material else None
        teacher_additional_material_url = await self.file_service.get_url(result.teacher_additional_material.path) if result.teacher_additional_material else None

        return LessonInfoTeacherReadSchema(
            id=result.id,
            name=result.name,
            course_id=result.course_id,
            homework=LessonHTMLReadSchema(
                id=result.homework.id,
                name=result.homework.name,
                url=homework_url
            ) if result.homework else None,
            homework_additional_material=LessonHTMLReadSchema(
                id=result.homework_additional_material.id,
                name=result.homework_additional_material.name,
                url=homework_additional_url
            ) if result.homework_additional_material else None,
            teacher_material=LessonHTMLReadSchema(
                id=result.teacher_material.id,
                name=result.teacher_material.name,
                url=teacher_material_url
            ) if result.teacher_material else None,
            teacher_additional_material=LessonHTMLReadSchema(
                id=result.teacher_additional_material.id,
                name=result.teacher_additional_material.name,
                url=teacher_additional_material_url
            ) if result.teacher_additional_material else None,
        )
    
    async def _process_lesson_data(self, lesson: Union[LessonTeacherMaterialDetailReadDBSchema, LessonStudentMaterialDetailReadDBSchema]) -> \
        tuple[Union[LessonHTMLReadSchema, None], Union[LessonHTMLReadSchema, None], list[LessonGroupDetailBaseSchema]]:
        homework_material = None
        if lesson.homework:
            homework_url = await self.file_service.get_url(lesson.homework.path)
            homework_material = LessonHTMLReadSchema(
                id=lesson.homework.id,
                name=lesson.homework.name,
                url=homework_url
            )
        homework_additional_material = None
        if lesson.homework_additional_material:
            homework_additional_url = await self.file_service.get_url(lesson.homework_additional_material.path)
            homework_additional_material = LessonHTMLReadSchema(
                id=lesson.homework_additional_material.id,
                name=lesson.homework_additional_material.name,
                url=homework_additional_url
            )

        processed_groups = []
        if lesson.groups:
            for group in lesson.groups:
                processed_students = []
                if group.students:
                    for student in group.students:
                        processed_passed_homeworks = []
                        if student.passed_homeworks:
                            for hw in student.passed_homeworks:
                                hw_url = await self.file_service.get_url(hw.file.path)
                                file_schema = FileHomeworkReadSchema(id=hw.file.id, name=hw.file.name, url=hw_url)
                                homework_schema = HomeworkReadSchema(id=hw.id, file_id=hw.file.id, homework=file_schema)
                                processed_passed_homeworks.append(homework_schema)

                        comment_schemas = [comment.model_dump() for comment in student.comments]

                        student_schema = LessonStudentDetailReadSchema(
                            id=student.id,
                            student_id=student.student_id,
                            lesson_group_id=student.lesson_group_id,
                            is_visited=student.is_visited,
                            is_excused_absence=student.is_excused_absence,
                            is_compensated_skip=student.is_compensated_skip,
                            is_sent_homework=student.is_sent_homework,
                            is_graded_homework=student.is_graded_homework,
                            coins_for_visit=student.coins_for_visit,
                            coins_for_homework=student.coins_for_homework,
                            passed_homeworks=processed_passed_homeworks,
                            comments=comment_schemas,
                            comments_students=student.comments_students
                        )
                        processed_students.append(student_schema)

                group_schema = LessonGroupDetailBaseSchema(
                    lesson_id=group.lesson_id,
                    group_id=group.group_id,
                    auditorium=group.auditorium,
                    start_datetime=group.start_datetime,
                    end_datetime=group.end_datetime,
                    is_opened=group.is_opened,
                    students=processed_students
                )
                processed_groups.append(group_schema)

        return homework_material, homework_additional_material, processed_groups
    
    async def get_all_teacher_lessons(self: Self, teacher_id: UUID, is_graded_homework: Optional[bool] = None) -> List[LessonInfoTeacherReadSchema]:
        lessons = await self.lesson_repository.get_all_teacher_lessons(teacher_id, is_graded_homework)
        result = []
        for lesson in lessons:
            homework_url = await self.file_service.get_url(lesson.homework.path) if lesson.homework else None
            homework_additional_url = await self.file_service.get_url(lesson.homework_additional_material.path) if lesson.homework_additional_material else None
            teacher_material_url = await self.file_service.get_url(lesson.teacher_material.path) if lesson.teacher_material else None
            teacher_additional_material_url = await self.file_service.get_url(lesson.teacher_additional_material.path) if lesson.teacher_additional_material else None

            result.append(LessonInfoTeacherReadSchema(
                id=lesson.id,
                name=lesson.name,
                course_id=lesson.course_id,
                homework=LessonHTMLReadSchema(
                    id=lesson.homework.id,
                    name=lesson.homework.name,
                    url=homework_url
                ) if lesson.homework else None,
                homework_additional_material=LessonHTMLReadSchema(
                    id=lesson.homework_additional_material.id,
                    name=lesson.homework_additional_material.name,
                    url=homework_additional_url
                ) if lesson.homework_additional_material else None,
                teacher_material=LessonHTMLReadSchema(
                    id=lesson.teacher_material.id,
                    name=lesson.teacher_material.name,
                    url=teacher_material_url
                ) if lesson.teacher_material else None,
                teacher_additional_material=LessonHTMLReadSchema(
                    id=lesson.teacher_additional_material.id,
                    name=lesson.teacher_additional_material.name,
                    url=teacher_additional_material_url
                ) if lesson.teacher_additional_material else None
            ))

        return result
