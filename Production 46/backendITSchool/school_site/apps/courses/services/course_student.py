import logging
from typing import Protocol
from uuid import UUID
from school_site.core.services.files import FileServiceProtocol
from ..repositories.course_student import CourseStudentRepositoryProtocol
from ..schemas import (
    CourseStudentCreateSchema,
    CourseStudentUpdateSchema,
    CourseStudentReadSchema,
    CourseStudentUpdateDBSchema,
    CourseStudentWithCoursesSchema,
    PhotoReadSchema,
    CourseWithPhotoReadSchema
)

logger = logging.getLogger(__name__)


class CourseStudentServiceProtocol(Protocol):
    async def create(self, course_student: CourseStudentCreateSchema) -> CourseStudentReadSchema:
        ...

    async def get(self, course_student_id: UUID) -> CourseStudentReadSchema:
        ...

    async def update(self, course_student_id: UUID, course_student: CourseStudentUpdateSchema) -> CourseStudentReadSchema:
        ...

    async def delete(self, course_student_id: UUID) -> None:
        ...

    async def get_courses_by_student_id(self, student_id: UUID) -> list[CourseStudentWithCoursesSchema]:
        ...
    
    async def bulk_create(self, course_students: list[CourseStudentCreateSchema]) -> list[CourseStudentReadSchema]:
        ...
    
    async def get_by_student_id_and_course_id(self, student_id: UUID, course_id: UUID) -> CourseStudentReadSchema:
        ...

class CourseStudentService(CourseStudentServiceProtocol):
    def __init__(self, course_student_repository: CourseStudentRepositoryProtocol):
        self.course_student_repository = course_student_repository

    async def create(self, course_student: CourseStudentCreateSchema) -> CourseStudentReadSchema:
        logger.info("Creating CourseStudent")
        return await self.course_student_repository.create(course_student)

    async def get(self, course_student_id: UUID) -> CourseStudentReadSchema:
        logger.info(f"Fetching CourseStudent with ID: {course_student_id}")
        return await self.course_student_repository.get(course_student_id)

    async def update(self, course_student_id: UUID, course_student: CourseStudentUpdateSchema) -> CourseStudentReadSchema:
        logger.info(f"Updating CourseStudent with ID: {course_student_id}")
        db_course_student = CourseStudentUpdateDBSchema(
            id=course_student_id,
            student_id=course_student.student_id,
            course_id=course_student.course_id,
            progress=course_student.progress,
        )
        return await self.course_student_repository.update(db_course_student)

    async def delete(self, course_student_id: UUID) -> None:
        logger.info(f"Deleting CourseStudent with ID: {course_student_id}")
        await self.course_student_repository.delete(course_student_id)

    async def bulk_create(self, course_students: list[CourseStudentCreateSchema]) -> list[CourseStudentReadSchema]:
        logger.info("Bulk creating CourseStudents")
        return await self.course_student_repository.bulk_create(course_students)
    
    async def get_by_student_id_and_course_id(self, student_id: UUID, course_id: UUID) -> CourseStudentReadSchema:
        logger.info(f"Fetching CourseStudent for student ID: {student_id} and course ID: {course_id}")
        return await self.course_student_repository.get_by_student_id_and_course_id(student_id, course_id)

    
class GetCoursesByStudentServiceProtocol(Protocol):
    async def get_courses_by_student_id(self, student_id: UUID) -> list[CourseStudentWithCoursesSchema]:
        ...


class GetCoursesByStudentService(GetCoursesByStudentServiceProtocol):
    def __init__(self, course_student_repository: CourseStudentRepositoryProtocol,
                 file_service: FileServiceProtocol):
        self.course_student_repository = course_student_repository
        self.file_service = file_service

    async def get_courses_by_student_id(self, student_id: UUID) -> list[CourseStudentWithCoursesSchema]:
        logger.info(f"Fetching courses for student with ID: {student_id}")
        courses =  await self.course_student_repository.get_courses_by_student_id(student_id)
        course_photos = []
        for course in courses:
            photo_url = None
            if course.course.photo:
                photo_url = await self.file_service.get_url(course.course.photo.path)
            converted_course = CourseWithPhotoReadSchema(
                id=course.course.id,
                name=course.course.name,
                description=course.course.description,
                age_category=course.course.age_category,
                price=course.course.price,
                author_name=course.course.author_name,
                photo=PhotoReadSchema(
                    id=course.course.photo.id,
                    name=course.course.photo.name,
                    course_id=course.course.photo.course_id,
                    url=photo_url
                    ) if photo_url else None
            )
            converted_course_students = CourseStudentWithCoursesSchema(
                id=course.id,
                student_id=course.student_id,
                course_id=course.course_id,
                progress=course.progress,
                course=converted_course
            )
            course_photos.append(converted_course_students)
        return course_photos