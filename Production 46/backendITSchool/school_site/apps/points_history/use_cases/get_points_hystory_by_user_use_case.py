from school_site.core.use_cases import UseCaseProtocol
from school_site.core.schemas import PaginationSchema
from ..services.points_history import PointsHistoryServiceProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..schemas import PointsHistoryPaginationSchema


class GetPointsHistoryByUserUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, access_token: str,
        limit: int = 10, offset: int = 0
    ) -> PointsHistoryPaginationSchema:
        ...


class GetPointsHistoryByUserUseCase(GetPointsHistoryByUserUseCaseProtocol):
    def __init__(
        self,
        history_service: PointsHistoryServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.history_service = history_service
        self.auth_service = auth_service

    async def __call__(
        self,  access_token: str,
        limit: int = 10, offset: int = 0
    ) -> PointsHistoryPaginationSchema:
        user_data = await self.auth_service.get_student_user(access_token)
        params = PaginationSchema(limit=limit, offset=offset)
        return await self.history_service.paginate_points_history_by_user_id(user_data.user_id, params)