from datetime import datetime
from uuid import UUID
from pydantic import Field, BaseModel
from school_site.core.schemas import CreateBaseModel, UpdateBaseModel, PaginationResultSchema
from school_site.apps.users.schemas import UserWithPhotoReadSchema

class EventBaseSchema(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: str = Field(..., min_length=1)
    start_datetime: datetime
    end_datetime: datetime
    auditorium: str | None = Field(None, max_length=255)
    is_opened: bool = False

    class Config:
        from_attributes = True

class EventCreateSchema(EventBaseSchema, CreateBaseModel):
    pass

class EventUpdateSchema(EventBaseSchema):
    pass

class EventUpdateDBSchema(EventUpdateSchema, UpdateBaseModel):
    pass

class EventReadSchema(EventBaseSchema):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class EventWithUsersReadSchema(BaseModel):
    id: UUID
    users: list[UserWithPhotoReadSchema] = Field(default_factory=list, description="List of user IDs associated with the event")

    class Config:
        from_attributes = True

class GroupForEventSchema(BaseModel):
    group_id: UUID
    with_teacher: bool = False

class EventPaginationSchema(PaginationResultSchema[EventReadSchema]):
    pass


class EventUserBaseSchema(BaseModel):
    user_id: UUID
    event_id: UUID


class EventUserCreateSchema(EventUserBaseSchema, CreateBaseModel):
    pass

class EventUserUpdateSchema(EventUserBaseSchema):
    pass

class EventUserUpdateDBSchema(EventUserUpdateSchema, UpdateBaseModel):
    pass

class EventUserReadSchema(EventUserBaseSchema):
    id: UUID
    class Config:
        from_attributes = True


class UsersToAdd(BaseModel):
    user_ids: list[UUID] = Field(..., min_items=1, description="List of user IDs to add to the event")

    class Config:
        from_attributes = True