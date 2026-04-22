from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol
from school_site.apps.students.services.students import StudentServiceProtocol 
from school_site.apps.courses.services.lesson_student import GetLessonStudentsByStudentServiceProtocol
from school_site.apps.courses.schemas import LessonStudentWithLessonGroupReadSchema


class GetAllLessonStudentByStudentUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, access_token: str) -> LessonStudentWithLessonGroupReadSchema:
        ...


class GetAllLessonStudentByStudentUseCase(GetAllLessonStudentByStudentUseCaseProtocol):
    def __init__(
        self,
        auth_admin_service: AuthAdminServiceProtocol,
        student_service: StudentServiceProtocol,
        lesson_student_service: GetLessonStudentsByStudentServiceProtocol,

    ):
        self.auth_admin_service = auth_admin_service
        self.student_service = student_service
        self.lesson_student_service = lesson_student_service

    async def __call__(self, access_token: str) -> LessonStudentWithLessonGroupReadSchema:
        user_data = await self.auth_admin_service.get_student_user(access_token)
        student = await self.student_service.get_by_user_id(user_data.user_id)
        return await self.lesson_student_service.get_all_lesson_students_by_student_id(student.id)
