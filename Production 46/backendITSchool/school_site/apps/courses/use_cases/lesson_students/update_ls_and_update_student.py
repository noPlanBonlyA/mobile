from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lesson_student import LessonStudentWithStudentService
from ...services.auth import AuthAdminServiceProtocol
from school_site.apps.courses.schemas import LessonStudentReadSchema, LessonStudentUpdateSchema
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.core.enums import UserRole

class UpdateLessonStudentsAndUpdateStudentsUseCaseProtocol(UseCaseProtocol):
    async def __call__(self, lesson_student_id: UUID, lesson_student: LessonStudentUpdateSchema, access_token: str) -> LessonStudentReadSchema:
        ...


class UpdateLessonStudentsAndUpdateStudentsUseCase(UpdateLessonStudentsAndUpdateStudentsUseCaseProtocol):
    def __init__(
        self,
        lesson_student_service: LessonStudentWithStudentService,
        auth_service: AuthAdminServiceProtocol
    ):
        self.lesson_student_service = lesson_student_service
        self.auth_service = auth_service

    async def __call__(self, lesson_student_id: UUID, lesson_student: LessonStudentUpdateSchema, access_token: str) -> LessonStudentReadSchema:
        user = await self.auth_service.decode_access_token(access_token)
        if  user.role not in [UserRole.TEACHER, UserRole.ADMIN, UserRole.SUPERADMIN]:
            raise PermissionDeniedError()
        return await self.lesson_student_service.update_ls_and_update_student(lesson_student_id, lesson_student)
