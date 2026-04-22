from uuid import UUID
from school_site.core.use_cases import UseCaseProtocol
from ..services.events_users import EventsUsersServiceProtocol
from ..services.auth import AuthAdminServiceProtocol
from ..schemas import EventWithUsersReadSchema


class GetEventWithUsersUseCaseProtocol(UseCaseProtocol):
    async def __call__(
        self, event_id: UUID, access_token: str
    ) -> EventWithUsersReadSchema:
        ...


class GetEventWithUsersUseCase(GetEventWithUsersUseCaseProtocol):
    def __init__(
        self,
        event_service: EventsUsersServiceProtocol,
        auth_service: AuthAdminServiceProtocol
    ):
        self.event_service = event_service
        self.auth_service = auth_service

    async def __call__(
        self,  event_id: UUID, access_token: str
    ) -> EventWithUsersReadSchema:
        await self.auth_service.get_admin_user(access_token)
        return await self.event_service.get_event_with_users(event_id)