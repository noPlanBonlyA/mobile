from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.courses import CourseServiceProtocol
from school_site.apps.courses.schemas import CourseWithPhotoPaginationResultSchema
from school_site.core.schemas import PaginationSchema

class GetListCoursesUseCaseProtocol(UseCaseProtocol[CourseWithPhotoPaginationResultSchema]):
    async def __call__(self, 
                       limit: int = 10, 
                       offset: int = 0) -> CourseWithPhotoPaginationResultSchema:
        ...

class GetListCoursesUseCase(GetListCoursesUseCaseProtocol):
    def __init__(self, course_service: CourseServiceProtocol):
        self.course_service = course_service
    
    async def __call__(self, 
                       limit: int = 10, 
                       offset: int = 0) -> CourseWithPhotoPaginationResultSchema:
        pagination = PaginationSchema(
            limit=limit, 
            offset=offset
            )
        return await self.course_service.list(pagination)