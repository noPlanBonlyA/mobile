from uuid import UUID
import sqlalchemy as sa
from school_site.core.repositories.base_repository import BaseRepositoryImpl
from school_site.core.utils.exceptions import ModelNotFoundException
from ..models import EventsUsers
from ..schemas import EventUserCreateSchema, EventUserUpdateDBSchema, EventUserReadSchema


class EventsUsersRepositoryProtocol(BaseRepositoryImpl[
    EventsUsers,
    EventUserReadSchema,
    EventUserCreateSchema,
    EventUserUpdateDBSchema
]):
    async def get_all_users_by_event_id(self, event_id: UUID) -> list[EventsUsers]:
        ...
    
    async def bulk_create(self, create_objects: list[EventUserCreateSchema]) -> list[EventUserReadSchema]:
        ...

    async def delete_user_from_event(self, event_id: UUID, user_id: UUID) -> bool:
        ...

class EventsUsersRepository(EventsUsersRepositoryProtocol):
    async def get_all_users_by_event_id(self, event_id: UUID) -> list[EventsUsers]:
        async with self.session as s:
            stmt = (
                sa.select(self.model_type).where(
                    self.model_type.event_id == event_id
                )
            )
            results = (await s.execute(stmt)).scalars().all()
            if results is None:
                raise ModelNotFoundException(
                    model=self.model_type,
                    model_id=event_id
                )
            return [EventUserReadSchema.model_validate(result) for result in results]
        
    async def bulk_create(self, create_objects: list[EventUserCreateSchema]) -> list[EventUserReadSchema]:
        if len(create_objects) == 0:
            return []
        async with self.session as s, s.begin():
            statement = (
                sa.dialects.postgresql.insert(self.model_type)
                .returning(self.model_type)
                .on_conflict_do_nothing(
                    index_elements=['user_id', 'event_id']
                )
            )
            models = (await s.scalars(statement, [x.model_dump() for x in create_objects])).all()
            return [self.read_schema_type.model_validate(model, from_attributes=True) for model in models]
        
    async def delete_user_from_event(self, event_id: UUID, user_id: UUID) -> bool:
        async with self.session as s, s.begin():
            stmt = (
                sa.delete(self.model_type)
                .where(
                    self.model_type.event_id == event_id,
                    self.model_type.user_id == user_id
                )
            )
            await s.execute(stmt)
            return True