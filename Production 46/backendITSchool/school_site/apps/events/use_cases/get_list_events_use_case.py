from school_site.core.use_cases import UseCaseProtocol
from school_site.core.schemas import PaginationSchema
from ..services.events import EventServiceProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..schemas import EventPaginationSchema


class GetListEventUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, access_token: str,
        limit: int = 10, offset: int = 0
    ) -> EventPaginationSchema:
        ...


class GetListEventUseCase(GetListEventUseCaseProtocol):
    def __init__(
        self,
        event_service: EventServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.event_service = event_service
        self.auth_service = auth_service

    async def __call__(
        self,  access_token: str, limit: int = 10, offset: int = 0
    ) -> EventPaginationSchema:
        await self.auth_service.get_admin_user(access_token)
        params = PaginationSchema(limit=limit, offset=offset)
        return await self.event_service.list(params)