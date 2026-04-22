import logging
from typing import Protocol, List
from ..services.lesson_group import LessonGroupServiceProtocol
from ..services.lesson_student import LessonStudentServiceProtocol
from ..services.lessons import LessonServiceProtocol
from ..services.course_student import CourseStudentServiceProtocol
from ..schemas import (
    LessonGroupCreateSchema,
    LessonStudentCreateSchema,
    LessonGroupReadSchema,
    CourseStudentCreateSchema
)
from school_site.apps.students.services.students import StudentsByGroupServiceProtocol  

logger = logging.getLogger(__name__)


class CombinedLessonGroupStudentServiceProtocol(Protocol):
    async def create_lesson_group_with_students(self, lesson_group_data: LessonGroupCreateSchema) -> LessonGroupReadSchema:
        ...

    async def bulk_create_lesson_groups_with_students(self, lesson_groups_data: List[LessonGroupCreateSchema]) -> List[LessonGroupReadSchema]:
        ...


class CombinedLessonGroupStudentService:
    def __init__(
        self,
        lesson_group_service: LessonGroupServiceProtocol,
        lesson_student_service: LessonStudentServiceProtocol,
        course_student_service: CourseStudentServiceProtocol,
        lesson_service: LessonServiceProtocol,
        student_service: StudentsByGroupServiceProtocol
    ):
        self.lesson_group_service = lesson_group_service
        self.lesson_student_service = lesson_student_service
        self.course_student_service = course_student_service
        self.lesson_service = lesson_service
        self.student_service = student_service

    async def create_lesson_group_with_students(self, lesson_group_data: LessonGroupCreateSchema) -> LessonGroupReadSchema:
        """
        Создает LessonGroup и для каждого студента из группы:
        - Создает LessonStudent
        - Создает CourseStudent, если ещё нет
        """

        created_lesson_group = await self.lesson_group_service.create(lesson_group_data)

        students = await self.student_service.get_students_by_group_id(lesson_group_data.group_id)
        if not students:
            logger.warning(f"Group {lesson_group_data.group_id} has no students")
            return created_lesson_group

        lesson = await self.lesson_service.get(created_lesson_group.lesson_id)
        course_id = lesson.course_id

        lesson_students = []
        course_students_to_create = []

        for student in students:
            lesson_student = LessonStudentCreateSchema(
                student_id=student.id,
                lesson_group_id=created_lesson_group.id
            )
            lesson_students.append(lesson_student)

        created_lesson_students = await self.lesson_student_service.bulk_create(lesson_students)

        for lesson_student in created_lesson_students:
            course_student = await self.course_student_service.get_by_student_id_and_course_id(
                student_id=lesson_student.student_id,
                course_id=course_id
            )
            
            if not course_student:
                course_students_to_create.append(
                    CourseStudentCreateSchema(
                        student_id=lesson_student.student_id,
                        course_id=course_id
                    )
                )

        if course_students_to_create:
            await self.course_student_service.bulk_create(course_students_to_create)
            logger.info(f"Created {len(course_students_to_create)} CourseStudents")

        return created_lesson_group

    async def bulk_create_lesson_groups_with_students(self, lesson_groups_data: List[LessonGroupCreateSchema]) -> List[LessonGroupReadSchema]:
        if not lesson_groups_data:
            logger.warning("Received empty list for bulk creation")
            return []

        created_groups = []
        failed_groups = []

        for group_data in lesson_groups_data:
            try:
                created_group = await self.create_lesson_group_with_students(group_data)
                created_groups.append(created_group)
            except Exception as e:
                logger.error(f"Failed to create LessonGroup with students: {e}")
                failed_groups.append(group_data)

        if failed_groups:
            logger.warning(f"Failed to create {len(failed_groups)} groups")

        return created_groups