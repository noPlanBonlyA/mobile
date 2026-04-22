import logging
from typing import Protocol, Self
from uuid import UUID
from ..repositories.events_users import EventsUsersRepositoryProtocol
from ..schemas import (
    UsersToAdd,
    EventWithUsersReadSchema,
    EventUserCreateSchema,
    GroupForEventSchema
)
from school_site.apps.users.services.users import UserServiceProtocol
from school_site.apps.groups.services.groups import GroupServiceProtocol

logger = logging.getLogger(__name__)


class EventsUsersServiceProtocol(Protocol):
    async def get_event_with_users(self: Self, event_id: UUID) -> EventWithUsersReadSchema:
        ...

    async def add_users_to_event(self: Self, event_id: UUID, user_ids: UsersToAdd) -> EventWithUsersReadSchema:
        ...

    async def add_event_for_group(self: Self, event_id: UUID, group: GroupForEventSchema) -> EventWithUsersReadSchema:
        ...

    async def delete_user_from_event(self: Self, event_id: UUID, user_id: UUID) -> None:
        ...

class EventsUsersService(EventsUsersServiceProtocol):
    def __init__(self: Self, 
                 event_repository: EventsUsersRepositoryProtocol,
                 user_service: UserServiceProtocol,
                 group_service: GroupServiceProtocol):
        self.event_repository = event_repository
        self.user_service = user_service
        self.group_service = group_service

    async def get_event_with_users(self: Self, event_id: UUID) -> EventWithUsersReadSchema:
        logger.info(f"Fetching event with users for event ID: {event_id}")
        events_users = await self.event_repository.get_all_users_by_event_id(event_id)
        
        users = [await self.user_service.get_user_by_id(user.user_id) for user in events_users]
        return EventWithUsersReadSchema(
            id=event_id,
            users=users
        )

    async def add_users_to_event(self: Self, event_id: UUID, user_ids: UsersToAdd) -> EventWithUsersReadSchema:
        logger.info(f"Adding users to event with ID: {event_id}")
        event_for_create = [
            EventUserCreateSchema(user_id=user_id, event_id=event_id) for user_id in user_ids.user_ids
        ]
        await self.event_repository.bulk_create(event_for_create)
        return await self.get_event_with_users(event_id)
    
    async def add_event_for_group(self: Self, event_id: UUID, group: GroupForEventSchema) -> EventWithUsersReadSchema:
        logger.info(f"Adding event for group with ID: {group.group_id}, event ID: {event_id}, with teacher: {group.with_teacher}")
        group_users = await self.group_service.get(group.group_id)
        user_ids = [student.user.id for student in group_users.students]
        user_ids += [group_users.teacher.user.id] if group.with_teacher else []
        return await self.add_users_to_event(event_id, UsersToAdd(user_ids=user_ids))
    
    async def delete_user_from_event(self: Self, event_id: UUID, user_id: UUID) -> None:
        logger.info(f"Deleting user with ID: {user_id} from event with ID: {event_id}")
        await self.event_repository.delete_user_from_event(event_id, user_id)
        return None