from school_site.core.repositories.base_repository import BaseRepositoryImpl
from ..models import Event
from ..schemas import EventCreateSchema, EventUpdateDBSchema, EventReadSchema


class EventRepositoryProtocol(BaseRepositoryImpl[
    Event,
    EventReadSchema,
    EventCreateSchema,
    EventUpdateDBSchema
]):
    pass

class EventRepository(EventRepositoryProtocol):
    pass