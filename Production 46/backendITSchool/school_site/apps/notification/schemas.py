from school_site.core.schemas import BaseModel, CreateBaseModel, UpdateBaseModel
from uuid import UUID
from datetime import datetime
from typing import TypeVar, Generic, List, Optional
from enum import Enum

T = TypeVar('T')

class RecipientType(str, Enum):
    STUDENT = 'student'
    GROUP = 'group'

class PaginationResultSchema(BaseModel, Generic[T]):
    count: int
    objects: List[T]

class NotificationBase(BaseModel):
    content: str

class NotificationCreateSchema(CreateBaseModel):
    content: str

class NotificationReadSchema(BaseModel):
    id: UUID
    content: str
    created_at: datetime

class NotificationUpdateSchema(UpdateBaseModel):
    content: str

class NotificationRecipientCreateSchema(BaseModel):
    recipient_type: RecipientType
    recipient_id: UUID

class NotificationRecipientReadSchema(BaseModel):
    notification_id: UUID
    recipient_type: RecipientType
    recipient_id: UUID

class ReadStatusCreateSchema(CreateBaseModel):
    notification_id: UUID
    student_id: UUID
    is_read: bool = False
    read_at: Optional[datetime] = None

class ReadStatusReadSchema(BaseModel):
    notification_id: UUID
    student_id: UUID
    is_read: bool
    read_at: Optional[datetime]

class NotificationWithStatusSchema(NotificationReadSchema):
    is_read: bool = False
    read_at: Optional[datetime] = None