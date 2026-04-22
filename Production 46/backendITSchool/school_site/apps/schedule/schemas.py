from datetime import datetime
from uuid import UUID
from pydantic import BaseModel

class ScheduleReadSchema(BaseModel):
    id: UUID
    lesson_id: UUID
    group_id: UUID
    start_datetime: datetime
    end_datetime: datetime
    auditorium: str
    is_opened: bool
    lesson_name: str
    course_name: str

    class Config:
        from_attributes = True 

class ScheduleEventsSchema(BaseModel):
    event_id: UUID
    event_name: str
    start_datetime: datetime
    end_datetime: datetime
    auditorium: str

class AllScheduleReadSchema(BaseModel):
    lessons: list[ScheduleReadSchema]
    events: list[ScheduleEventsSchema]
