from school_site.core.use_cases import UseCaseProtocol
from ..services.points_history import PointsHistoryServiceProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..schemas import PointsHistoryCreateSchema, PointsHistoryReadSchema
from school_site.core.utils.exceptions import PermissionDeniedError
from school_site.core.enums import UserRole


class CreatePointsHistoryUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, history: PointsHistoryCreateSchema, access_token: str
    ) -> PointsHistoryReadSchema:
        ...


class CreatePointsHistoryUseCase(CreatePointsHistoryUseCaseProtocol):
    def __init__(
        self,
        history_service: PointsHistoryServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.history_service = history_service
        self.auth_service = auth_service

    async def __call__(
        self,  history: PointsHistoryCreateSchema, access_token: str
    ) -> PointsHistoryReadSchema:
        user = await self.auth_service.decode_access_token(access_token)
        if  user.role not in [UserRole.TEACHER, UserRole.ADMIN, UserRole.SUPERADMIN]:
            raise PermissionDeniedError()
        return await self.history_service.create_points_history(history)