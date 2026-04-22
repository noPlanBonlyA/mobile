import logging
from typing import Protocol, Self
from uuid import UUID
from ..repositories.events import EventRepositoryProtocol
from ..schemas import (
    EventCreateSchema,
    EventUpdateSchema,
    EventUpdateDBSchema,
    EventReadSchema,
    EventPaginationSchema
)
from school_site.core.schemas import PaginationSchema

logger = logging.getLogger(__name__)


class EventServiceProtocol(Protocol):
    async def create(self: Self, event: EventCreateSchema) -> EventReadSchema:
        ...

    async def get(self: Self, event_id: UUID) -> EventReadSchema:
        ...

    async def update(self: Self, event_id: UUID, event: EventUpdateSchema) -> EventReadSchema:
        ...

    async def delete(self: Self, event_id: UUID) -> None:
        ...

    async def list(self: Self, params: PaginationSchema) -> EventPaginationSchema:
        ...

class EventService(EventServiceProtocol):
    def __init__(self: Self, event_repository: EventRepositoryProtocol):
        self.event_repository = event_repository

    async def create(self: Self, event: EventCreateSchema) -> EventReadSchema:
        logger.info("Creating event")
        return await self.event_repository.create(event)

    async def get(self: Self, event_id: UUID) -> EventReadSchema:
        logger.info(f"Fetching event with ID: {event_id}")
        return await self.event_repository.get(event_id)

    async def update(self: Self, event_id: UUID, event: EventUpdateSchema) -> EventReadSchema:
        logger.info(f"Updating event with ID: {event_id}")
        db_event = EventUpdateDBSchema(
            id=event_id,
            **event.model_dump()
        )
        return await self.event_repository.update(db_event)

    async def delete(self: Self, event_id: UUID) -> None:
        logger.info(f"Deleting event with ID: {event_id}")
        await self.event_repository.delete(event_id)

    async def list(self: Self, params: PaginationSchema) -> EventPaginationSchema:
        logger.info("Listing events with pagination")
        events = await self.event_repository.paginate(
            search=None,
            search_by=None,
            sorting=["created_at"],
            pagination=params,
            user=None,
            policies=["can_view"]
        )
        return events