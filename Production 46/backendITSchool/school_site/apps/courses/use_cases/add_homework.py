from fastapi import UploadFile
from uuid import UUID
import json
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.homeworks_files import FileHomeworkServiceProtocol
from school_site.apps.courses.services.homeworks import HomeworkServiceProtocol
from school_site.apps.courses.services.comments_students import CommentStudentServiceProtocol
from school_site.apps.courses.services.lesson_student import GetLessonStudentByStudentAndLessonServiceProtocol, LessonStudentServiceProtocol
from school_site.apps.students.services.students import StudentServiceProtocol
from school_site.apps.courses.services.lesson_student_homework import LessonStudentHomeworkServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import FileHomeworkCreateSchema, HomeworkCreateSchema, \
    LessonStudentHomeworkCreateSchema, LessonStudentUpdateSchema, AddHomeworkReadSchema, CommentStudentCreateSchema


class AddHomeworkUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, lesson_id: UUID, homework_data: str, file: UploadFile, access_token: str

    )  -> AddHomeworkReadSchema:
        ...


class AddHomeworkUseCase(AddHomeworkUseCaseProtocol):
    def __init__(
        self,
        file_homework_service: FileHomeworkServiceProtocol,
        homework_service: HomeworkServiceProtocol,
        lesson_student_service_by_student_and_lesson: GetLessonStudentByStudentAndLessonServiceProtocol,
        lesson_student_service: LessonStudentServiceProtocol,
        lesson_student_homework_service: LessonStudentHomeworkServiceProtocol,
        student_service: StudentServiceProtocol,
        comment_student_service: CommentStudentServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.file_homework_service = file_homework_service
        self.homework_service = homework_service
        self.lesson_student_service_by_student_and_lesson = lesson_student_service_by_student_and_lesson
        self.lesson_student_service = lesson_student_service
        self.lesson_student_homework_service = lesson_student_homework_service
        self.student_service = student_service
        self.comment_student_service = comment_student_service
        self.auth_service = auth_service

    async def __call__(
        self, lesson_id: UUID, homework_data: str, file: UploadFile, access_token: str

    ) -> AddHomeworkReadSchema:
        student_data = await self.auth_service.get_student_user(access_token)
        homework = FileHomeworkCreateSchema(**json.loads(homework_data))
        created_homework_file =  await self.file_homework_service.create(homework, file)
        homework_for_create = HomeworkCreateSchema(file_id=created_homework_file.id)
        created_homework = await self.homework_service.create(homework_for_create)
        student = await self.student_service.get_by_user_id(student_data.user_id)
        lesson_student = await self.lesson_student_service_by_student_and_lesson.get_lesson_student(student.id, lesson_id)

        student_comment_id = None
        if homework.text:
            comment_for_create = CommentStudentCreateSchema(
                text=homework.text,
                lesson_student_id=lesson_student.id,
                student_id=student.id
            )
            student_comment = await self.comment_student_service.create(comment_for_create)
            student_comment_id = student_comment.id

        lesson_student_homework = LessonStudentHomeworkCreateSchema(
            lesson_student_id=lesson_student.id,
            homework_id=created_homework.id,
            student_comment_id=student_comment_id
            )
        lesson_student_homework = await self.lesson_student_homework_service.create(lesson_student_homework)
        update_homework_lesson_student = LessonStudentUpdateSchema(
            student_id=lesson_student.student_id,
            lesson_group_id=lesson_student.lesson_group_id,
            is_visited=lesson_student.is_visited,
            is_excused_absence=lesson_student.is_excused_absence,
            is_compensated_skip=lesson_student.is_compensated_skip,
            is_sent_homework=True,
            is_graded_homework=lesson_student.is_graded_homework,
            coins_for_visit=lesson_student.coins_for_visit,
            coins_for_homework=lesson_student.coins_for_homework            
        )
        await self.lesson_student_service.update(lesson_student.id, update_homework_lesson_student)
        return AddHomeworkReadSchema(
            lesson_id=lesson_id,
            homework=created_homework_file,
            lesson_student_homework=lesson_student_homework,
            student_comment=homework.text
        )
