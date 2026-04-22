from typing import Self, Protocol
from datetime import datetime
from ..schemas import AllScheduleReadSchema
from ..repositories.schedule import ScheduleRepositoryProtocol

class ScheduleServiceProtocol(Protocol):
    async def get_student_schedule(self: Self, user_id: str) -> AllScheduleReadSchema:
        ...
    
    async def get_teacher_schedule(self: Self, user_id: str) -> AllScheduleReadSchema:
        ...

    async def get_filtered_student_schedule(
        self: Self,
        user_id: str,
        date_start: datetime,
        date_end: datetime
    ) -> AllScheduleReadSchema:
        ...

    async def get_filtered_teacher_schedule(
        self: Self,
        user_id: str,
        date_start: datetime,
        date_end: datetime
    ) -> AllScheduleReadSchema:
        ...

    async def get_all_groups_schedule(self: Self) -> AllScheduleReadSchema:
        ...

    async def get_filtered_all_groups_schedule(
        self: Self,
        date_start: datetime,
        date_end: datetime
    ) -> AllScheduleReadSchema:
        ...

class ScheduleService(ScheduleServiceProtocol):
    def __init__(
        self: Self,
        schedule_repository: ScheduleRepositoryProtocol,
    ):
        self.schedule_repository = schedule_repository

    async def get_student_schedule(self: Self, user_id: str) -> AllScheduleReadSchema:
        lessons = await self.schedule_repository.get_student_schedule(user_id)
        events = await self.schedule_repository.get_events_schedule(user_id)
        return AllScheduleReadSchema(
            lessons=lessons,
            events=events
        )

    async def get_teacher_schedule(self: Self, user_id: str) -> AllScheduleReadSchema:
        lessons = await self.schedule_repository.get_teacher_schedule(user_id)
        events = await self.schedule_repository.get_events_schedule(user_id)
        return AllScheduleReadSchema(
            lessons=lessons,
            events=events
        )

    async def get_filtered_student_schedule(
        self: Self,
        user_id: str,
        date_start: datetime,
        date_end: datetime
    ) -> AllScheduleReadSchema:
        lessons = await self.schedule_repository.get_filtered_student_schedule(
            user_id,
            date_start,
            date_end
        )
        events = await self.schedule_repository.get_filtered_events_schedule(
            user_id,
            date_start,
            date_end
        )
        return AllScheduleReadSchema(
            lessons=lessons,
            events=events
        )

    async def get_filtered_teacher_schedule(
        self: Self,
        user_id: str,
        date_start: datetime,
        date_end: datetime
    ) -> AllScheduleReadSchema:
        lessons = await self.schedule_repository.get_filtered_teacher_schedule(
            user_id,
            date_start,
            date_end
        )
        events = await self.schedule_repository.get_filtered_events_schedule(
            user_id,
            date_start,
            date_end
        )
        return AllScheduleReadSchema(
            lessons=lessons,
            events=events
        )

    async def get_all_groups_schedule(self: Self) -> AllScheduleReadSchema:
        lessons = await self.schedule_repository.get_all_groups_schedule()
        events = await self.schedule_repository.get_all_group_events_schedule()
        return AllScheduleReadSchema(
            lessons=lessons,
            events=events
        )

    async def get_filtered_all_groups_schedule(
        self: Self,
        date_start: datetime,
        date_end: datetime
    ) -> AllScheduleReadSchema:
        lessons = await self.schedule_repository.get_filtered_all_groups_schedule(
            date_start,
            date_end
        ) 
        events = await self.schedule_repository.get_filtered_all_groups_events_schedule(
            date_start,
            date_end
        )
        return AllScheduleReadSchema(
            lessons=lessons,
            events=events
        )