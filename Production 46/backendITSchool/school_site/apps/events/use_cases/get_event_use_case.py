from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.events import EventServiceProtocol
from ..schemas import EventReadSchema


class GetEventUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, event_id: UUID, access_token: str
    ) -> EventReadSchema:
        ...


class GetEventUseCase(GetEventUseCaseProtocol):
    def __init__(
        self,
        event_service: EventServiceProtocol,
    ):
        self.event_service = event_service

    async def __call__(
        self,  event_id: UUID, access_token: str
    ) -> EventReadSchema:
        return await self.event_service.get(event_id)