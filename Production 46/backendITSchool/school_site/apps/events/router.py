from fastapi import APIRouter, Depends, Path, Query
from uuid import UUID
from school_site.apps.users.depends import access_token_schema
from .depends import (
    get_create_event_use_case,
    get_update_event_use_case,
    get_get_event_use_case,
    get_delete_event_use_case,
    get_get_list_events_use_case,
    get_add_event_for_group_use_case,
    get_add_event_for_users_use_case,
    get_get_event_with_users_use_case,
    get_delete_user_from_event_use_case
)
from .use_cases.create_event_use_case import CreateEventUseCaseProtocol
from .use_cases.update_event_use_case import UpdateEventUseCaseProtocol
from .use_cases.get_event_use_case import GetEventUseCaseProtocol
from .use_cases.delete_event_use_case import DeleteEventUseCaseProtocol
from .use_cases.get_list_events_use_case import GetListEventUseCaseProtocol
from .use_cases.add_event_for_group_use_case import AddEventForGroupUseCaseProtocol
from .use_cases.add_event_for_users_use_case import AddEventForUsersUseCaseProtocol
from .use_cases.get_event_with_users_use_case import GetEventWithUsersUseCaseProtocol
from .use_cases.delete_user_from_event_use_case import DeleteUserFromEventUseCaseProtocol
from .schemas import (
    EventCreateSchema,
    EventReadSchema,
    EventUpdateSchema,
    EventPaginationSchema,
    EventWithUsersReadSchema,
    GroupForEventSchema,
    UsersToAdd
)

router = APIRouter(prefix='/api/events', tags=['Events'])

@router.get('/', response_model=EventPaginationSchema)
async def list_events(
    limit: int = Query(10, ge=1, le=100, description="Number of events to return"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    access_token: str = Depends(access_token_schema),
    use_case: GetListEventUseCaseProtocol = Depends(get_get_list_events_use_case)
) -> EventPaginationSchema:
    return await use_case(access_token, limit=limit, offset=offset)

@router.post('/', response_model=EventReadSchema, status_code=201)
async def create_event(
    event: EventCreateSchema,
    access_token: str = Depends(access_token_schema),
    use_case: CreateEventUseCaseProtocol = Depends(get_create_event_use_case)
) -> EventReadSchema:
    return await use_case(event, access_token)

@router.put('/{event_id}', response_model=EventReadSchema)
async def update_event(
    event: EventUpdateSchema,
    event_id: UUID = Path(..., title="Event ID"),
    access_token: str = Depends(access_token_schema),
    use_case: UpdateEventUseCaseProtocol = Depends(get_update_event_use_case)
) -> EventReadSchema:
    return await use_case(event_id, event, access_token)

@router.get('/{event_id}', response_model=EventReadSchema)
async def get_event(
    event_id: UUID = Path(..., title="Event ID"),
    access_token: str = Depends(access_token_schema),
    use_case: GetEventUseCaseProtocol = Depends(get_get_event_use_case)
) -> EventReadSchema:
    return await use_case(event_id, access_token)

@router.delete('/{event_id}', response_model=None, status_code=204)
async def delete_event(
    event_id: UUID = Path(..., title="Event ID"),
    access_token: str = Depends(access_token_schema),
    use_case: DeleteEventUseCaseProtocol = Depends(get_delete_event_use_case)
) -> None:
    return await use_case(event_id, access_token)

@router.post('/{event_id}/groups', response_model=EventWithUsersReadSchema, status_code=201)
async def add_event_for_group(
    group: GroupForEventSchema,
    event_id: UUID = Path(..., title="Event ID"),
    access_token: str = Depends(access_token_schema),
    use_case: AddEventForGroupUseCaseProtocol = Depends(get_add_event_for_group_use_case)
) -> EventWithUsersReadSchema:
    return await use_case(event_id, group, access_token)

@router.post('/{event_id}/users', response_model=EventWithUsersReadSchema, status_code=201)
async def add_event_for_users(
    users: UsersToAdd,
    event_id: UUID = Path(..., title="Event ID"),
    access_token: str = Depends(access_token_schema),
    use_case: AddEventForUsersUseCaseProtocol = Depends(get_add_event_for_users_use_case)
) -> EventWithUsersReadSchema:
    return await use_case(event_id, users, access_token)

@router.get('/{event_id}/users', response_model=EventWithUsersReadSchema)
async def get_event_with_users(
    event_id: UUID = Path(..., title="Event ID"),
    access_token: str = Depends(access_token_schema),
    use_case: GetEventWithUsersUseCaseProtocol = Depends(get_get_event_with_users_use_case)
) -> EventWithUsersReadSchema:
    return await use_case(event_id, access_token)

@router.delete('/{event_id}/users/{user_id}', response_model=None, status_code=204)
async def delete_user_from_event(
    event_id: UUID = Path(..., title="Event ID"),
    user_id: UUID = Path(..., title="User ID"),
    access_token: str = Depends(access_token_schema),
    use_case: DeleteUserFromEventUseCaseProtocol = Depends(get_delete_user_from_event_use_case)
) -> None:
    return await use_case(event_id, user_id, access_token)