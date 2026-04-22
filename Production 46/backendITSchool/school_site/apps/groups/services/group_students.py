import logging
from school_site.apps.groups.services.groups import GroupServiceProtocol
from typing import Protocol
from uuid import UUID
from sqlalchemy.exc import IntegrityError
from school_site.apps.students.services.students import StudentServiceProtocol
from ..repositories.group_students import GroupStudentsRepositoryProtocol
from ..schemas import GroupAddStudentsSchema, GroupAddStudentsDBSchema, GroupReadStudentsSchema, GroupsForStudentReadSchema
from school_site.core.utils.exceptions import ModelNotFoundException
from school_site.apps.students.models import Student
from school_site.apps.courses.services.lesson_group import LessonGroupServiceProtocol
from school_site.apps.courses.services.lesson_student import LessonStudentServiceProtocol
from school_site.apps.courses.services.course_student import CourseStudentServiceProtocol
from school_site.apps.courses.schemas import LessonStudentCreateSchema, CourseStudentCreateSchema
from school_site.apps.courses.services.lessons import LessonServiceProtocol

logger = logging.getLogger(__name__)


class GroupStudentServiceProtocol(Protocol):
    async def add_students(self, group_id: UUID, students: GroupAddStudentsSchema) -> GroupReadStudentsSchema:
        ...

    async def delete_student(self, group_id: UUID, student_id: UUID) -> bool:
        ...

    async def get_groups_by_student_id(self, student_id: UUID) -> list[GroupsForStudentReadSchema]:
        ...

class GroupStudentService(GroupStudentServiceProtocol):
    def __init__(
        self,
        group_students_repository: GroupStudentsRepositoryProtocol,
        group_service: GroupServiceProtocol,
        student_service: StudentServiceProtocol,
        lesson_group_service: LessonGroupServiceProtocol,
        lesson_student_service: LessonStudentServiceProtocol,
        course_student_service: CourseStudentServiceProtocol,
        lesson_service: LessonServiceProtocol
    ):
        self.group_students_repository = group_students_repository
        self.group_service = group_service
        self.student_service = student_service
        self.lesson_group_service = lesson_group_service
        self.lesson_student_service = lesson_student_service
        self.course_student_service = course_student_service
        self.lesson_service = lesson_service

    async def add_students(self, group_id: UUID, students: GroupAddStudentsSchema) -> GroupReadStudentsSchema:
        group = await self.group_service.get(group_id)
        try:
            students_db = GroupAddStudentsDBSchema(students_id=students.students_id)
            await self.group_students_repository.add_students(group_id, students_db)
            lesson_groups = await self.group_students_repository.get_lesson_groups_by_group_id(group_id)
            for student_id in students.students_id:
                lesson_students_to_create = []
                course_students_to_create = []
                for lesson_group in lesson_groups:
                    lesson = await self.lesson_service.get(lesson_group.lesson_id)
                    lesson_student = LessonStudentCreateSchema(
                        student_id=student_id,
                        lesson_group_id=lesson_group.id
                    )
                    lesson_students_to_create.append(lesson_student)
                    course_student = await self.course_student_service.get_by_student_id_and_course_id(
                        student_id=student_id,
                        course_id=lesson.course_id
                    )
                    if not course_student:
                        course_students_to_create.append(
                            CourseStudentCreateSchema(
                                student_id=student_id,
                                course_id=lesson.course_id
                            )
                        )
                if lesson_students_to_create:
                    await self.lesson_student_service.bulk_create(lesson_students_to_create)
                    logger.info(f"Created {len(lesson_students_to_create)} LessonStudents for student {student_id}")
                if course_students_to_create:
                    await self.course_student_service.bulk_create(course_students_to_create)
                    logger.info(f"Created {len(course_students_to_create)} CourseStudents for student {student_id}")
            return GroupReadStudentsSchema(
                id=group.id,
                name=group.name,
                description=group.description,
                start_date=group.start_date,
                end_date=group.end_date,
                students_id=students.students_id
            )
        except IntegrityError as e:
            logger.error(f"Error adding students to group: {str(e)}")
            raise ModelNotFoundException(
                model=Student,
                model_id=students.students_id
            )

    async def delete_student(self, group_id: UUID, student_id: UUID) -> bool:
        await self.group_students_repository.delete_student(group_id, student_id)
        return True
    
    async def get_groups_by_student_id(self, student_id: UUID) -> list[GroupsForStudentReadSchema]:
        groups = await self.group_students_repository.get_groups_by_student_id(student_id)
        return groups