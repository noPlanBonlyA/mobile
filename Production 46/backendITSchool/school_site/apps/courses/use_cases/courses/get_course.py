from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.courses import CourseServiceProtocol
from school_site.apps.courses.schemas import CourseWithPhotoReadSchema

class GetCourseUseCaseProtocol(UseCaseProtocol[CourseWithPhotoReadSchema]):
    async def __call__(self, course_id: UUID) -> CourseWithPhotoReadSchema:
        ...

class GetCourseUseCase(GetCourseUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, course_id: UUID) -> CourseWithPhotoReadSchema:
        return await self.course_service.get(course_id)