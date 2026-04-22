from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.events import EventServiceProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..schemas import EventUpdateSchema, EventReadSchema


class UpdateEventUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, event_id: UUID, event: EventUpdateSchema, access_token: str
    ) -> EventReadSchema:
        ...


class UpdateEventUseCase(UpdateEventUseCaseProtocol):
    def __init__(
        self,
        event_service: EventServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.event_service = event_service
        self.auth_service = auth_service

    async def __call__(
        self, event_id: UUID, event: EventUpdateSchema, access_token: str
    ) -> EventReadSchema:
        await self.auth_service.get_admin_user(access_token)
        return await self.event_service.update(event_id, event)