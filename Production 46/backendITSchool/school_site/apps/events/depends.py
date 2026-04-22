from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from school_site.core.db import get_async_session
from school_site.apps.users.services.auth import TokenServiceProtocol
from school_site.apps.users.depends import get_token_service
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.users.depends import get_user_service
from school_site.apps.groups.services.groups import GroupServiceProtocol
from school_site.apps.groups.depends import get_group_service
from .repositories.events import EventRepositoryProtocol, EventRepository
from .repositories.events_users import EventsUsersRepositoryProtocol, EventsUsersRepository
from .services.events import EventServiceProtocol, EventService
from .services.events_users import EventsUsersServiceProtocol, EventsUsersService
from .services.auth import AuthAdminServiceProtocol, AuthService
from .use_cases.create_event_use_case import CreateEventUseCase, CreateEventUseCaseProtocol
from .use_cases.update_event_use_case import UpdateEventUseCase, UpdateEventUseCaseProtocol
from .use_cases.get_event_use_case import GetEventUseCase, GetEventUseCaseProtocol
from .use_cases.delete_event_use_case import DeleteEventUseCase, DeleteEventUseCaseProtocol
from .use_cases.get_list_events_use_case import GetListEventUseCase, GetListEventUseCaseProtocol
from .use_cases.add_event_for_group_use_case import AddEventForGroupUseCase, AddEventForGroupUseCaseProtocol
from .use_cases.add_event_for_users_use_case import AddEventForUsersUseCase, AddEventForUsersUseCaseProtocol
from .use_cases.get_event_with_users_use_case import GetEventWithUsersUseCase, GetEventWithUsersUseCaseProtocol
from .use_cases.delete_user_from_event_use_case import DeleteUserFromEventUseCase, DeleteUserFromEventUseCaseProtocol

def __get_event_repository(
    session: AsyncSession = Depends(get_async_session)
) -> EventRepositoryProtocol:
    return EventRepository(session)


def get_event_service(
    event_repository: EventRepositoryProtocol = Depends(__get_event_repository)
) -> EventServiceProtocol:
    return EventService(event_repository)

def get_auth_service(
    token_service: TokenServiceProtocol = Depends(get_token_service)
) -> AuthAdminServiceProtocol:
    return AuthService(token_service)


def get_create_event_use_case(
    event_service: EventServiceProtocol = Depends(get_event_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> CreateEventUseCaseProtocol:
    return CreateEventUseCase(event_service, auth_service)

def get_update_event_use_case(
    event_service: EventServiceProtocol = Depends(get_event_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> UpdateEventUseCaseProtocol:
    return UpdateEventUseCase(event_service, auth_service)

def get_get_event_use_case(
    event_service: EventServiceProtocol = Depends(get_event_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> GetEventUseCaseProtocol:
    return GetEventUseCase(event_service, auth_service)

def get_delete_event_use_case(
    event_service: EventServiceProtocol = Depends(get_event_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> DeleteEventUseCaseProtocol:
    return DeleteEventUseCase(event_service, auth_service)

def get_get_list_events_use_case(
    event_service: EventServiceProtocol = Depends(get_event_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> GetListEventUseCaseProtocol:
    return GetListEventUseCase(event_service, auth_service)


def __get_events_users_repository(
    session: AsyncSession = Depends(get_async_session)
) -> EventsUsersRepositoryProtocol:
    return EventsUsersRepository(session)

def get_events_users_service(
    events_users_repository: EventsUsersRepositoryProtocol = Depends(__get_events_users_repository),
    user_service: UserServiceProtocol = Depends(get_user_service),
    group_service: GroupServiceProtocol = Depends(get_group_service)
) -> EventsUsersServiceProtocol:
    return EventsUsersService(
        events_users_repository, user_service, group_service
    )

def get_add_event_for_group_use_case(
    event_service: EventsUsersServiceProtocol = Depends(get_events_users_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> AddEventForGroupUseCaseProtocol:
    return AddEventForGroupUseCase(event_service, auth_service)

def get_add_event_for_users_use_case(
    event_service: EventsUsersServiceProtocol = Depends(get_events_users_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> AddEventForUsersUseCaseProtocol:
    return AddEventForUsersUseCase(event_service, auth_service)

def get_get_event_with_users_use_case(
    event_service: EventsUsersServiceProtocol = Depends(get_events_users_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> GetEventWithUsersUseCaseProtocol:
    return GetEventWithUsersUseCase(event_service, auth_service)

def get_delete_user_from_event_use_case(
    event_service: EventsUsersServiceProtocol = Depends(get_events_users_service),
    auth_service: AuthAdminServiceProtocol = Depends(get_auth_service)
) -> DeleteUserFromEventUseCaseProtocol:
    return DeleteUserFromEventUseCase(event_service, auth_service)