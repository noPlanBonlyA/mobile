from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from school_site.apps.courses.services.lessons import LessonServiceProtocol
from school_site.apps.courses.schemas import LessonPaginationResultSchema
from school_site.core.schemas import PaginationSchema

class GetListLessonsUseCaseProtocol(UseCaseProtocol[LessonPaginationResultSchema]):
    async def __call__(self, course_id: UUID, limit: int = 10, offset: int = 0) -> LessonPaginationResultSchema:
        ...

class GetListLessonsUseCase(GetListLessonsUseCaseProtocol):
    def __init__(self, lesson_service: LessonServiceProtocol):
        self.lesson_service = lesson_service
    
    async def __call__(self, course_id: UUID, limit: int = 10, offset: int = 0) -> LessonPaginationResultSchema:
        pagination = PaginationSchema(
            limit=limit,
            offset=offset
        )
        return await self.lesson_service.list(course_id, pagination) 