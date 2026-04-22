from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.courses import CourseServiceProtocol
from school_site.apps.courses.services.auth import AuthAdminServiceProtocol

class DeleteCourseUseCaseProtocol(UseCaseProtocol[None]):
    async def __call__(self, course_id: UUID, access_token: str) -> None:
        ...

class DeleteCourseUseCase(DeleteCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol, auth_service: AuthAdminServiceProtocol):
        self.course_service = course_service
        self.auth_service = auth_service
    
    async def __call__(self, course_id: UUID, access_token: str) -> None:
        await self.auth_service.get_admin_user(access_token)
        return await self.course_service.delete(course_id)