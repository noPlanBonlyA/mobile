from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.events import EventServiceProtocol
from ..services.auth import AuthAdminServiceProtocol


class DeleteEventUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, event_id: UUID, access_token: str
    ) -> None:
        ...


class DeleteEventUseCase(DeleteEventUseCaseProtocol):
    def __init__(
        self,
        event_service: EventServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.event_service = event_service
        self.auth_service = auth_service

    async def __call__(
        self,  event_id: UUID, access_token: str
    ) -> None:
        await self.auth_service.get_admin_user(access_token)
        return await self.event_service.delete(event_id)