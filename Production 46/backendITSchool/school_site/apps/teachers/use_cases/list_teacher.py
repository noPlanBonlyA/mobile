from uuid import UUID
from school_site.core.schemas import PaginationSchema
from school_site.core.use_cases import UseCaseProtocol 
from ..services.auth import AuthAdminAndTeacherServiceProtocol
from ..services.teachers import TeacherServiceProtocol
from ..schemas import TeacherPaginationWithUserAndUserPhotoResultSchema


class GetListTeacherUseCaseProtocol(UseCaseProtocol[TeacherPaginationWithUserAndUserPhotoResultSchema]):
    async def __call__(self, access_token: str, limit: int = 10,
                       offset: int = 0) -> TeacherPaginationWithUserAndUserPhotoResultSchema:
        ...


class GetListTeacherUseCase(GetListTeacherUseCaseProtocol):
    def __init__(self, auth_service: AuthAdminAndTeacherServiceProtocol, teacher_service: TeacherServiceProtocol):
        self.auth_service = auth_service
        self.teacher_service = teacher_service

    async def __call__(self, access_token: str, limit: int = 10,
                       offset: int = 0) -> TeacherPaginationWithUserAndUserPhotoResultSchema:
        await self.auth_service.get_admin_user(access_token)
        pagination = PaginationSchema(
            limit=limit,
            offset=offset
        )
        return await self.teacher_service.list(pagination) 